from __future__ import with_statement

import modgrammar
from tests import util

class TestIssue1(util.TestCase):
    """
    Issue 1: Fails with traceback if matchtype="longest" or "shortest" and
             there's more than one longest/shortest match with the same length
    """

    def test_longest_samelength(self):
        grammar = modgrammar.OR('aaa', 'aaa')
        o = grammar.parser().parse_string('aaaa', matchtype='longest')

    def test_shortest_samelength(self):
        grammar = modgrammar.OR('aaa', 'aaa')
        o = grammar.parser().parse_string('aaaa', matchtype='shortest')


class TestIssue2(util.TestCase):
    """
    Issue 2: NameError: global name 'GrammarDefError' is not defined (oops)
    """

    def test_grammardeferror(self):
        self.assertTrue(hasattr(modgrammar, "GrammarDefError"))
        with self.assertRaises(modgrammar.GrammarDefError):
            modgrammar.GRAMMAR(1)


class TestIssue4(util.TestCase):
    """
    Issue 4: Whitespace before EOF causes parse_lines to fail, even when parsing
             whitespace-consuming grammar (where it should work)
    """

    def test_whitespace_before_eof(self):
        grammar = modgrammar.GRAMMAR('A', whitespace=True)
        list(grammar.parser().parse_lines(["A "], eof=True))

