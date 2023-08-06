# Matmap: A Modular, Automatable, Tunable Mapper for Accelerator Programming

A representation for higher-level transforms, currently targeting [EXO](https://github.com/ChezJrk/exo) code.

## Setup

This has been extensively tested on Python 3.9.7. Python versions 3.7 and earlier are not supported as Exo requires several newer language features not available. If you are on a system with an outdated version of python, we recommend using [pyenv](https://github.com/pyenv/pyenv) to install a new version of pyenv.

```
git clone https://github.com/gdinh/matmap.git
python -m venv $HOME/.venv/matmap
source $HOME/.venv/matmap/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ./matmap
```

Further documentation and demo notebooks can be found in the docs directory.

## Project status:

Working:
- Tiling schedule (including automatic generation of tiles for projective nested loops)
- Reordering schedule

In progress:
- [GPTune](https://gptune.lbl.gov/) integration
- [CoSA](https://github.com/ucb-bar/cosa) transform

Next TODOs:
- HBL autotiling for CNNs
- Code specialization for variable sized bounds
