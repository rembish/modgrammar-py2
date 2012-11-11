# -*- coding: utf-8 -*-
try:
    from setuptools import setup, Command
except ImportError:
    import distribute_setup

    distribute_setup.use_setuptools()
    from setuptools import setup, Command

from pkg_utils import *

setup(
    name='modgrammar-py2',
    version=pkg_version,
    url='http://code.google.com/p/modgrammar',
    download_url='https://github.com/don-ramon/modgrammar-py2',
    license='BSD',
    author='Alex Stewart, Aleksey Rembish',
    author_email='alex@foogod.com, alex@rembish.ru',
    description='Modular grammar-parsing engine (Python 2.6+ / Python 3.x)',
    long_description=pkg_readme,
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
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
    command_options={
        'build_sphinx': dict(
            build_dir=('setup.py', 'build'),
        )
    },
)
