# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['diffql', 'diffql.agents', 'diffql.envs']

package_data = \
{'': ['*'], 'diffql': ['config/*', 'config/agents/*', 'config/envs/*']}

install_requires = \
['Mosek>=9.3,<9.4',
 'PyYAML>=6.0,<6.1',
 'cvxpy>=1.2,<1.3',
 'cvxpylayers>=0.1,<0.2',
 'gym>=0.22,<0.23',
 'numpy>=1.22,<1.23',
 'scipy>=1.8,<1.9',
 'torch>=1.11,<1.12',
 'wandb>=0.12,<0.13']

setup_kwargs = {
    'name': 'diffql',
    'version': '0.2.1',
    'description': 'Differentiable Q-learning (DiffQL) for continuous-action deep reinforcement learning',
    'long_description': None,
    'author': 'Jinrae Kim',
    'author_email': 'kjl950403@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
