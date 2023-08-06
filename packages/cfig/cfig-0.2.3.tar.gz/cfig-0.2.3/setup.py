# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfig', 'cfig.sample', 'cfig.sources', 'cfig.tests']

package_data = \
{'': ['*']}

install_requires = \
['lazy-object-proxy>=1.7.1,<2.0.0']

extras_require = \
{'cli': ['click>=8.1.2,<9.0.0', 'colorama>=0.4.4,<0.5.0']}

setup_kwargs = {
    'name': 'cfig',
    'version': '0.2.3',
    'description': 'A configuration manager for Python',
    'long_description': '# cfig\n\nA configuration manager for Python \n\n\\[ [**Example**](https://github.com/Steffo99/cfig/tree/main/cfig/sample) | [**Documentation**](https://cfig.readthedocs.io/) | [**PyPI**](https://pypi.org/project/cfig/) \\]\n\n```python\nimport cfig\n\nconfig = cfig.Configuration()\n\n@config.required()\ndef SECRET_KEY(val: str) -> str:\n    """Secret string used to manage HTTP session tokens."""\n    return val\n\nif __name__ == "__main__":\n    config.cli()\n```\n\n```python\nfrom mypackage.mycfig import SECRET_KEY\n\nprint(f"My SECRET_KEY is: {SECRET_KEY}")\n```\n\n```console\n$ python -m mypackage.mycfig\n===== Configuration =====\n\nSECRET_KEY    → Required, but not set.\nSecret string used to manage HTTP session tokens.\n\n===== End =====\n```\n',
    'author': 'Stefano Pigozzi',
    'author_email': 'me@steffo.eu',
    'maintainer': 'Stefano Pigozzi',
    'maintainer_email': 'me@steffo.eu',
    'url': 'https://github.com/Steffo99/cfig',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
