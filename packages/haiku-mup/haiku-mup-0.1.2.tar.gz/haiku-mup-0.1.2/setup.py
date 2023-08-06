# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['haiku_mup']

package_data = \
{'': ['*']}

install_requires = \
['dm-haiku>=0.0.6,<0.0.7', 'jax>=0.3.7,<0.4.0', 'optax>=0.1.2,<0.2.0']

setup_kwargs = {
    'name': 'haiku-mup',
    'version': '0.1.2',
    'description': 'A simple port of μP  to Haiku/JAX.',
    'long_description': '# MUP for Haiku\n\nThis is a (very preliminary) port of Yang and Hu et al.\'s [μP repo](https://github.com/microsoft/mup) to Haiku and JAX. It\'s not feature complete, and I\'m very open to suggestions on improving the usability.\n\n## Installation\n\n```\npip install haiku-mup\n```\n\n## Learning rate demo\nThese plots show the evolution of the optimal learning rate for a 3-hidden-layer MLP on MNIST, trained for 10 epochs (5 trials per lr/width combination).\n\nWith standard parameterization, the learning rate optimum continues changing as the width increases:\n\n<img src="https://github.com/davisyoshida/haiku-mup/blob/master/figures/mlp_sp.png?raw=True" width="500" />\n\n\nWith μP, the learning rate optimum stabilizes as width increases:\n\n<img src="https://github.com/davisyoshida/haiku-mup/blob/master/figures/mlp.png?raw=True" width="500" />\n\n## Usage\n```python\nfrom functools import partial\n\nimport jax\nimport jax.numpy as jnp\nimport haiku as hk\nfrom optax import adam, chain\n\nfrom haiku_mup import apply_mup, Mup, Readout\n\nclass MyModel(hk.Module):\n    def __init__(self, width, n_classes=10):\n        super().__init__(name=\'model\')\n        self.width = width\n        self.n_classes = n_classes\n\n    def __call__(self, x):\n        x = hk.Linear(self.width)(x)\n        x = jax.nn.relu(x)\n        return Readout(2)(x) # 1. Replace output layer with Readout layer\n\ndef fn(x, width=100):\n    with apply_mup(): # 2. Modify parameter creation with apply_mup()\n        return MyModel(width)(x)\n\nmup = Mup()\n\ninit_input = jnp.zeros(123)\nbase_model = hk.transform(partial(fn, width=1))\n\nwith mup.init_base(): # 3. Use this context manager when initializing the base model\n    hk.init(fn, jax.random.PRNGKey(0), init_input) \n\nmodel = hk.transform(fn)\n\nwith mup.init_target(): # 4. Use this context manager when initializng the target model\n    params = model.init(jax.random.PRNGKey(0), init_input)\n\nmodel = mup.wrap_model(model) # 5. Modify your model with Mup\n\noptimizer = optax.adam(3e-4)\noptimizer = mup.wrap_optimizer(optimizer, adam=True) # 6. Use wrap_optimizer to get layer specific learning rates\n\n# Now the model can be trained as normal\n```\n\n### Summary\n1. Replace output layers with `Readout` layers\n2. Modify parameter creation with the `apply_mup()` context manager\n3. Initialize a base model inside a `Mup.init_base()` context\n4. Initialize the target model inside a `Mup.init_target()` context\n5. Wrap the model with `Mup.wrap_model`\n6. Wrap optimizer with `Mup.wrap_optimizer`\n',
    'author': 'Davis Yoshida',
    'author_email': 'dyoshida@ttic.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
