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

class BuildSphinxCommand (Command):
    description = "build Sphinx-based documentation"
    user_options = [
        ('sphinx-cmd=', None, "command to build sphinx docs [default: sphinx-build]"),
        ('sphinx-dir=', None, "source directory for sphinx docs [default: sphinx]"),
    ]

    def initialize_options(self):
        self.sphinx_cmd = 'sphinx-build'
        self.sphinx_dir = 'sphinx'
        self.build_base = None

    def finalize_options(self):
        if self.build_base is None:
            build = self.get_finalized_command('build')
            self.build_base = build.build_base

    def run(self):
        html_cmd = '{sphinx_cmd} -b html -d {build_base}/doctrees {sphinx_dir} {build_base}/html'
        os.system(html_cmd.format(self.__dict__))


setup(
    name='modgrammar',
    version=pkg_version,
    url='http://code.google.com/modgrammar',
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
