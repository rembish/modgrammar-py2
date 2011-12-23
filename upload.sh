#!/bin/sh
#
# Build a new version of the modgrammar package and upload it (and the docs) to
# PyPI.

python3 setup.py sdist build_sphinx register upload upload_docs
