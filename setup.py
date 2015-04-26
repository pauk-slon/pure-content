# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='pure_content',
    version='0.0.0',
    description='Selects the main content of a web page',
    author='Dmitry Kolyagin',
    author_email='dmitry.kolyagin@gmail.com',
    packages=['pure_content'],
    url='https://github.com/pauk-slon/pure-content',
    install_requires=[
        'beautifulsoup4 >= 4.3.2',
        'lxml >= 3.4.3',
    ],
    entry_points={
        'console_scripts': ['purify_page = pure_content.main:main'],
    },
    tests_require=['flake8'],
)
