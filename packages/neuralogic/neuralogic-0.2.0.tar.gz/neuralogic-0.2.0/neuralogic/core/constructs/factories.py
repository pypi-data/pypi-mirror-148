from typing import Dict
from neuralogic.core.constructs.predicate import Predicate
from neuralogic.core.constructs import atom


class AtomFactory:
    class Predicate:
        def __init__(self, hidden=False, special=False):
            self.is_hidden = hidden
            self.is_special = special

        @property
        def special(self) -> "AtomFactory.Predicate":
            return AtomFactory.Predicate(self.is_hidden, True)

        @property
        def hidden(self) -> "AtomFactory.Predicate":
            return AtomFactory.Predicate(True, self.is_special)

        @staticmethod
        def get_predicate(name, arity, hidden, special) -> Predicate:
            return Predicate(name, arity, hidden, special)

        def __getattr__(self, item):
            return atom.BaseAtom(Predicate(item, 0, self.is_hidden, self.is_special))

    def __init__(self):
        self.instances: Dict[str, Dict[int, atom.BaseAtom]] = {}

        self.special = AtomFactory.Predicate(special=True)
        self.hidden = AtomFactory.Predicate(hidden=True)

    def get(self, name: str) -> atom.BaseAtom:
        return atom.BaseAtom(Predicate(name, 0, False, False))

    def __getattr__(self, item) -> atom.BaseAtom:
        return atom.BaseAtom(Predicate(item, 0, False, False))


class VariableFactory:
    def __getattr__(self, item) -> str:
        return item.upper()


class TermFactory:
    def __getattr__(self, item) -> str:
        return item.lower()


Var = VariableFactory()
Relation = AtomFactory()
Term = TermFactory()

V = Var
T = Term
R = Relation
