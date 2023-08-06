# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['browsers']

package_data = \
{'': ['*']}

extras_require = \
{':sys_platform == "linux"': ['pyxdg>=0.27,<0.28'],
 ':sys_platform == "win32"': ['pywin32>=303,<304']}

setup_kwargs = {
    'name': 'pybrowsers',
    'version': '0.4.1',
    'description': 'Python library for detecting and launching browsers',
    'long_description': '<table>\n    <tr>\n        <td>License</td>\n        <td><img src=\'https://img.shields.io/pypi/l/pybrowsers.svg?style=for-the-badge\' alt="License"></td>\n        <td>Version</td>\n        <td><img src=\'https://img.shields.io/pypi/v/pybrowsers.svg?logo=pypi&style=for-the-badge\' alt="Version"></td>\n    </tr>\n    <tr>\n        <td>Github Actions</td>\n        <td><img src=\'https://img.shields.io/github/workflow/status/roniemartinez/browsers/Python?label=actions&logo=github%20actions&style=for-the-badge\' alt="Github Actions"></td>\n        <td>Coverage</td>\n        <td><img src=\'https://img.shields.io/codecov/c/github/roniemartinez/browsers/branch?label=codecov&logo=codecov&style=for-the-badge\' alt="CodeCov"></td>\n    </tr>\n    <tr>\n        <td>Supported versions</td>\n        <td><img src=\'https://img.shields.io/pypi/pyversions/pybrowsers.svg?logo=python&style=for-the-badge\' alt="Python Versions"></td>\n        <td>Wheel</td>\n        <td><img src=\'https://img.shields.io/pypi/wheel/pybrowsers.svg?style=for-the-badge\' alt="Wheel"></td>\n    </tr>\n    <tr>\n        <td>Status</td>\n        <td><img src=\'https://img.shields.io/pypi/status/pybrowsers.svg?style=for-the-badge\' alt="Status"></td>\n        <td>Downloads</td>\n        <td><img src=\'https://img.shields.io/pypi/dm/pybrowsers.svg?style=for-the-badge\' alt="Downloads"></td>\n    </tr>\n</table>\n\n# browsers\n\nPython library for detecting and launching browsers\n\n\n## Why?\n\nI recently wrote a snippet for detecting installed browsers in an OSX machine in \nhttps://github.com/mitmproxy/mitmproxy/issues/5247#issuecomment-1095337723 based on https://github.com/httptoolkit/browser-launcher\nand I thought this could be useful to other devs since I cannot find an equivalent library of `httptoolkit/browser-launcher` in Python\nand the known `webbrowser` standard library does not support arguments.\n\n## Installation\n\n```bash\npip install pybrowsers\n```\n\n## Features\n\n- Detect browser on OSX\n- Detect browser on Linux\n- Detect browser on Windows\n- Launch browser with arguments\n- Launch and get browser by version with wildcard support\n\n## Usage\n\n### Import\n\n```python\nimport browsers\n```\n\n### List all installer browsers\n\n```python\nimport browsers\n\nprint(list(browsers.browsers()))\n# [{\'browser_type\': \'chrome\', \'path\': \'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome\', \'display_name\': \'Google Chrome\', \'version\': \'100.0.4896.127\'}, {\'browser_type\': \'firefox\', \'path\': \'/Applications/Firefox.app/Contents/MacOS/firefox\', \'display_name\': \'Firefox\', \'version\': \'99.0.1\'}, {\'browser_type\': \'safari\', \'path\': \'/Applications/Safari.app/Contents/MacOS/Safari\', \'display_name\': \'Safari\', \'version\': \'15.4\'}, {\'browser_type\': \'opera\', \'path\': \'/Applications/Opera.app/Contents/MacOS/Opera\', \'display_name\': \'Opera\', \'version\': \'85.0.4341.60\'}, {\'browser_type\': \'msedge\', \'path\': \'/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge\', \'display_name\': \'Microsoft Edge\', \'version\': \'100.1185.22042050\'}]\n```\n\n### Get browser information\n\n```python\nimport browsers\n\nprint(browsers.get("chrome"))\n# {\'browser_type\': \'chrome\', \'path\': \'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome\', \'display_name\': \'Google Chrome\', \'version\': \'100.0.4896.127\'}\n```\n\n### Launch browser\n\n```python\nimport browsers\n\nbrowsers.launch("chrome")\n```\n\n### Launch browser with URL\n\n```python\nimport browsers\n\nbrowsers.launch("chrome", url="https://github.com/roniemartinez/browsers")\n```\n\n### Launch browser with arguments\n\n```python\nimport browsers\n\nbrowsers.launch("chrome", args=["--incognito"])\n```\n\n### Specifying version\n\nThe `get()` and `launch()` functions support specifying version in case multiple versions are installed.\nWildcard pattern is also supported.\n\n```python\nimport browsers\n\nprint(browsers.get("chrome", version="100.0.4896.127"))  # complete version\n# {\'browser_type\': \'chrome\', \'path\': \'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome\', \'display_name\': \'Google Chrome\', \'version\': \'100.0.4896.127\'}\n\nprint(browsers.get("chrome", version="100.*"))  # wildcard\n# {\'browser_type\': \'chrome\', \'path\': \'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome\', \'display_name\': \'Google Chrome\', \'version\': \'100.0.4896.127\'}\n\nbrowsers.launch("chrome", version="100.0.4896.127")  # complete version\nbrowsers.launch("chrome", version="100.*")  # wildcard\n```\n\n## References\n\n- [httptoolkit/browser-launcher](https://github.com/httptoolkit/browser-launcher)\n- [Desktop Entry Specification](https://specifications.freedesktop.org/desktop-entry-spec/latest/)\n- [Github: webbrowser.open incomplete on Windows](https://github.com/python/cpython/issues/52479#issuecomment-1093496412)\n- [Stackoverflow: Grabbing full file version of an exe in Python](https://stackoverflow.com/a/68774871/1279157)\n\n## Author\n\n- [Ronie Martinez](mailto:ronmarti18@gmail.com)\n',
    'author': 'Ronie Martinez',
    'author_email': 'ronmarti18@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/roniemartinez/browsers',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
