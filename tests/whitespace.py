import unittest
import sys
from modgrammar import *
from modgrammar import OR_Operator
from modgrammar.util import RepeatingTuple
from . import util

# These tests simply verify that the grammar_whitespace attribute gets set
# correctly on all forms of grammar constructs when they're created.  Actual
# testing of whether each form of grammar actually deals with whitespace
# correctly on parsing should be tested in the basic_grammar tests.

class G_Default (Grammar):
  grammar = (ONE_OR_MORE('A'), 'B')

class G_Default_True (Grammar):
  grammar = (ONE_OR_MORE('A'), 'B')
  grammar_whitespace = True

class G_Default_False (Grammar):
  grammar = (ONE_OR_MORE('A'), 'B')
  grammar_whitespace = False

default_grammars = (
  ("G_Default", G_Default, True),
  ("G_Default_True", G_Default_True, True),
  ("G_Default_False", G_Default_False, False),
  ("GRAMMAR('A', 'B')", GRAMMAR('A', 'B'), True),
  ("G('A', 'B')", G('A', 'B'), True),
  ("REPEAT(L('A'))", REPEAT(L('A')), True),
  ("OPTIONAL(L('A'))", OPTIONAL(L('A')), True),
  ("ZERO_OR_MORE(L('A'))", ZERO_OR_MORE(L('A')), True),
  ("ONE_OR_MORE(L('A'))", ONE_OR_MORE(L('A')), True),
  ("LIST_OF(L('A'), sep=L('A'))", LIST_OF(L('A'), sep=L('A')), True),

  # explicit False:
  ("GRAMMAR('A', whitespace=False)", GRAMMAR('A', whitespace=False), False),
  ("G('A', whitespace=False)", G('A', whitespace=False), False),
  ("LITERAL('A', whitespace=False)", LITERAL('A', whitespace=False), False),
  ("L('A', whitespace=False)", L('A', whitespace=False), False),
  ("WORD('A', whitespace=False)", WORD('A', whitespace=False), False),
  ("ANY_EXCEPT('A', whitespace=False)", ANY_EXCEPT('A', whitespace=False), False),
  ("OR(L('A'), L('B'), whitespace=False)", OR(L('A'), L('B'), whitespace=False), False),
  ("EXCEPT(L('A'), L('B'), whitespace=False)", EXCEPT(L('A'), L('B'), whitespace=False), False),
  ("REPEAT(L('A'), whitespace=False)", REPEAT(L('A'), whitespace=False), False),
  ("OPTIONAL(L('A'), whitespace=False)", OPTIONAL(L('A'), whitespace=False), False),
  ("ZERO_OR_MORE(L('A'), whitespace=False)", ZERO_OR_MORE(L('A'), whitespace=False), False),
  ("ONE_OR_MORE(L('A'), whitespace=False)", ONE_OR_MORE(L('A'), whitespace=False), False),
  ("LIST_OF(L('A'), sep=L('A'), whitespace=False)", LIST_OF(L('A'), sep=L('A'), whitespace=False), False),

  # explicit True:
  ("GRAMMAR('A', whitespace=True)", GRAMMAR('A', whitespace=True), True),
  ("G('A', whitespace=True)", G('A', whitespace=True), True),
  ("LITERAL('A', whitespace=True)", LITERAL('A', whitespace=True), True),
  ("L('A', whitespace=True)", L('A', whitespace=True), True),
  ("WORD('A', whitespace=True)", WORD('A', whitespace=True), True),
  ("ANY_EXCEPT('A', whitespace=True)", ANY_EXCEPT('A', whitespace=True), True),
  ("OR(L('A'), L('B'), whitespace=True)", OR(L('A'), L('B'), whitespace=True), True),
  ("EXCEPT(L('A'), L('B'), whitespace=True)", EXCEPT(L('A'), L('B'), whitespace=True), True),
  ("REPEAT(L('A'), whitespace=True)", REPEAT(L('A'), whitespace=True), True),
  ("OPTIONAL(L('A'), whitespace=True)", OPTIONAL(L('A'), whitespace=True), True),
  ("ZERO_OR_MORE(L('A'), whitespace=True)", ZERO_OR_MORE(L('A'), whitespace=True), True),
  ("ONE_OR_MORE(L('A'), whitespace=True)", ONE_OR_MORE(L('A'), whitespace=True), True),
  ("LIST_OF(L('A'), sep=L('A'), whitespace=True)", LIST_OF(L('A'), sep=L('A'), whitespace=True), True),

  # Always false by default:
  ("LITERAL('A')", LITERAL('A'), False),
  ("L('A')", L('A'), False),
  ("WORD('A')", WORD('A'), False),
  ("ANY_EXCEPT('A')", ANY_EXCEPT('A'), False),
  ("OR(L('A'), L('B'))", OR(L('A'), L('B')), False),
  ("L('A') | L('B')", L('A') | L('B'), False),
  ("EXCEPT(L('A'), L('B'))", EXCEPT(L('A'), L('B')), False),
  ("ANY", ANY, False),
  ("EOL", EOL, False),
  ("EOF", EOF, False),
  ("EMPTY", EMPTY, False),
  ("REST_OF_LINE", REST_OF_LINE, False),
  ("SPACE", SPACE, False),

  # GRAMMAR with a single element just returns that element, so the following
  # should resolve to LITERALs, which are always false by default.
  ("GRAMMAR('A')", GRAMMAR('A'), False),
  ("G('A')", G('A'), False),
)

grammar_whitespace = False

class G_False (Grammar):
  grammar = (ONE_OR_MORE('A'), 'B')

class G_False_True (Grammar):
  grammar = (ONE_OR_MORE('A'), 'B')
  grammar_whitespace = True

class G_False_False (Grammar):
  grammar = (ONE_OR_MORE('A'), 'B')
  grammar_whitespace = False

modfalse_grammars = (
  ("G_False", G_False, False),
  ("G_False_True", G_False_True, True),
  ("G_False_False", G_False_False, False),
  ("GRAMMAR('A', 'B')", GRAMMAR('A', 'B'), False),
  ("G('A', 'B')", G('A', 'B'), False),
  ("REPEAT(L('A'))", REPEAT(L('A')), False),
  ("OPTIONAL(L('A'))", OPTIONAL(L('A')), False),
  ("ZERO_OR_MORE(L('A'))", ZERO_OR_MORE(L('A')), False),
  ("ONE_OR_MORE(L('A'))", ONE_OR_MORE(L('A')), False),
  ("LIST_OF(L('A'), sep=L('A'))", LIST_OF(L('A'), sep=L('A')), False),

  # explicit False:
  ("GRAMMAR('A', whitespace=False)", GRAMMAR('A', whitespace=False), False),
  ("G('A', whitespace=False)", G('A', whitespace=False), False),
  ("LITERAL('A', whitespace=False)", LITERAL('A', whitespace=False), False),
  ("L('A', whitespace=False)", L('A', whitespace=False), False),
  ("WORD('A', whitespace=False)", WORD('A', whitespace=False), False),
  ("ANY_EXCEPT('A', whitespace=False)", ANY_EXCEPT('A', whitespace=False), False),
  ("OR(L('A'), L('B'), whitespace=False)", OR(L('A'), L('B'), whitespace=False), False),
  ("EXCEPT(L('A'), L('B'), whitespace=False)", EXCEPT(L('A'), L('B'), whitespace=False), False),
  ("REPEAT(L('A'), whitespace=False)", REPEAT(L('A'), whitespace=False), False),
  ("OPTIONAL(L('A'), whitespace=False)", OPTIONAL(L('A'), whitespace=False), False),
  ("ZERO_OR_MORE(L('A'), whitespace=False)", ZERO_OR_MORE(L('A'), whitespace=False), False),
  ("ONE_OR_MORE(L('A'), whitespace=False)", ONE_OR_MORE(L('A'), whitespace=False), False),
  ("LIST_OF(L('A'), sep=L('A'), whitespace=False)", LIST_OF(L('A'), sep=L('A'), whitespace=False), False),

  # explicit True:
  ("GRAMMAR('A', whitespace=True)", GRAMMAR('A', whitespace=True), True),
  ("G('A', whitespace=True)", G('A', whitespace=True), True),
  ("LITERAL('A', whitespace=True)", LITERAL('A', whitespace=True), True),
  ("L('A', whitespace=True)", L('A', whitespace=True), True),
  ("WORD('A', whitespace=True)", WORD('A', whitespace=True), True),
  ("ANY_EXCEPT('A', whitespace=True)", ANY_EXCEPT('A', whitespace=True), True),
  ("OR(L('A'), L('B'), whitespace=True)", OR(L('A'), L('B'), whitespace=True), True),
  ("EXCEPT(L('A'), L('B'), whitespace=True)", EXCEPT(L('A'), L('B'), whitespace=True), True),
  ("REPEAT(L('A'), whitespace=True)", REPEAT(L('A'), whitespace=True), True),
  ("OPTIONAL(L('A'), whitespace=True)", OPTIONAL(L('A'), whitespace=True), True),
  ("ZERO_OR_MORE(L('A'), whitespace=True)", ZERO_OR_MORE(L('A'), whitespace=True), True),
  ("ONE_OR_MORE(L('A'), whitespace=True)", ONE_OR_MORE(L('A'), whitespace=True), True),
  ("LIST_OF(L('A'), sep=L('A'), whitespace=True)", LIST_OF(L('A'), sep=L('A'), whitespace=True), True),

  # Always false by default:
  ("LITERAL('A')", LITERAL('A'), False),
  ("L('A')", L('A'), False),
  ("WORD('A')", WORD('A'), False),
  ("ANY_EXCEPT('A')", ANY_EXCEPT('A'), False),
  ("OR(L('A'), L('B'))", OR(L('A'), L('B')), False),
  ("L('A') | L('B')", L('A') | L('B'), False),
  ("EXCEPT(L('A'), L('B'))", EXCEPT(L('A'), L('B')), False),
  ("ANY", ANY, False),
  ("EOL", EOL, False),
  ("EOF", EOF, False),
  ("EMPTY", EMPTY, False),
  ("REST_OF_LINE", REST_OF_LINE, False),
  ("SPACE", SPACE, False),

  # GRAMMAR with a single element just returns that element, so the following
  # should resolve to LITERALs, which are always false by default.
  ("GRAMMAR('A')", GRAMMAR('A'), False),
  ("G('A')", G('A'), False),
)

grammar_whitespace = True

class G_True (Grammar):
  grammar = (ONE_OR_MORE('A'), 'B')

class G_True_True (Grammar):
  grammar = (ONE_OR_MORE('A'), 'B')
  grammar_whitespace = True

class G_True_False (Grammar):
  grammar = (ONE_OR_MORE('A'), 'B')
  grammar_whitespace = False

modtrue_grammars = (
  ("G_True", G_True, True),
  ("G_True_True", G_True_True, True),
  ("G_True_False", G_True_False, False),
  ("GRAMMAR('A', 'B')", GRAMMAR('A', 'B'), True),
  ("G('A', 'B')", G('A', 'B'), True),
  ("REPEAT(L('A'))", REPEAT(L('A')), True),
  ("OPTIONAL(L('A'))", OPTIONAL(L('A')), True),
  ("ZERO_OR_MORE(L('A'))", ZERO_OR_MORE(L('A')), True),
  ("ONE_OR_MORE(L('A'))", ONE_OR_MORE(L('A')), True),
  ("LIST_OF(L('A'), sep=L('A'))", LIST_OF(L('A'), sep=L('A')), True),

  # explicit False:
  ("GRAMMAR('A', whitespace=False)", GRAMMAR('A', whitespace=False), False),
  ("G('A', whitespace=False)", G('A', whitespace=False), False),
  ("LITERAL('A', whitespace=False)", LITERAL('A', whitespace=False), False),
  ("L('A', whitespace=False)", L('A', whitespace=False), False),
  ("WORD('A', whitespace=False)", WORD('A', whitespace=False), False),
  ("ANY_EXCEPT('A', whitespace=False)", ANY_EXCEPT('A', whitespace=False), False),
  ("OR(L('A'), L('B'), whitespace=False)", OR(L('A'), L('B'), whitespace=False), False),
  ("EXCEPT(L('A'), L('B'), whitespace=False)", EXCEPT(L('A'), L('B'), whitespace=False), False),
  ("REPEAT(L('A'), whitespace=False)", REPEAT(L('A'), whitespace=False), False),
  ("OPTIONAL(L('A'), whitespace=False)", OPTIONAL(L('A'), whitespace=False), False),
  ("ZERO_OR_MORE(L('A'), whitespace=False)", ZERO_OR_MORE(L('A'), whitespace=False), False),
  ("ONE_OR_MORE(L('A'), whitespace=False)", ONE_OR_MORE(L('A'), whitespace=False), False),
  ("LIST_OF(L('A'), sep=L('A'), whitespace=False)", LIST_OF(L('A'), sep=L('A'), whitespace=False), False),

  # explicit True:
  ("GRAMMAR('A', whitespace=True)", GRAMMAR('A', whitespace=True), True),
  ("G('A', whitespace=True)", G('A', whitespace=True), True),
  ("LITERAL('A', whitespace=True)", LITERAL('A', whitespace=True), True),
  ("L('A', whitespace=True)", L('A', whitespace=True), True),
  ("WORD('A', whitespace=True)", WORD('A', whitespace=True), True),
  ("ANY_EXCEPT('A', whitespace=True)", ANY_EXCEPT('A', whitespace=True), True),
  ("OR(L('A'), L('B'), whitespace=True)", OR(L('A'), L('B'), whitespace=True), True),
  ("EXCEPT(L('A'), L('B'), whitespace=True)", EXCEPT(L('A'), L('B'), whitespace=True), True),
  ("REPEAT(L('A'), whitespace=True)", REPEAT(L('A'), whitespace=True), True),
  ("OPTIONAL(L('A'), whitespace=True)", OPTIONAL(L('A'), whitespace=True), True),
  ("ZERO_OR_MORE(L('A'), whitespace=True)", ZERO_OR_MORE(L('A'), whitespace=True), True),
  ("ONE_OR_MORE(L('A'), whitespace=True)", ONE_OR_MORE(L('A'), whitespace=True), True),
  ("LIST_OF(L('A'), sep=L('A'), whitespace=True)", LIST_OF(L('A'), sep=L('A'), whitespace=True), True),

  # Always false by default:
  ("LITERAL('A')", LITERAL('A'), False),
  ("L('A')", L('A'), False),
  ("WORD('A')", WORD('A'), False),
  ("ANY_EXCEPT('A')", ANY_EXCEPT('A'), False),
  ("OR(L('A'), L('B'))", OR(L('A'), L('B')), False),
  ("L('A') | L('B')", L('A') | L('B'), False),
  ("EXCEPT(L('A'), L('B'))", EXCEPT(L('A'), L('B')), False),
  ("ANY", ANY, False),
  ("EOL", EOL, False),
  ("EOF", EOF, False),
  ("EMPTY", EMPTY, False),
  ("REST_OF_LINE", REST_OF_LINE, False),
  ("SPACE", SPACE, False),

  # GRAMMAR with a single element just returns that element, so the following
  # should resolve to LITERALs, which are always false by default.
  ("GRAMMAR('A')", GRAMMAR('A'), False),
  ("G('A')", G('A'), False),
)

class WhitespaceTests (util.TestCase):

  def check_recursive(self, name, g, expected, expected_sub):
    if g.grammar_whitespace != expected:
      raise self.failureException("When testing {}: grammar_whitespace for {!r} is {!r}".format(name, g, g.grammar_whitespace))
    sub_list = g.grammar
    if isinstance(sub_list, RepeatingTuple):
      sub_list = [g.grammar[0]]
      if len(g.grammar) > 1:
        sub_list.append(g.grammar[1])
    if isinstance(g, ListRepetition):
      sub_list = list(sub_list)
      sub_list.append(g.sep)
    for sub_g in sub_list:
      if issubclass(sub_g, (Terminal, OR_Operator)):
	# Terminals (and OR constructs) always normally have grammar_whitespace
	# set to False
        self.check_recursive(name, sub_g, False, expected_sub)
      else:
        self.check_recursive(name, sub_g, expected_sub, expected_sub)

  def test_ws_default(self):
    for name, g, expected in default_grammars:
      self.check_recursive(name + " (module grammar_whitespace unset)", g, expected, True)

  def test_ws_modfalse(self):
    for name, g, expected in modfalse_grammars:
      self.check_recursive(name + " (module grammar_whitespace=False)", g, expected, False)

  def test_ws_modtrue(self):
    for name, g, expected in modtrue_grammars:
      self.check_recursive(name + " (module grammar_whitespace=True)", g, expected, True)

