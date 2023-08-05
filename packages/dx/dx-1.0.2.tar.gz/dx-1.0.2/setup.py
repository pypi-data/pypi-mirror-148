# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dx']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=8.2.0,<9.0.0', 'pandas>=1.3.5,<2.0.0']

setup_kwargs = {
    'name': 'dx',
    'version': '1.0.2',
    'description': 'Python wrapper for Data Explorer',
    'long_description': "# dx\n\nA Pythonic Data Explorer.\n\n## Install\n\nFor Python 3.8+:\n```\npip install dx>=1.0.0\n```\n\n## Usage\n\nThe `dx` library allows for enabling/disabling DEX media type visualization with `dx.enable()` and `dx.display(data)` by setting a custom `IPython` formatter.\n\n```python\nimport dx\n\ndx.enable()\n```\n\n### Example\n\n```python\nimport pandas as pd\n\n# load randomized number/bool/string data\ndf = pd.read_csv('examples/sample_data.csv')\ndx.display(df)\n```\n\nPass `index=True` to visualize the `.index` values of a dataframe as well as the column/row values:\n```python\ndx.display(df, index=True)\n```\n\nIf you only wish to display a certain number of rows from the dataframe, use\na context and specify the max rows (if set to None, all rows are used):\n\n```python\n# To use the first 13 rows for visualization with dx\nwith pd.option_context('display.max_rows', 13):\n  dx.display(df)\n```\n\n## Develop\n\n```\ngit clone https://github.com/noteable-io/dx\ncd ./dx\npip install -e .\n```\n\n\n\n## Code of Conduct\n\nWe follow the noteable.io code of conduct.\n\n## LICENSE\n\nSee [LICENSE.md](LICENSE.md).",
    'author': 'Dave Shoup',
    'author_email': 'dave.shoup@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://app.noteable.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
