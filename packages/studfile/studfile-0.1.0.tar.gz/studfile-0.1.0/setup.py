# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['studfile']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'calligraphy-scripting>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['stud = studfile.main:main']}

setup_kwargs = {
    'name': 'studfile',
    'version': '0.1.0',
    'description': 'A simplified tool for making easy-to-use build scripts',
    'long_description': '# Stud\n\n## Example Studfile.yaml\n\n```yaml\ntest: \n  help: "Run test commands"\n  options:\n    - name: -m,--message\n      default: Hello world\n      nargs: \'?\'\n      required: true\n    - name: foobar\n  cmd: |\n    echo "{foobar}"\n    \n    for foo in ["bar", "baz"]:\n      print(f"{message}: {foo}")\n```\n',
    'author': 'John Carter',
    'author_email': 'jfcarter2358@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jfcarter2358/stud',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
