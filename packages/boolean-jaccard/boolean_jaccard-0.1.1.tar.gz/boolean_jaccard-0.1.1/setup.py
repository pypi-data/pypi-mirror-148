# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jaccard']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0', 'pandas>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'boolean-jaccard',
    'version': '0.1.1',
    'description': 'Jaccard metric calculations for boolean vectors',
    'long_description': '# boolean_jaccard\n\n[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)\n[![PyPI Version](https://img.shields.io/pypi/v/boolean_jaccard)](https://pypi.org/project/boolean_jaccard/)\n[![Python Versions](https://shields.io/pypi/pyversions/boolean_jaccard)](https://shields.io/pypi/pyversions/boolean_jaccard)\n[![CI/CD](https://github.com/IMS-Bio2Core-Facility/boolean_jaccard/actions/workflows/cicd.yaml/badge.svg)](https://github.com/IMS-Bio2Core-Facility/boolean_jaccard/actions/workflows/cicd.yaml)\n[![codecov](https://codecov.io/gh/IMS-Bio2Core-Facility/boolean_jaccard/branch/main/graph/badge.svg?token=2TGYX69U3N)](https://codecov.io/gh/IMS-Bio2Core-Facility/boolean_jaccard)\n[![Documentation Status](https://readthedocs.org/projects/boolean_jaccard/badge/?version=latest)](https://boolean_jaccard.readthedocs.io/en/latest/?badge=latest)\n[![Project Status: Active](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)\n[![Codestyle: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n\nCalculate Jaccard metrics for boolean values.\n\nThe source code lives on [github][github].\n\nThe documentation lives at [ReadTheDocs][readthedocs].\n\nThe project can be installed from [PyPI][pip].\n\n## Abstract\n\nThe code here represents a python implementation of the Jaccard package hosted\n[here][jaccard] by N. Chung. Its citation follows.\n\n### Citation\n\nChung, N., Miasojedow, B., Startek, M., and Gambin, A. "Jaccard/Tanimoto similarity test and estimation methods for biological presence-absence data" _BMC Bioinformatics_ **(2019)** 20(Suppl 15): 644. https://doi.org/10.1186/s12859-019-3118-5\n\n## Installation\n\nIt\'s a [PyPI][pip] package,\nso the pocess is pretty straightforward:\n\n```shell\npip install -U boolean_jaccard # for most recent version\npip install -U boolean_jaccard==0.0.1 # for a specific version\n```\n\nA list of all released versions can be found at our [tags][tags].\n\n### A Note on Version Numbers\n\n`boolean_jaccard` uses strict automated [semantic versioning][semver].\nAs such,\nwe guarantee bugfixes in path releases,\nbackwards compatible features in minor releases,\nand breaking changes in major releases.\nWe will endeavour to avoid breaking changes where possible,\nbut,\nshould they occur,\nthey will _**only**_ be in major releases.\n\n### Installing from Source\n\n```{important}\nMost users **will not need** these instructions.\n```\n\nIf you need to customise the code in some manner,\nyou\'ll need to install from source.\nTo do that,\neither clone the repository from github,\nor download one of our releases.\nFor full instructions,\nplease see our guide on [contributing](./contributing.md).\n\n\n## Contributing\n\nOpen-source software is only open-source becaues of the excellent community,\nso we welcome any and all contributions!\nIf you think you have found a bug,\nplease log a report in our [issues][issues].\nIf you think you can fix a bug,\nor have an idea for a new feature,\nplease see our guide on [contributing](./contributing.md)\nfor more information on how to get started!\nWhile here,\nwe request that you follow our [code of conduct](./coc.md)\nto help maintain a welcoming,\nrespectful environment.\n\n## Future Developments\n\n- [ ] Fully vectorise to improve performance.\n\n## Citations\n\nIf you use `boolean_jaccard` in your work,\nplease cite the following manuscripts:\n\n1. Chung, N., Miasojedow, B., Startek, M., and Gambin, A. "Jaccard/Tanimoto similarity test and estimation methods for biological presence-absence data" _BMC Bioinformatics_ **(2019)** 20(Suppl 15): 644. https://doi.org/10.1186/s12859-019-3118-5\n\n[github]: https://github.com/IMS-Bio2Core-Facility/boolean_jaccard "Source Code"\n[readthedocs]: http://boolean_jaccard.readthedocs.io/ "Documentation"\n[pip]: https://pypi.org/project/boolean_jaccard/ "PyPI Package"\n[jaccard]: https://github.com/ncchung/Jaccard\n[semver]: https://semver.org "Semantic Versioning"\n[tags]: https://github.com/IMS-Bio2Core-Facility/boolean_jaccard/releases "Releases"\n[issues]: https://github.com/IMS-Bio2Core-Facility/boolean_jaccard/issues "Issues"\n',
    'author': 'rbpatt2019',
    'author_email': 'rb.patterson.cross@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/IMS-Bio2Core-Facility/boolean_jaccard',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.11',
}


setup(**setup_kwargs)
