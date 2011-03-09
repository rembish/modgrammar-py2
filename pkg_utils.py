# This file just contains some handy routines for extracting version/readme
# info from the appropriate files for use in setup.py and documentation
# generation, so they don't have to be specified multiple places.

import re
import os.path

__all__ = ['pkg_base_dir', 'pkg_version', 'pkg_version_short', 'pkg_readme']

class PkgUtilsError (Exception):
  pass

def get_base_dir():
  dir = os.path.abspath(__file__)
  while not os.path.exists(os.path.join(dir, 'setup.py')):
    parent_dir = os.path.dirname(dir)
    if parent_dir == dir:
      raise PkgUtilsError("Cannot find setup.py!")
    dir = parent_dir
  return dir

ver_line_re = re.compile("Version ([0-9]+[.][0-9]+[^: ]*)")
shortver_re = re.compile("([0-9]+[.][0-9]+)")

def get_changelog_version():
  version = ""
  with open(os.path.join(pkg_base_dir, 'CHANGELOG')) as f:
    for line in f:
      m = ver_line_re.match(line)
      if m:
        version = m.group(1)
        break
  if not version:
    raise PkgUtilsError("Unable to extract version number from CHANGELOG")
  short_version = shortver_re.match(version).group(1)
  return (short_version, version)

def get_readme():
  try:
    text = open(os.path.join(pkg_base_dir, 'README')).read()
  except IOError as e:
    if e.errno == 2:
      # No README file found.
      text = ''
    else:
      raise
  return text.strip()

###############################################################################

pkg_base_dir = get_base_dir()
pkg_version_short, pkg_version = get_changelog_version()
pkg_readme = get_readme()
