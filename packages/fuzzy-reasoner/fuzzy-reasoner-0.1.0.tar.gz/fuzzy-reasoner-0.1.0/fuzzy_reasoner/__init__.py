__version__ = "0.1.0"

from .prover.SLDProver import SLDProver

from .types.Atom import Atom
from .types.Constant import Constant
from .types.Predicate import Predicate
from .types.Rule import Rule
from .types.Variable import Variable

from .similarity import cosine_similarity, symbol_compare
