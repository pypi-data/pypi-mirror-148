![Tests](https://github.com/joelee2012/gitlab-branch/workflows/Tests/badge.svg?branch=main)
![CodeQL](https://github.com/joelee2012/gitlab-branch/workflows/CodeQL/badge.svg?branch=main)
[![Coverage Status](https://coveralls.io/repos/github/joelee2012/gitlab-branch/badge.svg?branch=main)](https://coveralls.io/github/joelee2012/gitlab-branch?branch=main)
[![codecov](https://codecov.io/gh/joelee2012/gitlab-branch/branch/main/graph/badge.svg?token=YGM4CIB149)](https://codecov.io/gh/joelee2012/gitlab-branch)
![PyPI](https://img.shields.io/pypi/v/gitlab-branch)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gitlab-branch)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/gitlab-branch)
[![Documentation Status](https://readthedocs.org/projects/gitlab-branch/badge/?version=latest)](https://gitlab-branch.readthedocs.io/en/latest/?badge=latest)
![GitHub](https://img.shields.io/github/license/joelee2012/gitlab-branch)

# Manage branch for gitlab project

## Installation

from pypi
```sh
python3 -m pip install gitlab-branch
```
or install from source

```sh
git clone git@github.com:joelee2012/gitlab-branch.git
python3 -m pip install gitlab-branch
```

## Usage
```sh
$ gitlab-branch -h
usage: gitlab-branch [-h] {create,delete,list,protect,unprotect} ...

manage branch for gitlab project

optional arguments:
  -h, --help            show this help message and exit

subcommands:
  the following commands are supported

  {create,delete,list,protect,unprotect}
    create              create branch
    delete              delete branch
    list                list branch
    protect             protect branch
    unprotect           unprotect branch
```