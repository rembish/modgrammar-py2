#!/bin/sh

python3 setup.py sdist build_sphinx register upload upload_docs
