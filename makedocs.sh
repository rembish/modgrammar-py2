#!/bin/bash
#
# Gemnerate the current docs, zip them up, and put both the zipped and unzipped
# versions in the right locations of the doc repository.
#
# After running this, all that should be needed to push the new documentation
# to the official location is to cd into the doc repo working directory,
# 'hg commit', and then 'hg push'
#
# This assumes that the modgrammar doc repository is checked out under the
# following path:
docrepo=../modgrammar.doc

set -e
docrepo=$(cd "$docrepo" && pwd) # fully-qualify the path
version=$(python3 -c 'from pkg_utils import *; print(pkg_version_short)')
if [[ -z "$version" ]]; then
  echo "Error: Unable to determine package version."
  exit 1
fi

doc_dir="$docrepo/$version"
doc_zip="$docrepo/modgrammar-doc-$version.zip"

python3 setup.py build_sphinx
cd build
cp -a html "modgrammar-$version"
rm -f "$doc_zip" && zip -9 -r "$doc_zip" "modgrammar-$version"
rm -rf "$doc_dir" && mv "modgrammar-$version" "$doc_dir"
cd "$docrepo"
hg add "$doc_dir" "$doc_zip"

hg status | grep -v '^[AM]'
