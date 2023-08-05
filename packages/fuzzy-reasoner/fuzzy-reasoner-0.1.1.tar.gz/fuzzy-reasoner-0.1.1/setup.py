# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fuzzy_reasoner',
 'fuzzy_reasoner.prover',
 'fuzzy_reasoner.prover.operations',
 'fuzzy_reasoner.types']

package_data = \
{'': ['*']}

install_requires = \
['immutables>=0.17,<0.18', 'numpy>=1.21.1,<2.0.0']

setup_kwargs = {
    'name': 'fuzzy-reasoner',
    'version': '0.1.1',
    'description': 'Simple symbolic reasoner which supports fuzzy unification',
    'long_description': '# Fuzzy Reasoner\n\n[![ci](https://img.shields.io/github/workflow/status/chanind/fuzzy-reasoner/CI/main)](https://github.com/chanind/fuzzy-reasoner)\n[![Codecov](https://img.shields.io/codecov/c/github/chanind/fuzzy-reasoner/main)](https://codecov.io/gh/chanind/fuzzy-reasoner)\n[![PyPI](https://img.shields.io/pypi/v/fuzzy-reasoner?color=blue)](https://pypi.org/project/fuzzy-reasoner/)\n\n\nA simple symbolic reasoner which allows fuzzy unification based on embedding comparisons.\n\nThis projects takes ideas and inspiration from the following papers:\n\n- [End-to-End Differentiable Proving](https://arxiv.org/abs/1705.11040) by Rocktäschel et al.\n- [Braid - Weaving Symbolic and Neural Knowledge into Coherent Logical Explanations](https://arxiv.org/abs/2011.13354) by Kalyanpur et al.\n\nThank you so much to the authors of these papers!\n\n## Installation\n\n```\npip install fuzzy-reasoner\n```\n\n## Limitations and issues\n\nThis library is still very much in beta and may change its public API at any time before reaching version 1.0, so it\'s recommended to pin the exact version before then.\n\nThis library is currently limited to only use a rule once in a proof as a way to avoid cycles in the proof graph. This restriction should be fixed soon though, as this restriction does limit the usefulness of the library.\n\nThis library is pure Python, and is not highly optimized code. If you need a high-performance mature solver this package is likely not a great fit. However, pull requests are welcome if you\'d like to contribute and help make this library higher-performance!\n\n## Usage\n\nfuzzy-reasoner can be used either as a standard symbolic reasoner, or it can be used with fuzzy unification.\n\nThe setup works similar to prolog, except with python objects representing each component. A simple example of how this works is shown below:\n\n```python\nimport numpy as np\nfrom fuzzy_reasoner import SLDProver, Atom, Rule, Constant, Predicate, Variable\n\nX = Variable("X")\nY = Variable("Y")\nZ = Variable("Z")\n# predicates and constants can be given an embedding array for fuzzy unification\ngrandpa_of = Predicate("grandpa_of", np.array([1.0, 1.0, 0.0, 0.3, ...]))\ngrandfather_of = Predicate("grandfather_of", np.array([1.01, 0.95, 0.05, 0.33, ...]))\nparent_of = Predicate("parent_of", np.array([ ... ]))\nfather_of = Predicate("father_of", np.array([ ... ]))\nbart = Constant("bart", np.array([ ... ]))\nhomer = Constant("homer", np.array([ ... ]))\nabe = Constant("abe", np.array([ ... ]))\n\nrules = [\n    # base facts\n    Rule(parent_of(homer, bart)),\n    Rule(father_of(abe, homer)),\n    # theorems\n    Rule(grandpa_of(X, Y), (father_of(X, Z), parent_of(Z, Y)))\n]\n\nreasoner = SLDReasoner(rules=rules)\n\n# query the reasoner to find who is bart\'s grandfather\nproof = reasoner.prove(grandfather_of(X, bart))\n\n# even though `grandpa_of` and `grandfather_of` are not identical symbols,\n# their embedding is close enough that the reasoner can still find the answer\nprint(proof.variable_bindings[X]) # abe\n\n# the reasoner will return `None` if the proof could not be solved\nfailed_proof = reasoner.prove(grandfather_of(bart, homer))\nprint(failed_proof) # None\n\n```\n\nIf you don\'t want to use fuzzy unification, you can just not pass in an embedding array when creating a `Predicate` or `Constant`, and the reasoner will just do a plain string equality comparison for unification.\n\n```python\n# constants and predicates can be defined without an embedding array for strict (non-fuzzy) unification\ngrandpa_of = Predicate("grandpa_of")\nbart = Constant("bart")\n```\n\n### Custom matching functions and similarity thresholds\n\nBy default, the reasoner will use cosine similarity for unification. If you\'d like to use a different similarity function, you can pass in a function to the reasoner to perform the similarity calculation however you wish.\n\n```python\n\ndef fancy_similarity(item1, item2):\n    norm = np.linalg.norm(item1.vector) + np.linalg.norm(item2.vector)\n    return np.linalg.norm(item1.vector - item2.vector) / norm\n\nreasoner = SLDReasoner(rules=rules, similarity_func=fancy_similarity)\n```\n\nBy default, there is a minimum similarity threshold of `0.5` for a unification to success. You can customize this as well when creating a `SLDReasoner` instance\n\n```python\nreasoner = SLDReasoner(rules=rules, min_similarity_threshold=0.9)\n```\n\n### Max proof depth\n\nBy default, the SLDReasoner will abort proofs after a depth of 10. You can customize this behavior by passing `max_proof_depth` when creating the reasoner\n\n```python\nreasoner = SLDReasoner(rules=rules, max_proof_depth=10)\n```\n\n## Contributing\n\nContributions are welcome! Please leave an issue in the Github repo if you find any bugs, and open a pull request with and fixes or improvements that you\'d like to contribute.\n\n## Happy solving!\n',
    'author': 'David Chanin',
    'author_email': 'chanindav@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chanind/fuzzy-reasoner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
