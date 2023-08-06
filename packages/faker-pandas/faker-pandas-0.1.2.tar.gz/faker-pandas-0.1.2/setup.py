# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['faker_pandas']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=13.6.0,<14.0.0', 'pandas>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'faker-pandas',
    'version': '0.1.2',
    'description': 'Adds Provider for Faker library to Generate randomized Pandas DataFrames',
    'long_description': "\n# Faker Pandas\n\n```py\nfrom faker import Faker\nfrom faker_pandas import PandasProvider\n\nfake = Faker()\nfake.add_provider(PandasProvider)\n\ncolgen = fake.pandas_column_generator()\n\ndf = fake.pandas_dataframe(\n    colgen.first_name('First Name', empty_value='', empty_ratio=.5),\n    colgen.last_name('Last Name'),\n    colgen.pandas_int('Age', 18, 80, empty_ratio=.2),\n    rows=7\n)\n\nprint(df)\n```\nOutput:\n```txt\n  First Name Last Name   Age\n1             Lawrence  72.0\n2       Lisa  Holloway   NaN\n3              Edwards  31.0\n4     Steven   Johnson  69.0\n5                Smith  66.0\n6     Monica     Lynch   NaN\n7     Edward     Brown  20.0\n```\n",
    'author': 'Sani',
    'author_email': 'sani@sani.love',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nitori/faker_pandas',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
