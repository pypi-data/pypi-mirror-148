# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandas_dash']

package_data = \
{'': ['*']}

install_requires = \
['dash>=2,<3', 'pandas>=1,<2']

setup_kwargs = {
    'name': 'pandas-dash',
    'version': '0.1.2',
    'description': 'Tools for working with Pandas, Plotly, and Dash.',
    'long_description': '# Pandas Dash\n\n![Python version](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue.svg)\n[![PyPI version](https://badge.fury.io/py/pandas-dash.svg)](https://pypi.org/project/pandas-dash/)\n[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/lucasjamar/pandas-dash/blob/main/LICENSE.md)\n\nTools for working with Pandas, Plotly, and Dash.\n\n[See examples](https://github.com/lucasjamar/pandas-dash/blob/main/examples/app.py)\n\n## Available extensions for `Dash`\n* `df.dash.to_dash_table()` for getting the `data` and `columns` for `dash_table` from a flat or multi-index `pd.DataFrame`.\n* `df.dash.to_options("my_column")` for creating `dcc.Dropdown` options from the column of a `pd.DataFrame`.\n* `df.dash.to_pivot_table()` for creating the date necessary for `dash_pivottable.PivotTable`.\n\n## Extensions for `Plotly` coming soon.',
    'author': 'lucas.jamar',
    'author_email': 'lucasjamar@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lucasjamar/pandas-dash',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
