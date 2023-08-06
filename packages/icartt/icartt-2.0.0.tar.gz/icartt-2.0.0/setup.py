# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['icartt']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19']

setup_kwargs = {
    'name': 'icartt',
    'version': '2.0.0',
    'description': 'ICARTT format reader and writer',
    'long_description': "# icartt\n\n``icartt`` is an ICARTT format reader and writer\n\n## Documentation\n\nPlease have a look at docs/source/usage.rst for usage examples. Full documentation is in preparation.\n\n## Contributing\n\nWe are looking forward to receiving your [new issue report](https://mbees.med.uni-augsburg.de/gitlab/mbees/icartt_pypackage/-/issues/new).\n\nIf you'd like to contribute source code directly, please [create a fork](https://mbees.med.uni-augsburg.de/gitlab/mbees/icartt_pypackage),\nmake your changes and then [submit a merge request](https://mbees.med.uni-augsburg.de/gitlab/mbees/icartt_pypackage/-/merge_requests/new) to the original project.\n\n\n## Installation of the development version\n\nClone this repository / or your fork and install. We use [poetry](https://python-poetry.org/) for packaging, which needs to be installed.\n\n```\ngit clone https://mbees.med.uni-augsburg.de/gitlab/mbees/icartt_pypackage.git or <URL of your fork>\ncd icartt_pypackage\npoetry install\npoetry shell\n```\n\n# Changelog\n\n## 2.0.0 (2022-04-28)\n\n- Compatible with ICARTT v2 standard\n- Formats 1001 and 2110\n- Complete internal overhaul\n\n## 1.0.0 (2017-12-19)\n\n- Peer-reviewed version to be published in Knote et al., GMD\n\n## 0.1.0 (2017-08-12)\n\n- Initial release\n",
    'author': 'Christoph Knote',
    'author_email': 'christoph.knote@med.uni-augsburg.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://mbees.med.uni-augsburg.de/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
