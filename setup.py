# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="yunbk",
    version='0.1.56',
    zip_safe=False,
    platforms='any',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    install_requires=['paramiko', 'sh', 'grandfatherson'],
    url="https://github.com/dantezhu/yunbk",
    license="MIT",
    author="dantezhu",
    author_email="zny2008@gmail.com",
    description="make backup easier",
)
