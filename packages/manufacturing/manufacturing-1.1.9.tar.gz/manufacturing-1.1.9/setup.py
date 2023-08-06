# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['manufacturing']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.3.0,<23.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'openpyxl>=3.0.9,<4.0.0',
 'pandas>=1.4.2,<2.0.0',
 'scipy>=1.7.0,<2.0.0',
 'xlrd>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'manufacturing',
    'version': '1.1.9',
    'description': 'Six-Sigma based analysis of manufacturing data',
    'long_description': "# Purpose\n\nTo provide analysis tools and metrics useful in manufacturing environments.\n\nI am slowly generating the documentation and, as that is maturing, I will begin to move information\nfrom this `readme.md` into that location.  If you don't find something here, head over to the\n[documentation](https://manufacturing.readthedocs.io/en/latest/).\n\n# Project Maturity\n\nEvery effort is being made to ensure that the results are accurate, but the user is ultimately\nresponsible for any resulting analysis.\n\nThe API should not be considered stable until v1.0 or greater.  Until then, breaking changes may\nbe released as different API options are explored.\n\nDuring the `v0.X.X` versioning, I am using the package in my own analyses in order to find any bugs.  Once\nI am reasonably satisfied that the package is feature complete, usable, and bug-free, I will break out\nthe `v1.X.X` releases.\n\n# Installation\n\nTo install from `pypi`:\n\n    pip install manufacturing\n\nTo install from source download and install using poetry:\n\n    poetry install\n\n# Usage\n\n## Visualizations with Jupyter Notebooks\n\nVisualizations work approximately as expected within a jupyter notebook.\n\n    data = np.random.normal(0, 1, size=30)  # generate some data\n    manufacturing.ppk_plot(data, lower_specification_limit=-2, upper_specification_limit=2)\n    \nThere is a sample jupyter notebook in the examples directory.\n\n## Cpk Visualization\n\nThe most useful feature of the `manufacturing` package is the visualization of Cpk.\nAs hinted previously, the `ppk_plot()` function is the primary method for display of\nCpk visual information.  First, get your data into a `list`, `numpy.array`, or \n`pandas.Series`; then supply that data, along with the `lower_control_limit` and \n`upper_control_limit` into the `ppk_plot()` function.\n\n    manufacturing.ppk_plot(data, lower_specification_limit=-2, upper_specification_limit=2)\n    \n![Screenshot](images/example3.png)\n\nIn this example, it appears that the manufacturing processes are not up to the task of \nmaking consistent product within the specified limits.\n\n## Zone Control Visualization\n\nAnother useful feature is the zone control visualization.\n\n    manufacturing.control_chart(data)\n\nThere are X-MR charts, Xbar-R charts, and Xbar-S charts available as well.  If you call the \n`control_chart()` function, the appropriate sample size will be selected and data grouped as\nthe dataset requires.  However, if you wish to call a specific type of control chart, use\n\n - `x_mr_chart`\n - `xbar_r_chart`\n - `xbar_s_chart`\n\n# RoadMap\n\nItems marked out were added most recently.\n\n - ...\n - ~~Add use github actions for deployment~~\n - ~~Transition to `poetry` for releases~~\n - ~~Add `I-MR Chart` (see `examples/imr_chart.py`)~~\n - ~~Add `Xbar-R Chart` (subgroups between 2 and 10)~~\n - ~~Add `Xbar-S Chart` (subgroups of 11 or more)~~\n - Back with testing\n\n# Gallery\n\n![Ppk example](images/ppk-chart-example.png)\n\n![Cpk example](images/cpk-by-subgroups.png)\n\n![X-MR Chart](images/xmr-chart.png)\n\n![Xbar-R Chart](images/xbar-r-chart.png)\n\n![Xbar-S Chart](images/xbar-s-chart.png)\n",
    'author': 'Jason R. Jones',
    'author_email': 'slightlynybbled@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
