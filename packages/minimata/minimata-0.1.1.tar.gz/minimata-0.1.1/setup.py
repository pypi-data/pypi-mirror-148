# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minimata']

package_data = \
{'': ['*']}

modules = \
['README', 'LICENSE']
install_requires = \
['graphviz>=0.20,<0.21']

setup_kwargs = {
    'name': 'minimata',
    'version': '0.1.1',
    'description': 'Minimata is a minimalist state-machine implementation.',
    'long_description': '# Minimata: minimalist state-machine in Python\n\nMiniata is a very small library to manage state-machines in Python.\n\nBecause it doesn\'t bundle a lot of features, it\'s pretty flexible.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install `minimata`.\n\n```bash\npip install minimata\n```\n\n## Why\n\nI needed a really simple implementations and didn\'t wanted to reach to heavier\nalternatives like [transitions](https://github.com/pytransitions/transitions).\n\n## Usage\n\nHere is an example:\n\n```python\nfrom minimata import StateMachine, skip_transition\n\nmodel_onboarding_state_machine = StateMachine("onboarding_state")\n\n@model_onboarding_state_machine.on("event", {"source_state": "destination_state"})\ndef callback(model: Model, param: bool = False, **kwargs):\n    if param:\n        print(model)\n\n@dataclass\nclass UserModel:\n    onboarding_state: str\n\nuser_model = UserModel(onboarding_state="source_state")\n\nmodel_onboarding_state_machine.trigger(\n    model=user_model,\n    event="event",\n    param=True,\n) # Executes callback (prints user_model) *THEN* update its state.\n```\n\n## Contributing\n\nWith a hundred line of code, it\'s possible to get there and customize this. It\'ll\nprobably make sense for you to copy-paste that code rather than to add it as a\ndependency.\n\nThat being said, pull-requests are welcome. It would be nice to polish the library,\nplease open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## Credits\n\nInspiration was heavily taken from the following projects.\n\n* [micro-machine](https://github.com/soveran/micromachine)\n* [transitions](https://github.com/pytransitions/transitions)\n\nMany thanks to their authors, maintainers, and contributors.\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Nicolas Zermati',
    'author_email': 'nicoolas25@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nicoolas25/minimata',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
