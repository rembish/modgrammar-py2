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

