from modgrammar import *
from .. import util

class G1 (Grammar):
  grammar = (L('a'))

class G2 (Grammar):
  grammar = (REF('G1'))

class G3 (Grammar):
  grammar = (REF('G1'))

G4 = REF('G1')

class G5 (Grammar):
  grammar = (REF('G6'))

class G6 (Grammar):
  grammar = (REF('G1'))

class G0 (Grammar):
  grammar = (REF('G1'), G2, REF('G3'), REF('G4'), REF('G5'))


G0.grammar_resolve_refs(recurse=False, follow=True)


class ResolveRefTests (util.TestCase):
  def test_toplevel(self):
    self.assertIs(G0.grammar[0], G1)
    self.assertIs(G0.grammar[1], G2)
    self.assertIs(G0.grammar[2], G3)
    self.assertIs(G0.grammar[3], G1)
    self.assertIs(G0.grammar[4], G5)

  def test_sublevel(self):
    self.assertIsSubclass(G2.grammar[0], Reference)
    self.assertIsSubclass(G3.grammar[0], Reference)
    self.assertIsSubclass(G5.grammar[0], Reference)
    self.assertIsSubclass(G6.grammar[0], Reference)

  def test_parse(self):
    o = G0.parser().parse_string('aaaaa')
    self.assertIsNotNone(o)

