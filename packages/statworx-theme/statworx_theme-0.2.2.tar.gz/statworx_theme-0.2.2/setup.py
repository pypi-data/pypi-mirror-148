# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['statworx_theme']

package_data = \
{'': ['*'], 'statworx_theme': ['styles/*']}

install_requires = \
['seaborn>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'statworx-theme',
    'version': '0.2.2',
    'description': 'A color theme for matplotlib using the offical statworx design',
    'long_description': '# Statworx Theme\n\nA color theme plugin for the [matplotlib](https://matplotlib.org/) library and all its derivatives, which automatically applies the official statworx color theme.\nThis package also registers commonly used [color maps](https://matplotlib.org/stable/tutorials/colors/colormaps.html) for use in presentations.\n\n<center>\n    <img src="./docs/assets/sample.png" width="400" />\n</center>\n\n## Quick Start\n\nSimply install a module with `pip` by using the following command.\n\n```console\npip install statworx-theme\n```\n\nTo apply the style, you must call the `apply_style` function by typing:\n\n```python\nfrom statworx_theme import apply_style\napply_style()\n```\n\n## Gallery\n\n<!-- TODO: Add link -->\nWe have an extensive gallery of figures using the statworx theme. You can see them [here](abc).\n',
    'author': 'An Hoang',
    'author_email': 'an.hoang@statworx.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.9,<3.9.0',
}


setup(**setup_kwargs)
