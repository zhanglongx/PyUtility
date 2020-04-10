# coding: utf-8

from setuptools import setup

setup(
    name='vsadd',
    version='1.0',
    packages=['vsadd'],
    entry_points={
        'console_scripts': [
            'vsadd = vsadd.vs_add_project:main'
        ]}
)