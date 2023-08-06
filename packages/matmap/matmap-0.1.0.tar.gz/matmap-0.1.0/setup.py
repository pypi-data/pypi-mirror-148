# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['matmap', 'matmap.qast_utils', 'matmap.transforms', 'matmap.tuning']

package_data = \
{'': ['*']}

install_requires = \
['cvxpy>=1.0.0,<2.0.0', 'exo-lang>=0.0.2,<0.0.3']

setup_kwargs = {
    'name': 'matmap',
    'version': '0.1.0',
    'description': 'MatMap: A Modular, Automatable, Tunable Mapper for Accelerator Programming',
    'long_description': '# Matmap: A Modular, Automatable, Tunable Mapper for Accelerator Programming\n\nA representation for higher-level transforms, currently targeting [EXO](https://github.com/ChezJrk/exo) code.\n\n## Setup\n\nThis has been extensively tested on Python 3.9.7. Python versions 3.7 and earlier are not supported as Exo requires several newer language features not available. If you are on a system with an outdated version of python, we recommend using [pyenv](https://github.com/pyenv/pyenv) to install a new version of pyenv.\n\n```\ngit clone https://github.com/gdinh/matmap.git\npython -m venv $HOME/.venv/matmap\nsource $HOME/.venv/matmap/bin/activate\npython -m pip install --upgrade pip\npython -m pip install -e ./matmap\n```\n\nFurther documentation and demo notebooks can be found in the docs directory.\n\n## Project status:\n\nWorking:\n- Tiling schedule (including automatic generation of tiles for projective nested loops)\n- Reordering schedule\n\nIn progress:\n- [GPTune](https://gptune.lbl.gov/) integration\n- [CoSA](https://github.com/ucb-bar/cosa) transform\n\nNext TODOs:\n- HBL autotiling for CNNs\n- Code specialization for variable sized bounds\n',
    'author': 'Grace Dinh',
    'author_email': 'dinh@berkeley.edu',
    'maintainer': 'Grace Dinh',
    'maintainer_email': 'dinh@berkeley.edu',
    'url': 'https://github.com/gdinh/matmap',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
