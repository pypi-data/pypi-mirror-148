#!/usr/bin/env python
# coding: utf-8
import pathlib
from setuptools import setup,find_packages
path = pathlib.Path(__file__).parent
README = (path / "README.md").read_text(encoding='utf-8')

setup(
    name='deatool',
    version='1.5',
    author='WANGY',
    LICENSE = "GNU AGPLv3",
    author_email='wangy_prince@126.com',
    long_description = README,
    long_description_content_type = 'text/markdown',
    url='https://github.com/DEATien',
    description=u'Data envelopment analysis efficiency calculator',
    packages=find_packages(),
    python_requires="<3.10" ,
    install_requires=['pandas','Pyside2','numpy','openpyxl','pyomo','gurobipy'],
    entry_points = {
        "consle_scripts":
            "rundea=deatool.__main__:main",
    }

)