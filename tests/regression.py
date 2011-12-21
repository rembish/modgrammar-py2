import modgrammar
from modgrammar import *
from . import util

class TestIssue1 (util.TestCase):
  """
  Issue 1: Fails with traceback if matchtype="longest" or "shortest" and
  there's more than one longest/shortest match with the same length
  """

  def test_longest_samelength(self):
    grammar = OR('aaa', 'aaa')
    o = grammar.parser().parse_string('aaaa', matchtype='longest')

  def test_shortest_samelength(self):
    grammar = OR('aaa', 'aaa')
    o = grammar.parser().parse_string('aaaa', matchtype='shortest')

class TestIssue2 (util.TestCase):
  """
  Issue 2: NameError: global name 'GrammarDefError' is not defined (oops)
  """

  def test_grammardeferror(self):
    self.assertTrue(hasattr(modgrammar, "GrammarDefError"))
    with self.assertRaises(modgrammar.GrammarDefError):
      GRAMMAR(1)
