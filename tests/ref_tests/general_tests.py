from modgrammar import *
from modgrammar.util import RepeatingTuple
from .. import util

class G0 (Grammar):
  grammar = (REF('G1', default=L('x')))

class G1 (Grammar):
  grammar = (L('a'))

class G2 (Grammar):
  grammar = (L('b'))

class G3 (Grammar):
  grammar = (REF('NonexistantGrammar'))

class G4 (Grammar):
  grammar = (REF('subgrammar', default=G1))

# The following are used by the test_resolve_* tests:

class RG0 (Grammar):
  grammar = (REF('subgrammar'))

class RG1 (Grammar):
  grammar = (REF('subgrammar'))

class RG2 (Grammar):
  grammar = (REF('subgrammar'))

class RG3 (Grammar):
  grammar = (REF('RG3'), REF('RG4'), REF('RG5'), REF('RG6'))

class RG4 (Grammar):
  grammar = (RG3, REF('RG3'))

RG5 = REF('RG3')

RG6 = RG3

class RG7 (Grammar):
  grammar = (REPEAT(REF('RG8'), min=3, max=5))

class RG8 (Grammar):
  grammar = (L('a'))

class GeneralRefTests (util.TestCase):
  def test_basic_ref(self):
    o = G0.parser().parse_string('a')
    self.assertIsInstance(o, G0)
    self.assertIsInstance(o.elements[0], G1)

  def test_override(self):
    o = G0.parser({'G1': G2}).parse_string('b')
    self.assertIsInstance(o, G0)
    self.assertIsInstance(o.elements[0], G2)

  def test_func_override(self):
    class SessionData:
      def grammar_resolve_ref(self, ref):
        return G2

    data = SessionData()
    o = G0.parser(data).parse_string('b')
    self.assertIsInstance(o, G0)
    self.assertIsInstance(o.elements[0], G2)

  def test_null_override(self):
    o = G0.parser({'G1': None}).parse_string('a')
    self.assertIsInstance(o, G0)
    self.assertIsInstance(o.elements[0], G1)
  
  def test_default(self):
    o = G4.parser().parse_string('a')
    self.assertIsInstance(o, G4)
    self.assertIsInstance(o.elements[0], G1)
    o = G4.parser({'subgrammar': G2}).parse_string('b')
    self.assertIsInstance(o, G4)
    self.assertIsInstance(o.elements[0], G2)
  
  def test_null_override_with_default(self):
    o = G4.parser({'subgrammar': None}).parse_string('a')
    self.assertIsInstance(o, G4)
    self.assertIsInstance(o.elements[0], G1)
  
  def test_unknown_ref(self):
    with self.assertRaises(UnknownReferenceError):
      o = G3.parser().parse_string('a')

  def test_invalid_override(self):
    with self.assertRaises(BadReferenceError):
      o = G0.parser({'G1': self}).parse_string('a')

  def test_resolve_unknown(self):
    with self.assertRaises(UnknownReferenceError):
      RG0.grammar_resolve_refs()

  def test_resolve_missingok(self):
    RG1.grammar_resolve_refs(missing_ok=True)
    self.assertIsSubclass(RG1.grammar[0], Reference)

  def test_resolve_with_refmap(self):
    RG2.grammar_resolve_refs(refmap={'subgrammar': G1}, recurse=False, follow=False)
    self.assertIs(RG2.grammar[0], G1)

  def test_resolve_selfref(self):
    RG3.grammar_resolve_refs(recurse=True, follow=True)
    self.assertIs(RG3.grammar[0], RG3)
    self.assertIs(RG3.grammar[1], RG4)
    self.assertIs(RG3.grammar[2], RG3)
    self.assertIs(RG3.grammar[3], RG3)
    self.assertIs(RG4.grammar[0], RG3)
    self.assertIs(RG4.grammar[1], RG3)

  def test_resolve_repeating(self):
    RG7.grammar_resolve_refs()
    g = RG7.grammar[0]
    self.assertIs(g.grammar[0], RG8)
    self.assertIs(g.grammar[1], RG8)
    self.assertIsInstance(g.grammar, RepeatingTuple)
    self.assertEqual(len(g.grammar), 5)
