# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tuftelike']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3,<4']

setup_kwargs = {
    'name': 'matplotlib-tufte',
    'version': '1.0',
    'description': 'Tufte-style plots for matplotlib',
    'long_description': '<!--\nThis file is part of matplotlib-tufte, Tufte-style plots for matplotlib.\nhttps://gitlab.com/lemberger/matplotlib-tufte\n\nSPDX-FileCopyrightText: 2022 Thomas Lemberger <https://thomaslemberger.com>\n\nSPDX-License-Identifier: Apache-2.0\n-->\n# matplotlib-tufte\n\nmatplotlib-tufte is a python module\nto create Tufte-like plots with matplotlib.\n\nInspiration is drawn from *Edward Tufte: The Visual Display of Quantitative Data*.\n\n## Requirements\n\n- python >= 3.7\n- matplotlib\n\n## Examples\n\nSee [examples/Basic.ipynb](examples/Basic.ipynb) for some small examples of tuftelike plots.\n\n## Usage\n\nCreate your plots with matplotlib as usual.\nThen, run `tuftelike.adjust` with the x- and y-values of your plot to adjust it in-place.\n\n```\nimport matplotlib.pyplot as plt\nimport tuftelike\n\nxs, ys = [1, 2, 3, 4], [1, 4, 2, 3]\nplt.plot(xs, ys)\n\ntuftelike.adjust(xs, ys)\nplt.savefig("example.png")\n```\n\nTuftelike needs the x- and y-values because matplotlib does not store these internally.\nThe above code produces:\n\n![an example tuftelike plot](examples/simple.png).',
    'author': 'Thomas Lemberger',
    'author_email': 'lembergerth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/lemberger/matplotlib-tufte',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
