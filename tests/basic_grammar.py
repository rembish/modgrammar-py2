import sys
import modgrammar
from modgrammar import *
from modgrammar import AnonGrammar
from . import util

#TODO:
# * modgrammar.extras classes
# * standard arg handling for all grammars that use them (count, min, max, collapse, name, desc)
# * collapsing
# * collapse_skip

grammar_whitespace = True

NoneType = type(None)

class G1 (Grammar):
  grammar = 'ABC'

class G2 (Grammar):
  grammar = ('ABC', 'DEF')

class G3 (Grammar):
  grammar = ('ABC', 'DEF')
  grammar_whitespace = False

class TestG1 (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = G1
    self.grammar_name = "G1"
    self.grammar_details = "L('ABC')"
    self.terminal = False
    self.subgrammar_types = (Literal,)
    self.matches = ('ABC',)
    self.matches_with_remainder = ('ABCD',)
    self.fail_matches = ('ABX', 'BC', 'abc', 'AB C')
    self.partials = (('A', 'B', 'C'), ('AB', 'C'), ('A', 'BC'), ('AB','CD'))
    self.fail_partials = (('A', 'B', 'X'), ('A', 'BX'))

class TestG2 (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = G2
    self.grammar_name = "G2"
    self.grammar_details = "(L('ABC'), L('DEF'))"
    self.terminal = False
    self.subgrammar_types = (Literal, Literal)
    self.matches = ('ABCDEF', 'ABC DEF')
    self.matches_with_remainder = ('ABCDEFG',)
    self.fail_matches = ('ABCDEX', 'ABCEF', 'abcdef', 'A BCDEF', 'ABCDE F')
    self.partials = (('A', 'B', 'C', 'DEF'), ('ABC', 'D', 'E', 'F'), ('AB', 'CD', 'EF'), ('ABC', ' ', 'DEF'))
    self.fail_partials = (('A', 'B', 'C', 'D', 'E', 'X'), ('ABC', 'D', 'EX'), ('AB', 'XDEF'))

class TestG3 (util.BasicGrammarTestCase):
  # For this, we're just checking that if grammar_whitespace=False, it won't
  # match if there's whitespace between tokens.
  def setUp(self):
    self.grammar = G3
    self.grammar_name = "G3"
    self.grammar_details = "(L('ABC'), L('DEF'))"
    self.terminal = False
    self.subgrammar_types = (Literal, Literal)
    self.matches = ('ABCDEF',)
    self.fail_matches = ('ABC DEF',)

class TestGRAMMAR (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = GRAMMAR('ABC', 'DEF')
    self.grammar_name = "<GRAMMAR>"
    self.grammar_details = "(L('ABC'), L('DEF'))"
    self.terminal = False
    self.subgrammar_types = (Literal, Literal)
    self.matches = ('ABCDEF', 'ABC DEF')
    self.matches_with_remainder = ('ABCDEFG',)
    self.fail_matches = ('ABCDEX', 'ABCEF', 'abcdef', 'A BCDEF', 'ABCDE F')
    self.partials = (('A', 'B', 'C', 'DEF'), ('ABC', 'D', 'E', 'F'), ('AB', 'CD', 'EF'), ('ABC', ' ', 'DEF'))
    self.fail_partials = (('A', 'B', 'C', 'D', 'E', 'X'), ('ABC', 'D', 'EX'), ('AB', 'XDEF'))

  def test_funcdef(self):
    self.assertTrue(issubclass(self.grammar, modgrammar.AnonGrammar))
    # using GRAMMAR() with a single element should just return the
    # (regularized) element.
    g = GRAMMAR('ABC')
    self.assertTrue(issubclass(g, Literal))

class TestGRAMMAR_NoWS (util.BasicGrammarTestCase):
  # For this, we're just checking that if grammar_whitespace=False, it won't
  # match if there's whitespace between tokens.
  def setUp(self):
    self.grammar = GRAMMAR('ABC', 'DEF', whitespace=False)
    self.grammar_name = "<GRAMMAR>"
    self.grammar_details = "(L('ABC'), L('DEF'))"
    self.terminal = False
    self.subgrammar_types = (Literal, Literal)
    self.matches = ('ABCDEF',)
    self.fail_matches = ('ABC DEF',)

class TestLiteral (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = LITERAL('ABC')
    self.grammar_name = "L('ABC')"
    self.grammar_details = "L('ABC')"
    self.matches = ('ABC',)
    self.matches_with_remainder = ('ABCD',)
    self.fail_matches = ('ABX', 'BC', 'abc', '\nABC', 'AB C')
    self.partials = (('A', 'B', 'C'), ('AB', 'C'), ('A', 'BC'), ('AB','CD'))
    self.fail_partials = (('A', 'B', 'X'), ('A', 'BX'))

class TestEmpty (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = EMPTY
    self.grammar_name = "EMPTY"
    self.grammar_details = "EMPTY"
    self.expected_match_types = (NoneType,)
    self.matches_as_false = ('',)
    self.matches_with_remainder = ('A',)

class TestOr (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = OR('ABC', 'ABD', 'CDE')
    self.grammar_name = "<OR>"
    self.grammar_details = "(L('ABC') | L('ABD') | L('CDE'))"
    self.subgrammar_types = (Literal, Literal, Literal)
    self.expected_match_types = (Literal,)
    self.matches = ('ABC', 'ABD', 'CDE')
    self.matches_with_remainder = ('ABCD', 'CDEF', 'ABD\n')
    self.fail_matches = ('abc', '\nABC', 'AABC')
    self.partials = (('A', 'B', 'C'), ('A', 'B', 'D'), ('C', 'DE'), ('AB', 'CD'))
    self.fail_partials = (('A', 'B', 'X'),)

  def num_tokens_for(self, teststr):
    return (1, 1)

  def test_operator(self):
    """Test the OR operator ('|')
       Make sure the OR operator ('|') correctly wraps other grammars in an OR
       class.  Also make sure that ORing together grammars with non-grammars
        results in a correctly regularized result.
    """
    g = L('ABC') | L('ABD')
    self.assertTrue(issubclass(g, modgrammar.OR_Operator))
    self.check_sanity(g, (Literal, Literal))
    g = L('ABC') | 'ABD'
    self.assertTrue(issubclass(g, modgrammar.OR_Operator))
    self.check_sanity(g, (Literal, Literal))
    g = 'ABC' | L('ABD')
    self.assertTrue(issubclass(g, modgrammar.OR_Operator))
    self.check_sanity(g, (Literal, Literal))
    g = L('ABC') | (L('ABD'), L('CDE'))
    self.assertTrue(issubclass(g, modgrammar.OR_Operator))
    self.check_sanity(g, (Literal, AnonGrammar))
    g = (L('ABC'), L('ABD')) | L('CDE')
    self.assertTrue(issubclass(g, modgrammar.OR_Operator))
    self.check_sanity(g, (AnonGrammar, Literal))

  def test_ormerge(self):
    """Test multiple ORs in sequence
       Make sure that ORing together multiple things collapses to just a single
       OR, and keeps the order correct.
    """
    g = ( L('ABC') | L('ABD') ) | L('CDE')
    self.assertTrue(issubclass(g, modgrammar.OR_Operator))
    self.check_sanity(g, (Literal, Literal, Literal))
    self.assertEqual([x.string for x in g.grammar], ['ABC', 'ABD', 'CDE'])
    g = L('ABC') | ( L('ABD') | L('CDE') )
    self.assertTrue(issubclass(g, modgrammar.OR_Operator))
    self.check_sanity(g, (Literal, Literal, Literal))
    self.assertEqual([x.string for x in g.grammar], ['ABC', 'ABD', 'CDE'])
    g = ( L('ABC') | L('ABD') ) | ( L('CDE') | L('FGH') )
    self.assertTrue(issubclass(g, modgrammar.OR_Operator))
    self.check_sanity(g, (Literal, Literal, Literal, Literal))
    self.assertEqual([x.string for x in g.grammar], ['ABC', 'ABD', 'CDE', 'FGH'])

class TestRepeat1 (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = REPEAT('ABC', min=2, max=5)
    self.grammar_name = "<REPEAT>"
    self.grammar_details = "REPEAT(L('ABC'), min=2, max=5)"
    self.subgrammar_types = (Literal, Literal, Literal, Literal, Literal)
    self.terminal = False
    self.matches = ('ABCABCABCABCABC', 'ABC ABC ABC ABC ABC')
    self.matches_with_remainder = ('ABCABCx', 'ABCABCABCABx', 'ABC ABCx', 'ABC ABC x')
    self.fail_matches = ('ABCx',)
    self.partials = (('ABC', 'ABC', 'x'), ('ABCABC', 'x'), ('AB', 'CA', 'BC', 'x'), ('ABCABC', 'ABCABC', 'ABC'), ('ABC ', 'ABC', ' ABC', ' ', 'ABC ABC'))
    self.fail_partials = (('ABC', 'ABx'),)

  def test_defaults(self):
    g = REPEAT('ABC')
    self.assertEqual(g.grammar_min, 1)
    self.assertEqual(g.grammar_max, sys.maxsize)

  def test_greedy(self):
    # Make sure the default is to be greedy
    self.assertTrue(REPEAT('ABC').grammar_greedy)
    # Test greedy behavior
    p = REPEAT('ABC', min=0, max=3, greedy=True).parser()
    o = p.parse_string('ABCABCABCABC', matchtype='all')
    self.assertEqual([x.string for x in o], ['ABCABCABC', 'ABCABC', 'ABC', ''])
    # Test non-greedy behavior
    p = REPEAT('ABC', min=0, max=3, greedy=False).parser()
    o = p.parse_string('ABCABCABCABC', matchtype='all')
    self.assertEqual([x.string for x in o], ['', 'ABC', 'ABCABC', 'ABCABCABC'])
    # Simple test of combining greedy and non-greedy repetitions
    g = GRAMMAR(REPEAT('ABC', max=3, min=0, greedy=False), REPEAT('ABC', max=3, min=0))
    p = g.parser()
    o = p.parse_string('ABCABCABCABCx', matchtype='all')
    strings = [[x.string for x in y] for y in o]
    self.assertEqual(strings, [['', 'ABCABCABC'],
                               ['', 'ABCABC'],
                               ['', 'ABC'],
                               ['', ''],
                               ['ABC', 'ABCABCABC'],
                               ['ABC', 'ABCABC'],
                               ['ABC', 'ABC'],
                               ['ABC', ''],
                               ['ABCABC', 'ABCABC'],
                               ['ABCABC', 'ABC'],
                               ['ABCABC', ''],
                               ['ABCABCABC', 'ABC'],
                               ['ABCABCABC', ''],
                              ])

class TestRepeat2 (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = REPEAT('ABC', min=0)
    self.grammar_name = "<REPEAT>"
    self.grammar_details = "REPEAT(L('ABC'), min=0)"
    self.subgrammar_types = None
    self.terminal = False
    self.matches_with_remainder = ('ABCx', 'ABCABCABCABCABCABCABCABCx')
    self.matches_as_false = ('x')

class TestRepeat1_NoWS (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = REPEAT('ABC', min=2, max=5, whitespace=False)
    self.grammar_name = "<REPEAT>"
    self.grammar_details = "REPEAT(L('ABC'), min=2, max=5)"
    self.subgrammar_types = (Literal, Literal, Literal, Literal, Literal)
    self.terminal = False
    self.matches = ('ABCABCABCABCABC',)
    self.matches_with_remainder = ('ABCABCx', 'ABCABCABCABx')
    self.fail_matches = ('ABC ABC ABC ABC ABC', 'ABC ABC', 'ABCx')
    self.partials = (('ABC', 'ABC', 'x'), ('ABCABC', 'x'), ('AB', 'CA', 'BC', 'x'), ('ABCABC', 'ABCABC', 'ABC'))
    self.fail_partials = (('ABC', 'ABx'), ('ABC ',), ('ABC', ' ABC'), ('ABC', ' '))

class TestOptional (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = OPTIONAL('ABC')
    self.grammar_name = "<OPTIONAL>"
    self.grammar_details = "OPTIONAL(L('ABC'))"
    self.subgrammar_types = (Literal,)
    self.expected_match_types = (Literal, NoneType)
    self.terminal = True
    self.matches = ('ABC',)
    self.matches_with_remainder = ('ABCx', 'ABCABC')
    self.partials = (('A', 'B', 'C'), ('A', 'B', 'x'))

  def test_failmatch_is_none(self):
    p = self.grammar.parser()
    o = p.parse_string('x')
    self.assertEqual(p.remainder(), 'x')
    self.assertIsNone(o)

  def test_greedy(self):
    # Make sure the default is to be greedy
    self.assertTrue(OPTIONAL('ABC').grammar_greedy)
    # Test greedy behavior
    p = OPTIONAL('ABC', greedy=True).parser()
    o = p.parse_string('ABC', matchtype='all')
    self.assertEqual([x and x.string for x in o], ['ABC', None])
    # Test non-greedy behavior
    p = OPTIONAL('ABC', greedy=False).parser()
    o = p.parse_string('ABC', matchtype='all')
    self.assertEqual([x and x.string for x in o], [None, 'ABC'])
    # Simple test of combining greedy and non-greedy optionals
    g = GRAMMAR(OPTIONAL('ABC', greedy=False), OPTIONAL('ABC'))
    p = g.parser()
    o = p.parse_string('ABCABC', matchtype='all')
    strings = [[x and x.string for x in y] for y in o]
    self.assertEqual(strings, [[None, 'ABC'],
                               [None, None],
                               ['ABC', 'ABC'],
                               ['ABC', None],
                              ])

class TestZeroOrMore (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = ZERO_OR_MORE('ABC')
    self.grammar_name = "<REPEAT>"
    self.grammar_details = "REPEAT(L('ABC'), min=0)"
    self.subgrammar_types = None
    self.terminal = False

  def test_def(self):
    self.assertTrue(issubclass(self.grammar, Repetition))
    self.assertEqual(self.grammar.grammar_min, 0)
    self.assertEqual(self.grammar.grammar_max, sys.maxsize)

class TestOneOrMore (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = ONE_OR_MORE('ABC')
    self.grammar_name = "<REPEAT>"
    self.grammar_details = "REPEAT(L('ABC'))"
    self.subgrammar_types = None
    self.terminal = False

  def test_def(self):
    self.assertTrue(issubclass(self.grammar, Repetition))
    self.assertEqual(self.grammar.grammar_min, 1)
    self.assertEqual(self.grammar.grammar_max, sys.maxsize)

class TestList1 (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = LIST_OF('ABC', max=3)
    self.grammar_name = "<LIST>"
    self.grammar_details = "LIST_OF(L('ABC'), sep=L(','), max=3)"
    self.subgrammar_types = (Literal, AnonGrammar, AnonGrammar)
    self.terminal = False
    self.matches = ('ABC,ABC,ABC', 'ABC, ABC ,ABC')
    self.matches_with_remainder = ('ABCx', 'ABC,ABCx', 'ABC,ABC,x', 'ABC,ABC,ABC,ABC')
    self.fail_matches = ('x',)
    self.partials = (('A', 'B', 'C', 'x'), ('ABC', ',A', 'BCx'), ('ABC', ',', 'ABC', 'x'), ('ABC ', ',', ' ABC', ' ,', 'ABC'), ('ABC, ', 'ABC', ' ', ',', ' ', 'ABC'))

  def num_tokens_for(self, teststr):
    numtok = len(teststr.split(','))*2 - 1
    return (numtok, numtok)

  def test_trailing_comma(self):
    p = self.grammar.parser()
    p.parse_string('ABC,x')
    self.assertEqual(p.remainder(), ',x')
    p.reset()
    p.parse_string('ABC,ABC,ABC,')
    self.assertEqual(p.remainder(), ',')

class TestList2 (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = LIST_OF('A', 'B', sep=(L(':'), L(':')))
    self.grammar_name = "<LIST>"
    self.grammar_details = "LIST_OF((L('A'), L('B')), sep=(L(':'), L(':')))"
    self.subgrammar_types = None
    self.terminal = False
    self.matches_with_remainder = ('ABC', 'ABAB', 'AB:AB', 'AB::ABx', 'AB::AB::x')
    self.fail_matches = ('::AB',)
    self.partials = (('A', 'B', ':', ':', 'AB', 'x'), ('AB:', ':AB', ':AB'))

  def num_tokens_for(self, teststr):
    numtok = (len(teststr.split('::'))*2 - 1)*2
    return (numtok, numtok)

class TestList_NoWS (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = LIST_OF('ABC', count=3, whitespace=False)
    self.grammar_name = "<LIST>"
    self.grammar_details = "LIST_OF(L('ABC'), sep=L(','), count=3)"
    self.subgrammar_types = (Literal, AnonGrammar, AnonGrammar)
    self.terminal = False
    self.matches = ('ABC,ABC,ABC',)
    self.fail_matches = ('ABC ,ABC,ABC', 'ABC, ABC,ABC')
    self.fail_partials = (('ABC ',), ('ABC', ' ,'), ('ABC', ', '), ('ABC', ',', ' ABC'))

  def num_tokens_for(self, teststr):
    numtok = len(teststr.split(','))*2 - 1
    return (numtok, numtok)

class TestWord1 (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = WORD('a-z', min=2, max=5)
    self.grammar_name = "WORD('a-z')"
    self.grammar_details = "WORD('a-z', min=2, max=5)"
    self.matches = ('abcde',)
    self.matches_with_remainder = ('abcdef', 'ab#cd')
    self.fail_matches = ('Abcd', '\nabcde', 'a bcd')
    self.partials = (('a', 'b', 'c', 'd', 'e'), ('a', 'b', '#'))
    self.fail_partials = (('a', '#'),)

  # Test backtracking on WORD grammars
  def test_backtrack(self):
    g = GRAMMAR(self.grammar, 'a')
    p = g.parser()
    with self.assertRaises(ParseError):
      p.parse_string('abcdefa') # doesn't have 'a' after the max word length
    p.reset()
    o = p.parse_string('abcdea')
    self.assertEqual(o.tokens(), ['abcde', 'a'])
    p.reset()
    o = p.parse_string('abcdae')
    self.assertEqual(o.tokens(), ['abcd', 'a'])
    p.reset()
    o = p.parse_string('abcade')
    self.assertEqual(o.tokens(), ['abc', 'a'])
    p.reset()
    o = p.parse_string('abacde')
    self.assertEqual(o.tokens(), ['ab', 'a'])
    p.reset()
    with self.assertRaises(ParseError):
      p.parse_string('aabcde') # has to backtrack too far

  def test_greedy(self):
    # Make sure the default is to be greedy
    self.assertTrue(WORD('a-z').grammar_greedy)
    # Test greedy behavior
    p = WORD('a-z', min=0, max=3, greedy=True).parser()
    o = p.parse_string('abcd', matchtype='all')
    self.assertEqual([x.string for x in o], ['abc', 'ab', 'a', ''])
    # Test non-greedy behavior
    p = WORD('a-z', min=0, max=3, greedy=False).parser()
    o = p.parse_string('abcd', matchtype='all')
    self.assertEqual([x.string for x in o], ['', 'a', 'ab', 'abc'])
    # Simple test of combining greedy and non-greedy words
    g = GRAMMAR(WORD('a-z', max=3, min=0, greedy=False), WORD('a-z', max=3, min=0))
    p = g.parser()
    o = p.parse_string('abcdefg', matchtype='all')
    strings = [[x.string for x in y] for y in o]
    self.assertEqual(strings, [['', 'abc'],
                               ['', 'ab'],
                               ['', 'a'],
                               ['', ''],
                               ['a', 'bcd'],
                               ['a', 'bc'],
                               ['a', 'b'],
                               ['a', ''],
                               ['ab', 'cde'],
                               ['ab', 'cd'],
                               ['ab', 'c'],
                               ['ab', ''],
                               ['abc', 'def'],
                               ['abc', 'de'],
                               ['abc', 'd'],
                               ['abc', ''],
                              ])

class TestWord2 (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = WORD('A-Z', 'a-z', min=0, max=5)
    self.grammar_name = "WORD('A-Z', 'a-z')"
    self.grammar_details = "WORD('A-Z', 'a-z', min=0, max=5)"
    self.matches = ('Abcde',)
    self.matches_with_remainder = ('Abcdef', 'Ab#cd', 'abc')
    self.matches_as_false = ('abc',)
    self.partials = (('A', 'b', 'c', 'd', 'e'), ('A', 'b', '#'))

  # Test backtracking on WORD(min=0) grammars
  def test_backtrack(self):
    g = GRAMMAR(self.grammar, 'a')
    p = g.parser()
    o = p.parse_string('Abcade')
    self.assertEqual(o.tokens(), ['Abc', 'a'])
    g = GRAMMAR(self.grammar, 'A')
    p = g.parser()
    o = p.parse_string('Abcade')
    self.assertEqual(o.tokens(), ['', 'A'])

class TestAnyExcept (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = ANY_EXCEPT('a-z')
    self.grammar_name = "ANY_EXCEPT('a-z')"
    self.grammar_details = "WORD('^a-z')"
    self.matches_with_remainder = ('Ab', '!@^  "abc', '\na', ' a')
    self.fail_matches = ('abcd', 'a')
    self.partials = (('A', 'B', 'c'),)

  def test_pre_post_space(self):
    # This would normally fail the default pre/post space tests, because it has
    # grammar_whitespace=False, but still matches fine if there's whitespace at
    # the beginning (because whitespace characters match the ANY_EXCEPT
    # criteria), so we'll just skip that test in this case.
    pass

class TestBOL (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = BOL
    self.grammar_name = "BOL"
    self.grammar_details = "BOL"
    self.matches = ('',)
    self.matches_with_remainder = ('a',)

  def test_match_fail(self):
    with self.assertRaises(ParseError):
      self.grammar.parser().parse_string('a', bol=False)

  def test_mid_string(self):
    grammar = GRAMMAR(ANY, BOL)
    p = grammar.parser()
    o = p.parse_string('a\na')
    self.assertIsNotNone(o)
    self.assertEqual(p.remainder(), 'a')
    grammar = GRAMMAR(ANY, ANY, BOL, whitespace=False)
    p = grammar.parser()
    o = p.parse_string('a\na')
    self.assertIsNotNone(o)
    self.assertEqual(p.remainder(), 'a')
    p.reset()
    o = p.parse_string('a\r')
    self.assertIsNotNone(o)
    self.assertEqual(p.remainder(), '')

class TestEOL (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = EOL
    self.grammar_name = "EOL"
    self.grammar_details = "EOL"
    self.subgrammar_types = None
    self.matches = ('\r\n', '\n\r')
    self.matches_with_remainder = ('\r ', '\n ', '\r\r', '\n\n', '\r\n\r', '\n\r\n', '\r\n\r\n', '\n\r\n\r')
    self.fail_matches = ('a\n', ' \r', ' \n')
    self.partials = (('\r', '\n'), ('\n', '\r'), ('\r', ' '), ('\n', ' '))

class TestRestOfLine (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = REST_OF_LINE
    self.grammar_name = "REST_OF_LINE"
    self.grammar_details = "WORD('^\\r\\n', min=0)"
    self.matches_with_remainder = ('\r', '\n', ' \r', ' \n')
    self.matches_as_false = ('\r', '\n')
    self.partials = (('ab', '\n'), ('ab', '\r'), ('a', 'b\r'), ('a', 'b\n'))

  def test_pre_post_space(self):
    # This would normally fail the default pre/post space tests, because it has
    # grammar_whitespace=False, but still matches fine if there's whitespace at
    # the beginning (because whitespace characters match the REST_OF_LINE
    # criteria), so we'll just skip that test in this case.
    pass

class TestANY (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = ANY
    self.grammar_name = "ANY"
    self.grammar_details = "ANY"
    self.matches = ('a', 'A', ' ', '\n', '\0')
    self.matches_with_remainder = ('aa', ' a', 'a ')

  def test_pre_post_space(self):
    # This would normally fail the default pre/post space tests, because it has
    # grammar_whitespace=False, but still matches if there's whitespace at
    # the beginning (because whitespace characters match the ANY
    # criteria), so we'll just skip that test in this case.
    # Actual testing of whitespace before/after a string is already handled by
    # the matches_with_remainder test cases.
    pass

class TestSpace (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = SPACE
    self.grammar_name = "SPACE"
    self.grammar_details = "SPACE"
    self.matches_with_remainder = (' \t\r\na', '   a')
    self.fail_matches = ('a', 'a ')
    self.partials = ((' ', 'a'),)

  def test_pre_post_space(self):
    # This would normally fail the default pre/post space tests, because it has
    # grammar_whitespace=False, but still matches fine if there's whitespace at
    # the beginning (because whitespace characters match the SPACE
    # criteria), so we'll just skip that test in this case.
    pass

class TestEOF (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = EOF
    self.grammar_name = "EOF"
    self.grammar_details = "EOF"

  def test_matches(self):
    # EOF is kinda a special case, so we need to test it differently than most
    # grammars.
    g = self.grammar
    p = g.parser()
    try:
      o = p.parse_string('', eof=True)
      self.check_result('', o, True, '')
    except ParseError:
      self.fail("Got unexpected ParseError")

  def test_match_fail(self):
    p = self.grammar.parser()
    for teststr in ('a', ' '):
      p.reset()
      msg = '[testcase={!r}]'.format(teststr)
      with self.assertRaises(ParseError, msg=msg):
        p.parse_string(teststr, eof=True)

  def test_partial(self):
    g = self.grammar
    p = g.parser()
    try:
      o = p.parse_string('')
      self.assertIsNone(o)
      o = p.parse_string('', eof=True)
      self.check_result('', o, True, '')
    except ParseError:
      self.fail("Got unexpected ParseError")

  def test_inside_grammar(self):
    g = GRAMMAR(EMPTY, EOF)
    p = g.parser()
    try:
      for teststr in ('', ' '):
        msg = '[testcase={!r}]'.format(teststr)
        o = p.parse_string(teststr, eof=True)
        self.assertIsNotNone(o)
        self.assertEqual(len(p.remainder()), 0)
    except ParseError:
      self.fail("Got unexpected ParseError")

class TestExcept (util.BasicGrammarTestCase):
  def setUp(self):
    self.grammar = EXCEPT(WORD('A-Z', count=3), L('ABC'))
    self.grammar_name = "<EXCEPT>"
    self.grammar_details = "(WORD('A-Z', min=3, max=3) - L('ABC'))"
    self.subgrammar_types = (Word, Literal)
    self.expected_match_types = (Word, Literal)
    self.matches = ('AAA', 'ABD')
    self.fail_matches = ('ABC',)
    self.partials = (('A', 'B', 'D'),)
    self.fail_partials = (('A', 'B', 'C'),)

  def num_tokens_for(self, teststr):
    return (1, 1)

  def test_operator(self):
    g = L('ABC') - L('DEF')
    self.assertTrue(issubclass(g, modgrammar.ExceptionGrammar))
    self.check_sanity(g, (Literal, Literal))
    g = L('ABC') - 'DEF'
    self.assertTrue(issubclass(g, modgrammar.ExceptionGrammar))
    self.check_sanity(g, (Literal, Literal))
    g = 'ABC' - L('DEF')
    self.assertTrue(issubclass(g, modgrammar.ExceptionGrammar))
    self.check_sanity(g, (Literal, Literal))
    g = L('ABC') - L('DEF') - L('GHI')
    self.assertTrue(issubclass(g, modgrammar.ExceptionGrammar))
    self.check_sanity(g, (modgrammar.ExceptionGrammar, Literal))
    self.assertEqual(g.grammar[0].grammar[1].string, 'DEF')

