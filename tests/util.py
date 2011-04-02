import sys
import unittest
from modgrammar import ParseError, Text
from modgrammar.util import RepeatingTuple

class _AssertRaisesContext(object):
    """A context manager used to implement BasicGrammarTestCase.assertRaises* methods."""

    def __init__(self, expected, test_case, expected_regexp=None, msg=None):
        self.expected = expected
        self.failureException = test_case.failureException
        self.longMessage = test_case.longMessage
        self.expected_regexp = expected_regexp
        self.msg = msg

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            try:
                exc_name = self.expected.__name__
            except AttributeError:
                exc_name = str(self.expected)
            msg = "{0} not raised".format(exc_name)
            if self.msg:
              if self.longMessage:
                msg = "{0}: {1}".format(msg, self.msg)
              else:
                msg = self.msg
            raise self.failureException(msg)
        if not issubclass(exc_type, self.expected):
            # let unexpected exceptions pass through
            return False
        self.exception = exc_value # store for later retrieval
        if self.expected_regexp is None:
            return True

        expected_regexp = self.expected_regexp
        if isinstance(expected_regexp, str):
            expected_regexp = re.compile(expected_regexp)
        if not expected_regexp.search(str(exc_value)):
            raise self.failureException('{!r} does not match {!r}'.format(expected_regexp.pattern, str(exc_value)))
        return True


class TestCase (unittest.TestCase):
  def assertRaises(self, excClass, callableObj=None, msg=None):
    context = _AssertRaisesContext(excClass, self, msg=msg)
    if callableObj is None:
      return context
    with context:
      callableObj(*args, **kwargs)

  def assertIsInstance(self, obj, cls, msg=None):
    if not isinstance(obj, cls):
      msg = self._formatMessage(msg, "%r is not an instance of %r" % (obj, cls))
      raise self.failureException(msg)

  def assertIsSubclass(self, obj, cls, msg=None):
    if not issubclass(obj, cls):
      msg = self._formatMessage(msg, "%r is not a subclass of %r" % (obj, cls))
      raise self.failureException(msg)

class BasicGrammarTestCase (TestCase):
  def __init__(self, *args, **kwargs):
    unittest.TestCase.__init__(self, *args, **kwargs)
    self.longMessage = True

    self.grammar = None
    self.grammar_name = None
    self.grammar_details = None
    self.subgrammar_types = ()
    self.expected_match_types = None
    self.terminal = True
    self.check_min_max = True
    self.matches = ()
    self.matches_with_remainder = ()
    self.matches_as_false = ()
    self.fail_matches = ()
    self.partials = ()
    self.fail_partials = ()


  def check_result(self, teststr, o, istrue, msg):
    matchtypes = self.expected_match_types
    if matchtypes is None:
      matchtypes = self.grammar
    self.assertIsInstance(o, matchtypes, msg)
    if o is not None:
      # If o is None, and it made it past the assertIsInstance above, this must
      # mean None is an expected result, so we'll skip the tests that don't
      # make any sense for None...
      self.assertEqual(o.string, teststr, msg)
      if istrue is not None:
        self.assertEqual(bool(o), istrue, msg)
      self.assertEqual(o.grammar_terminal, self.terminal, msg)
      if self.check_min_max:
        mintok, maxtok = self.num_tokens_for(teststr)
        self.assertGreaterEqual(len(o.tokens()), mintok, msg)
        self.assertLessEqual(len(o.tokens()), maxtok, msg)

  def num_tokens_for(self, teststr):
    if self.grammar.grammar_terminal:
      return (1, 1)
    else:
      return (self.grammar.grammar_min, self.grammar.grammar_max)

  def check_sanity(self, grammar, subgrammar_types=()):
    '''Basic sanity-checks that should always be true for all Grammar classes'''
    subgrammar = grammar.grammar
    self.assertIsInstance(subgrammar, tuple)
    glen = len(subgrammar)
    if subgrammar_types is not None:
      self.assertEqual(glen, len(subgrammar_types))
      for i in range(glen):
        g = subgrammar[i]
        t = subgrammar_types[i]
        self.assertTrue(issubclass(g, t), "Sub-grammar {}: {!r} should be a subclass of {}".format(i, g, t.__name__))
    self.assertIsInstance(grammar.grammar_min, int)
    self.assertGreaterEqual(grammar.grammar_min, 0)
    if grammar.grammar_max is not None:
      self.assertIsInstance(grammar.grammar_max, int)
      self.assertGreaterEqual(grammar.grammar_max, 0)
    if glen != 0:
      self.assertLessEqual(grammar.grammar_min, glen)
      self.assertLessEqual(grammar.grammar_max, glen)
    self.assertIsInstance(grammar.grammar_tags, tuple)

  def test_sanity(self):
    self.check_sanity(self.grammar, self.subgrammar_types)

  def test_grammar_name(self):
    self.assertEqual(self.grammar.grammar_name, self.grammar_name)

  def test_grammar_details(self):
    self.assertEqual(self.grammar.grammar_details(), self.grammar_details)

  def test_matches(self):
    p = self.grammar.parser()
    try:
      for teststr in self.matches:
        msg = '[testcase={!r}]'.format(teststr)
        o = p.parse_string(teststr)
        self.check_result(teststr, o, True, msg)
        self.assertEqual(p.remainder(), '', msg)
    except ParseError:
      self.fail("Got unexpected ParseError {}".format(msg))

  def test_matches_with_remainder(self):
    p = self.grammar.parser()
    try:
      for teststr in self.matches_with_remainder:
        msg = '[testcase={!r}]'.format(teststr)
        p.reset()
        o = p.parse_string(teststr)
        remainder = p.remainder()
        self.check_result(teststr[:-len(remainder)], o, None, msg)
        self.assertNotEqual(remainder, '', msg)
    except ParseError:
      self.fail("Got unexpected ParseError {}".format(msg))

  def test_matches_with_eof(self):
    # This uses the same testcases as test_matches_with_remainder, but cuts off
    # the remainders from the test input and substitutes eof=True instead.
    p = self.grammar.parser()
    try:
      for teststr in self.matches_with_remainder:
        p.reset()
        try:
          if p.parse_string(teststr) is None:
	    # This should be caught in test_matches_with_remainder, so let that
	    # one report the error, just keep going with the next test case.
            continue
        except ParseError:
	  # This should be caught in test_matches_with_remainder, so let that
	  # one report the error, just keep going with the next test case.
          continue
        remainder = p.remainder()
        teststr = teststr[:-len(remainder)]
        msg = '[testcase={!r}]'.format(teststr)
        p.reset()
        o = p.parse_string(teststr, eof=True)
        remainder = p.remainder()
        self.check_result(teststr, o, None, msg)
        self.assertEqual(remainder, '', msg)
	# Test this a second way, with the EOF being sent as an empty string
	# after a partial-match, to make sure that works too.
        msg = '[testcase={}, eof after partial]'.format(teststr)
        p.reset()
        o = p.parse_string(teststr)
        if o is None:
          o = p.parse_string('', eof=True)
        else:
	  # some matches-with-remainder cases may immediately match, without
	  # having to send an eof.  This is ok, too.
          pass
        remainder = p.remainder()
        self.check_result(teststr, o, None, msg)
        self.assertEqual(remainder, '', msg)
      # Make sure that if this grammar gets called with an empty text buffer and eof=True that it correctly yields either False or a 0-length match (specifically, yielding None on EOF is bad)
      for teststr in ('', ' '):
        t = Text(teststr, eof=True)
        s = self.grammar.grammar_parse(t, 0, {})
        for count, obj in s:
          if count is False:
            break
          elif count not in (0, len(teststr)):
            self.fail("{!r} yielded count={!r} for {!r}+EOF".format(self.grammar, count, teststr))
      # If we call parse_string with an empty buffer and eof=True, make sure it doesn't throw any exceptions
      p.reset()
      o = p.parse_string('', eof=True)
    except ParseError:
      self.fail("Got unexpected ParseError {}".format(msg))

  def test_matches_as_false(self):
    p = self.grammar.parser()
    try:
      for teststr in self.matches_as_false:
        msg = '[testcase={!r}]'.format(teststr)
        p.reset()
        o = p.parse_string(teststr)
        remlen = len(p.remainder())
        if remlen:
          teststr = teststr[:-remlen]
        self.check_result(teststr, o, False, msg)
    except ParseError:
      self.fail("Got unexpected ParseError {}".format(msg))

  def test_match_fail(self):
    p = self.grammar.parser()
    for teststr in self.fail_matches:
      p.reset()
      msg = '[testcase={!r}]'.format(teststr)
      with self.assertRaises(ParseError, msg=msg):
        p.parse_string(teststr)

  def test_partial(self):
    p = self.grammar.parser()
    for case in self.partials:
      msg = '[testcase={!r}]'.format(case)
      p.reset()
      prelim = case[:-1]
      final = case[-1]
      for pstr in prelim:
        try:
          o = p.parse_string(pstr)
        except ParseError:
          self.fail("Got ParseError on {!r} of {!r}".format(pstr, case))
        self.assertIsNone(o, "[{!r} of {!r}]".format(pstr, case))
      try:
        o = p.parse_string(final)
      except ParseError:
        self.fail("Got ParseError on {!r} of {!r}".format(final, case))
      remlen = len(p.remainder())
      teststr = ''.join(case)
      if remlen:
        teststr = teststr[:-remlen]
      self.check_result(teststr, o, None, msg)

  def test_partial_fail(self):
    p = self.grammar.parser()
    for case in self.fail_partials:
      msg = '[testcase={!r}]'.format(case)
      p.reset()
      prelim = case[:-1]
      final = case[-1]
      for pstr in prelim:
        try:
          o = p.parse_string(pstr)
        except ParseError:
          self.fail("Got ParseError on {!r} of {!r}".format(pstr, case))
        self.assertIsNone(o, "[{!r} of {!r}]".format(pstr, case))
      with self.assertRaises(ParseError, msg=msg):
        p.parse_string(final)

  def test_pre_post_space(self):
    try:
      p = self.grammar.parser()
      if self.grammar.grammar_whitespace is True:
        for teststr in self.matches + self.matches_with_remainder:
          msg = '[testcase={!r}]'.format(teststr)
          p.reset()
          teststr = ' ' + teststr + ' '
          o = p.parse_string(teststr)
          remainder = p.remainder()
          self.assertNotEqual(remainder, '', msg)
          self.check_result(teststr[:-len(remainder)], o, None, msg)
      elif self.grammar.grammar_whitespace is False:
        for teststr in self.matches + self.matches_with_remainder:
          p.reset()
          msg = '[testcase={!r}]'.format(teststr)
          teststr = ' ' + teststr
          try:
            o = p.parse_string(teststr)
          except ParseError:
            pass
          else:
            remainder = p.remainder()
            self.assertEqual(remainder, teststr, msg)
    except ParseError:
      self.fail("Got unexpected ParseError {}".format(msg))

