#!/usr/bin/env python
# coding: utf-8
import pathlib
from setuptools import setup,find_packages
path = pathlib.Path(__file__).parent
README = (path / "README.md").read_text(encoding='utf-8')

setup(
    name='deatool',
    version='3.0.0',
    author='WANGY',
    License = "GNU AGPLv3",
    author_email='wangy_prince@126.com',
    long_description = README,
    long_description_content_type = 'text/markdown',
    url='https://github.com/DEATien',
    description=u'Data envelopment analysis efficiency calculator',
    packages=find_packages(),
    python_requires="<3.10" ,
    install_requires=['pandas','Pyside2','numpy','openpyxl','mip'],
    classifiers={
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
    },
    entry_points = {
        "console_scripts":
            "deatool=deatool.__main__:run",
    }

)