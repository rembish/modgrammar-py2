# -*- coding: utf-8 -*-
try:
    from setuptools import setup, Command
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()
    from setuptools import setup, Command

import os
import sys
from distutils import log

from pkg_utils import *

setup(
    name='modgrammar',
    version=pkg_version,
    url='http://code.google.com/p/modgrammar',
    download_url='http://pypi.python.org/pypi/modgrammar',
    license='BSD',
    author='Alex Stewart',
    author_email='alex@foogod.com',
    description='Modular grammar-parsing engine',
    long_description=pkg_readme,
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Topic :: Text Processing',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms='any',
    packages=['modgrammar'],
    test_suite='tests.all_tests',
    include_package_data=False,
    install_requires=[],
    #cmdclass=dict(build_sphinx=BuildSphinxCommand),
    command_options={
        'build_sphinx': dict(
            build_dir=('setup.py', 'build'),
        )
    },
)
