# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyflowdroid']

package_data = \
{'': ['*'], 'pyflowdroid': ['sources_sinks/*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'progressbar>=2.5,<3.0',
 'typer>=0.4.1,<0.5.0']

setup_kwargs = {
    'name': 'pyflowdroid',
    'version': '0.1.0',
    'description': 'Python wrapper to use FlowDroid APK analyzer.',
    'long_description': "# PyFlowDroid\n\nPython wrappers for FlowDroid Apk analyzer. This project was built with two \ngoals in mind:\n\n1. Automate the creation of a FlowDroid environment out-of-the-box\n2. Allow the usage of FlowDroid from Python code \n\n## Installation\n\n### Prerequisites \n\nMake sure you have:\n\n1. A working version of [java](https://www.java.com/en/download/help/download_options.html) \n   in the PATH of your environment.\n2. A working version of [python](https://www.python.org/downloads/) in the PATH \n   of your environment.\n3. A working version of [git](https://git-scm.com/downloads) in the PATH of your \n   environment.\n\n### Installing pyFlowDroid dependencies\n\nYou can install it with [pip](https://pip.pypa.io/en/stable/installation/) by:\n\n```\n$ pip install pyflowdroid\n```\n### Download FlowDroid and its dependencies\n\nThis step will download and install FlowDroid and the required resources to use\nit:\n\n```\n$ python -m pyflowdroid install\n```\n\n## Usage\n\nThere are two ways in which you can use pyflowdroid: As a command line tool\nor as a Python library.\n\n### Using pyflowdroid from the command line\n\nThe main advantage of using pyflowdroid as a command line tool over using\nFlowDroid directly is the automatic gathering of resources required to \nexecute the flow analysis. pyflowdroid comes bundled with all the required \nresources to allow a quick analysis of apk files.\n\nTo analyze an .apk file with the default pyflowdroid setup, just run:\n\n```\n$ python -m pyflowdroid analyze path/to/file.apk\n```\n\nSimilarly, you can perform a flow analysis on all the apks inside a folder:\n\n```\n$ python -m pyflowdroid analyze path/to/folder/\n```\n\nThis should store raw FlowDroid logs for each analyzed apk and then show a \ngeneral report like the following:\n\n```\n################################################################################\n#                              PYFLOWDROID REPORT                              #\n################################################################################\nAnalized: 5\nLeaks found: 2\n\nLeaky apps:\n - 'path/to/folder/app1.apk'\n - 'path/to/folder/app3.apk'\n```\n\nIf you want to get some test apks, pyflowdroid includes a download function\nto fetch apks from a given supplier. Current available supplier are:\n\n- [cubapk.com](https://cubapk.com/)\n\nTo fetch apks from a supplier, just run:\n\n```\n$ python -m pyflowdroid download supplier_name\n```\n\n### Using pyflowdroid as a Python library\n\n[Comming Soon]\n\n## Contributing to pyflowdroid\n\nIf you want to add any features to pyflowdroid you will need to get a \ndevelopment enviroment.\n\n### Fetching the project source code\n\nYou can clone the github repository by executing:\n\n```\n$ git clone https://github.com/gvieralopez/pyFlowDroid\n$ cd pyFlowDroid\n```\n\n### Installing pyFlowDroid dependencies\n\nYou can install them with [poetry](https://python-poetry.org/docs/#installation)\n by executing:\n\n```\n$ poetry shell\n$ poetry install\n$ poetry build\n```\n### Download FlowDroid and its dependencies\n\nThis step will download and install FlowDroid. After doing this you can use \nFlowDroid with or without pyFlowDroid wrappers.\nSimply run:\n\n```\n$ python -m pyflowdroid install\n```\n\n### Making your changes appear in the project\n\nJust make a Pull Request.\n\n### Run tests:\n\n```\n$ pytest\n```\n\n### Type checking:\n\n```\n$ mypy\n```\n\n### Code style:\n\n```\n$ flake8\n```",
    'author': 'Gustavo Viera López',
    'author_email': 'gvieralopez@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gvieralopez/pyFlowDroid',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
