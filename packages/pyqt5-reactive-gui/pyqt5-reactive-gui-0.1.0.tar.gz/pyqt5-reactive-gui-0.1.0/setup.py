# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyqt5_reactive_gui']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5-Qt5==5.15.2',
 'PyQt5-sip==12.9.1',
 'PyQt5==5.14.1',
 'jsonpickle>=2.1.0,<3.0.0',
 'opencv-python>=4.5.5,<5.0.0']

setup_kwargs = {
    'name': 'pyqt5-reactive-gui',
    'version': '0.1.0',
    'description': 'PyQT5 reactive GUI',
    'long_description': None,
    'author': 'Jonas Frey',
    'author_email': 'jonas.immanuel.frey@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
