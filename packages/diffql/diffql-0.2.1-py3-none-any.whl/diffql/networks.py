from functools import wraps
import numpy as np
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parameter import Parameter
import torch.nn.init as init
import cvxpy as cp
from cvxpylayers.torch import CvxpyLayer


def construct_layer_list(node_list: list, act):
    """
    Construct a list of layers for feedforward neural networks (FNN).

    node_list: hidden layer nodes ([64, 64, 64])
    act: activation function
    """
    layer_list = nn.ModuleList()  # to be tracked by torch
    for i in range(1, len(node_list)):
        node_prev = node_list[i-1]
        node = node_list[i]
        layer_list.append(nn.Linear(node_prev, node))
        if i is not len(node_list)-1:
            layer_list.append(act)
    return layer_list


def normalise_forward(func):
    @wraps(func)
    def inner(self, x, u, **kwargs):
        device = next(self.parameters()).device.type
        x = x.to(device)
        u = u.to(device)
        if self.normalise_factor[0] is not None:
            self.normalise_factor[0] = self.normalise_factor[0].to(device)
        if self.normalise_factor[1] is not None:
            self.normalise_factor[1] = self.normalise_factor[1].to(device)
        if self.normalise_factor[2] is not None:
            self.normalise_factor[2] = self.normalise_factor[2].to(device)
        if self.normalise_factor[0] is None:
            x_normalised = x
        else:
            x_normalised = x / self.normalise_factor[0]
        if self.normalise_factor[1] is None:
            u_normalised = u
        else:
            u_normalised = u / self.normalise_factor[1]
        f_normalised = func(self, x_normalised, u_normalised, **kwargs)
        if self.normalise_factor[2] is None:
            f = f_normalised
        else:
            f = f_normalised * self.normalise_factor[2]
        return f
    return inner


def normalise_minimise(func):
    @wraps(func)
    def inner(self, x, **kwargs):
        device = next(self.parameters()).device.type
        if self.normalise_factor[0] is not None:
            self.normalise_factor[0] = self.normalise_factor[0].to(device)
        if self.normalise_factor[1] is not None:
            self.normalise_factor[1] = self.normalise_factor[1].to(device)
        if self.normalise_factor[2] is not None:
            self.normalise_factor[2] = self.normalise_factor[2].to(device)
        # type check
        x_normal = self.normalise_factor[0]
        u_normal = self.normalise_factor[1]
        if type(x) is np.ndarray and self.normalise_factor[0] is not None:
            x_normal = self.normalise_factor[0].detach().cpu().numpy()
        if type(x) is np.ndarray and self.normalise_factor[1] is not None:
            u_normal = self.normalise_factor[1].detach().cpu().numpy()
        # normalisation
        x_normalised = x if x_normal is None else x / x_normal
        u_normalised = func(self, x_normalised, **kwargs)
        u = u_normalised if u_normal is None else u_normalised * u_normal
        return u
    return inner


class AbstractBivariateApproximator(nn.Module):
    """
    The "bivariate" does not mean that the dimension of the argument of this approximator would be two;
    Instead, it means that the approximator has two arguments as `f(x, u)`.
    """
    def __init__(self, x=None, u=None, f=None):
        super().__init__()
        self.set_normalise_factor(x, u, f)

    def minimise_np(self, xs):
        raise NotImplementedError("TODO: for non-parametrised convex approximators, we should add an ad-hoc minimise algorithm.")

    def minimise_tch(self, xs):
        raise NotImplementedError("TODO: for non-parametrised convex approximators, we should add an ad-hoc minimise algorithm.")

    def set_normalise_factor(self, x, u, f):
        assert type(x) is torch.Tensor or x is None
        assert type(u) is torch.Tensor or u is None
        assert type(f) is torch.Tensor or f is None
        self.normalise_factor = [x, u, f]


class FNN(AbstractBivariateApproximator):
    def __init__(
        self, n: int, m: int, _node_list, act,
        x_normal=None, u_normal=None, f_normal=None,
    ):
        super().__init__(x_normal, u_normal, f_normal)
        self.n = n
        self.m = m
        node_list = [n+m, *_node_list, 1]
        self.layer_list = construct_layer_list(node_list, act)

    @normalise_forward
    def forward(self, xs, us):
        zs = torch.cat((xs, us), dim=-1)
        for layer in self.layer_list:
            zs = layer(zs)
        return zs


class AbstractParametrisedConvexApproximator(AbstractBivariateApproximator):
    def __init__(
        self,
        x_normal=None, u_normal=None, f_normal=None,
    ):
        super().__init__(x_normal, u_normal, f_normal)

    def minimise_np(self, xs):
        raise NotImplementedError("TODO: add cvxpy-like minimise algorithm")

    def minimise_tch(self, xs):
        raise NotImplementedError("TODO: add cvxpylayers-like minimise algorithm")

    def set_shift(self, x_shift, u_shift):
        if x_shift is None and u_shift is None:
            self.shift = None
        elif x_shift is not None and u_shift is not None:
            assert type(x_shift) is torch.Tensor
            assert type(u_shift) is torch.Tensor
            assert len(x_shift.shape) == 1
            assert len(u_shift.shape) == 1
            self.shift = [x_shift, u_shift]
        else:
            raise ValueError("`x_shift` and `u_shift` should be both None or both not None")

    def _cvxpylayer_wrapper(self, u, obj, u_min, u_max):
        m = self.m
        constraints = []
        if u_min is not None:
            if u_min is torch.Tensor:
                u_min = u_min.numpy()
            if len(u_min.shape) == 1:
                u_min = u_min.reshape((m,))
            constraints += [u >= u_min]
        if u_max is not None:
            if u_max is torch.Tensor:
                u_max = u_max.numpy()
            if len(u_max.shape) == 1:
                u_max = u_max.reshape((m,))
            constraints += [u <= u_max]
        prob = cp.Problem(obj, constraints)
        cvxpylayer = CvxpyLayer(
            prob,
            parameters=[*self.parameters_cp],
            variables=[u],
        )
        return prob, cvxpylayer

    def initialise_cvxpylayer(self, u_min, u_max, act):
        # normalisation
        if self.normalise_factor[1] is None:
            u_min_normalised, u_max_normalised = u_min, u_max
        else:
            u_min_normalised, u_max_normalised = u_min / self.normalise_factor[1], u_max / self.normalise_factor[1]
        m, T, i_max = self.m, self.T, self.i_max
        self.u_cp = cp.Variable((m,))
        alpha_is_u_cp = cp.Parameter((i_max, m))
        beta_is_plus_alpha_is_times_x_cp = cp.Parameter((i_max,))
        tmp_cp = self.u_cp @ alpha_is_u_cp.T + beta_is_plus_alpha_is_times_x_cp  # u @ A.T + b
        # network shift
        if self.shift is None:
            _tmp = T * cp.log_sum_exp((1/T)*tmp_cp)
            self.parameters_cp = [alpha_is_u_cp, beta_is_plus_alpha_is_times_x_cp]
        else:
            offset_value = cp.Parameter((1,))
            _tmp = T * cp.log_sum_exp((1/T)*tmp_cp) - offset_value
            self.parameters_cp = [alpha_is_u_cp, beta_is_plus_alpha_is_times_x_cp, offset_value]
        # output activation
        if act is None:
            pass
        elif act == "relu":
            _tmp = cp.pos(_tmp)
        # normalisation
        if self.normalise_factor[2] is not None:
            _tmp = self.normalise_factor[2].squeeze() * _tmp  # to make normalise_factor a scalar
        obj = cp.Minimize(_tmp)
        self.prob, self.cvxpylayer = self._cvxpylayer_wrapper(self.u_cp, obj, u_min_normalised, u_max_normalised)


class ParametrisedConvexApproximator(AbstractParametrisedConvexApproximator):
    def __init__(
        self, n: int, m: int, i_max: int, node_list, act,
        x_normal=None, u_normal=None, f_normal=None,
    ):
        super().__init__(x_normal, u_normal, f_normal)
        self.n = n
        self.m = m
        self.i_max = i_max
        self.layer_list = construct_layer_list(node_list, act)

    def NN(self, xs):
        for layer in self.layer_list:
            xs = layer(xs)
        return xs


class _PLSE(ParametrisedConvexApproximator):
    def __init__(
        self, n: int, m: int, i_max: int, T: float, _node_list, act, u_min=None, u_max=None, act_output=None,
        x_normal=None, u_normal=None, f_normal=None,
    ):
        node_list = [n, *_node_list, i_max*(m+1)]
        super().__init__(n, m, i_max, node_list, act, x_normal, u_normal, f_normal)
        self.T = T
        self.initialise_cvxpylayer(u_min, u_max, act_output)

    @normalise_forward
    def forward(self, xs, us):
        d = xs.shape[0]
        i_max, m, T = self.i_max, self.m, self.T
        X = torch.reshape(self.NN(xs), (d, i_max, m+1))
        alpha_is = X[:, :, 0:-1]  # d x i_max x m
        beta_is = X[:, :, -1]  # d x i_max
        tmp = torch.einsum("bm,bim->bi", us, alpha_is) + beta_is  # each row corresponds to us[i, :] @ alpha_is[i, :, :].T
        return T * torch.logsumexp((1/T)*tmp, dim=-1, keepdim=True)

    @normalise_minimise
    def minimise_np(self, x, solver=cp.MOSEK):
        assert type(x) is np.ndarray
        assert len(x.shape) == 1
        device = next(self.parameters()).device.type
        i_max, m = self.i_max, self.m
        x = torch.Tensor(x.reshape(1, *x.shape)).to(device)  # 1 x n
        X = torch.reshape(self.NN(x), (i_max, m+1)).detach().cpu().numpy()
        self.parameters_cp[0].value = X[:, 0:-1]  # i_max x m
        self.parameters_cp[1].value = X[:, -1]  # i_max
        if self.shift is not None:
            self.parameters_cp[2].value = self.forward(self.shift[0].reshape(1, self.n),
                                                       self.shift[1].reshape(1, self.m),).detach().cpu().numpy().reshape(1,)  # TODO
        self.prob.solve(solver=solver)
        u = self.u_cp.value
        return u

    @normalise_minimise
    def minimise_tch(self, xs):
        assert type(xs) is torch.Tensor
        assert len(xs.shape) == 2
        d = xs.shape[0]
        i_max, m = self.i_max, self.m
        X = torch.reshape(self.NN(xs), (d, i_max, m+1))
        alpha_is = X[:, :, 0:-1]  # d x i_max x m
        beta_is = X[:, :, -1]  # d x i_max
        if self.shift is not None:
            x_shift, u_shift = self.shift
            offset_value = self.forward(x_shift.reshape(1, self.n),
                                        u_shift.reshape(1, self.m),).reshape(1,)
            us, = self.cvxpylayer(alpha_is, beta_is, offset_value.repeat(d, 1))
        else:
            us, = self.cvxpylayer(alpha_is, beta_is)
        return us


class PLSE(_PLSE):
    def __init__(self, *args, x_shift=None, u_shift=None, **kwargs):
        """
        LSE considering shift
        """
        self.set_shift(x_shift, u_shift)
        super().__init__(*args, **kwargs)

    def forward(self, xs, us):
        if self.shift is None:
            fs = super().forward(xs, us)
        else:
            x_shift, u_shift = self.shift
            fs = super().forward(xs, us) - super().forward(x_shift.reshape(1, self.n), u_shift.reshape(1, self.m))
        return fs


class PLSEPlus(PLSE):
    def __init__(self, *args, act_output="relu", **kwargs):
        """
        PLSE+
        """
        super().__init__(*args, **kwargs, act_output=act_output)

    def forward(self, xs, us):
        return F.relu(super().forward(xs, us))


class QuadraticApproximator(AbstractParametrisedConvexApproximator):
    def __init__(
        self, n: int, m: int,
        u_min=None, u_max=None,
        x_normal=None, u_normal=None, f_normal=None,
    ):
        super().__init__(x_normal, u_normal, f_normal)
        self.n = n
        self.m = m
        param_11 = torch.randn((n, n))  # TODO: initialisation method
        param_12 = torch.randn((n, m))  # TODO: initialisation method
        param_22 = torch.randn((m, m))  # TODO: initialisation method
        self.param_11 = Parameter(param_11)
        self.param_12 = Parameter(param_12)
        self.param_22 = Parameter(param_22)
        # cvxpylayers
        # normalisation
        if self.normalise_factor[1] is None:
            u_min_normalised, u_max_normalised = u_min, u_max
        else:
            u_min_normalised, u_max_normalised = u_min / self.normalise_factor[1], u_max / self.normalise_factor[1]
        self.u_cp = cp.Variable((m,))
        param_0_cp = cp.Parameter((1,))  # bias term
        param_1_cp = cp.Parameter((m,))  # linear term
        param_2_cp = cp.Parameter((m, m))  # sqrt of quadratic term
        self.parameters_cp = [param_0_cp, param_1_cp, param_2_cp]
        _tmp = cp.sum_squares(param_2_cp @ self.u_cp) + param_1_cp @ self.u_cp.T + param_0_cp
        obj = cp.Minimize(_tmp)
        self.prob, self.cvxpylayer = self._cvxpylayer_wrapper(self.u_cp, obj, u_min_normalised, u_max_normalised)

    @normalise_forward
    def forward(self, xs, us):
        _result_0 = torch.einsum("bi,ij,jb", xs, self.param_11, xs.T)  # each element = x_i^T H_11 x_i
        _result_1 = 2 * torch.einsum("bi,ij,jb", xs, self.param_12, us.T)  # each element = x_i^T (2*H_12) u_i
        _result_2 = torch.einsum("bi,ij,ji,jb->b", us, self.param_22.T, self.param_22, us.T)  # each element = u_i^T H_22 u_i
        return (_result_0 + _result_1 + _result_2).reshape(-1, 1)

    @normalise_minimise
    def minimise_np(self, x, solver=cp.MOSEK):
        assert type(x) is np.ndarray
        assert len(x.shape) == 1
        self.parameters_cp[0].value = np.array([x @ self.param_11.detach().cpu().numpy() @ x.T])
        self.parameters_cp[1].value = 2 * x @ self.param_12.detach().cpu().numpy()
        self.parameters_cp[2].value = self.param_22.detach().cpu().numpy()
        self.prob.solve(solver=solver)
        return self.u_cp.value

    @normalise_minimise
    def minimise_tch(self, xs):
        assert type(xs) is torch.Tensor
        assert len(xs.shape) == 2
        d = xs.shape[0]
        param_cp_0 = torch.einsum("bi,ij,jb->b", xs, self.param_11, xs.T).reshape(-1, 1)  # d x 1
        param_cp_1 = 2 * xs @ self.param_12  # d x m
        param_cp_2 = self.param_22.repeat(d, 1, 1)
        us, = self.cvxpylayer(param_cp_0, param_cp_1, param_cp_2)
        return us


class ConvexApproximator(AbstractParametrisedConvexApproximator):
    def __init__(
        self, n: int, m: int, alpha_is, beta_is,
        x_normal=None, u_normal=None, f_normal=None,
    ):
        """
        alpha_is: i_max x (n+m) Tensor
        beta_is: i_max x (1) Tensor
        """
        super().__init__(x_normal, u_normal, f_normal)
        self.n = n
        self.m = m
        i_max = alpha_is.shape[0]
        assert beta_is.shape[0] == i_max
        assert alpha_is.shape[1] == n + m
        self.i_max = i_max
        self.alpha_is = Parameter(alpha_is)  # torch
        self.beta_is = Parameter(beta_is)  # torch


class _LSE(ConvexApproximator):
    def __init__(
        self, n: int, m: int, i_max: int, T: float, u_min=None, u_max=None, act_output=None,
        x_normal=None, u_normal=None, f_normal=None,
    ):
        assert T > 0
        alpha_is = torch.empty((i_max, n+m))
        beta_is = torch.empty((i_max,))
        # see the source code of torch.nn.modules.linear
        # https://github.com/pytorch/pytorch/blob/master/torch/nn/modules/linear.py
        init.kaiming_uniform_(alpha_is, a=math.sqrt(5))
        fan_in, _ = init._calculate_fan_in_and_fan_out(alpha_is)
        bound = 1 / math.sqrt(fan_in) if fan_in > 0 else 0
        init.uniform_(beta_is, -bound, bound)
        super().__init__(n, m, alpha_is, beta_is, x_normal, u_normal, f_normal)
        self.T = T
        # cvxpylayer
        self.initialise_cvxpylayer(u_min, u_max, act_output)

    @normalise_forward
    def forward(self, xs, us):
        T = self.T
        n = self.n
        alpha_is_u = self.alpha_is[:, n:]
        beta_is_plus_alpha_is_times_x = xs @ self.alpha_is[:, 0:n].T + self.beta_is
        tmp = us @ alpha_is_u.T + beta_is_plus_alpha_is_times_x
        fs = T * torch.logsumexp((1/T)*tmp, dim=-1, keepdim=True)
        return fs

    @normalise_minimise
    def minimise_np(self, x, solver=cp.MOSEK):
        assert type(x) is np.ndarray
        assert len(x.shape) == 1
        n = self.n
        alpha_is_u = self.alpha_is[:, n:].detach().cpu().numpy()
        beta_is_plus_alpha_is_times_x = x @ self.alpha_is[:, 0:n].T.detach().cpu().numpy() + self.beta_is.detach().cpu().numpy()  # TODO
        self.parameters_cp[0].value = alpha_is_u
        self.parameters_cp[1].value = beta_is_plus_alpha_is_times_x
        if self.shift is not None:
            self.parameters_cp[2].value = self.forward(self.shift[0].reshape(1, self.n),
                                                       self.shift[1].reshape(1, self.m),).detach().cpu().numpy().reshape(1,)
        self.prob.solve(solver=solver)
        u = self.u_cp.value
        return u

    @normalise_minimise
    def minimise_tch(self, xs):
        assert type(xs) is torch.Tensor
        assert len(xs.shape) == 2
        d = xs.shape[0]
        n = self.n
        beta_is_plus_alpha_is_times_x = xs @ torch.t(self.alpha_is[:, 0:n]) + torch.t(self.beta_is)  # x A[:, 0:n].T + b.T (d x 1)
        alpha_is_u = self.alpha_is[:, n:]  # A[:, n:]
        if self.shift is not None:
            x_shift, u_shift = self.shift
            offset_value = self.forward(x_shift.reshape(1, self.n),
                                        u_shift.reshape(1, self.m)).reshape(1,)
            us, = self.cvxpylayer(alpha_is_u.repeat(d, 1, 1), beta_is_plus_alpha_is_times_x,
                                  offset_value.repeat(d, 1))
        else:
            us, = self.cvxpylayer(alpha_is_u.repeat(d, 1, 1), beta_is_plus_alpha_is_times_x)
        return us


class LSE(_LSE):
    def __init__(self, *args, x_shift=None, u_shift=None, **kwargs):
        """
        LSE considering shift
        """
        self.set_shift(x_shift, u_shift)
        super().__init__(*args, **kwargs)

    def forward(self, xs, us):
        if self.shift is None:
            fs = super().forward(xs, us)
        else:
            x_shift, u_shift = self.shift
            fs = super().forward(xs, us) - super().forward(x_shift.reshape(1, self.n), u_shift.reshape(1, self.m))
        return fs


class LSEPlus(LSE):
    def __init__(self, *args, act_output="relu", **kwargs):
        """
        LSE+
        """
        super().__init__(*args, **kwargs, act_output=act_output)

    def forward(self, xs, us):
        return F.relu(super().forward(xs, us))
