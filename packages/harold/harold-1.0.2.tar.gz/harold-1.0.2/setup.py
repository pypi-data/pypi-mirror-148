# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['harold', 'harold.tests']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.0,<4.0.0', 'scipy>=1.8.0,<2.0.0', 'tabulate>=0.8.9,<0.9.0']

setup_kwargs = {
    'name': 'harold',
    'version': '1.0.2',
    'description': 'An open-source systems and controls toolbox for Python3.',
    'long_description': "|License| |ReadTheDocs| |Downloads|\n\nharold\n======\n\nA control systems package for Python>=3.8.\n\nIntroduction\n============\n\nThis package is written with the ambition of providing a full-fledged control\nsystems software that serves a control engineer/student/researcher with complete\naccess to the source code with permissive rights (see ``LICENSE`` file). \nMoreover, via working with a proper high-level computer programming language\nmany proprietary software obstacles are avoided and users can incorporate this\npackage into their workflow in any way they see fit.\n\nQuick Reference and Documentation\n---------------------------------\n\nThe documentation is online at `ReadTheDocs`_. A brief tutorial about the basics\ncan be found under the notebooks folder to see ``harold`` in action.\n\nRoadmap\n-------\n\nThe items that are in the pipeline and what possibly lies ahead is enumerated\nin our `roadmap <https://github.com/ilayn/harold/wiki/harold-roadmap>`_.\n\nUseful Links\n------------\n\n- There is already an almost-matured control toolbox which is led by\n  Richard Murray et al. (`click for the Github page`_) and it can perform\n  already most of the essential tasks. Hence, if you want to have\n  something that resembles the basics of matlab control toolbox, you should give\n  it a try. However, it is somewhat limited to SISO tools and also relies on\n  SLICOT library which can lead to installation hassle and/or licensing\n  problems for nontrivial tasks.\n\n- You can also use the tools available in SciPy ``signal`` module for basics\n  of LTI system manipulations. SciPy is a powerful all-purpose scientific\n  package. This makes it extremely useful however admittedly every discipline\n  has a limited presence hence the limited functionality. If you are looking\n  for a quick LTI system manipulation and don't want to install yet another\n  package, then it might be the tool for you.\n\n- Instead, if you are interested in robust control you probably would\n  appreciate the `Skogestad-Python`_ project. They are replicating the\n  code parts of the now-classic book completely in Python. Awesome!\n\nHelp Wanted!\n------------\n\nIf you are missing out a feature, or found a bug, get in contact. Such\nreports and PR submissions are more than welcome!\n\nContact\n--------\n\nIf you have questions/comments feel free to shoot one to\n``harold.of.python@gmail.com`` or join the Gitter chatroom.\n\n.. _click for the Github page: https://github.com/python-control/python-control\n.. _ReadTheDocs: http://harold.readthedocs.org/en/latest/\n.. _Skogestad-Python: https://github.com/alchemyst/Skogestad-Python\n\n.. |License| image:: https://img.shields.io/github/license/mashape/apistatus.svg\n   :target: https://github.com/ilayn/harold/blob/master/LICENSE\n.. |ReadTheDocs| image:: https://readthedocs.org/projects/harold/badge/?version=latest\n    :target: http://harold.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n.. |Downloads| image:: http://pepy.tech/badge/harold\n    :target: https://pepy.tech/project/harold\n    :alt: Download Counts\n",
    'author': 'Ilhan Polat',
    'author_email': 'ilhanpolat@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
