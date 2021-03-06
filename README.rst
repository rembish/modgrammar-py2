.. image:: https://api.travis-ci.org/rembish/modgrammar-py2.png

Modgrammar is a general-purpose library for constructing language parsers and
interpreters using context-free grammar definitions in Python. Language
parsing rules (grammars) can be defined using standard Python syntax, and then
used to parse and validate input strings or files into meaningful data
structures. Possible applications range from simple input validation, to
complex expression evaluation, to full-fledged programming language parsing for
compilers or interpreters.

Documentation: http://rembish.github.com/modgrammar-py2
Parent Project: http://code.google.com/p/modgrammar

Some features include:

* Pure-Python cross-platform design.
* Grammar definitions are created using standard Python syntax.
* Supports arbitrarily complex grammars, including recursion.
* Defining a grammar automatically creates a working parser in the process (no
  compilation steps or lengthy startup times).
* Parse results contain full parse-tree information, including heirarchical
  tokenization of the input.
* Parse result objects can be given custom methods and behaviors as part of the
  grammar definition, producing rich data objects.
* Modular grammar design supports distributing grammars as python library
  modules, combining grammars from multiple sources into larger grammars, and
  even parameterized grammar definitions.
* Python 2.6+, 3.x support
