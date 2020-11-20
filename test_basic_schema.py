# test some ideas that support a basic self aware schema parsing of the files
# Work out if re-using https://pypi.org/project/schema/ makes more sense to check files as we load them
#
from schema import Schema, And, Use, Optional


def test_kids():
# a stupid test case, to play with
    schema = Schema([{'name': And(str, len),
                      'age':  And(Use(int), lambda n: 18 <= n <= 99),

    Optional('gender'): And(str, Use(str.lower),

    lambda s: s in ('squid', 'kid'))}])

    data = [{'name': 'Sue', 'age': '28', 'gender': 'Squid'},
            {'name': 'Sam', 'age': '42'},
            {'name': 'Sacha', 'age': '20', 'gender': 'KID'}]

    validated = schema.validate(data)

    assert validated == [{'name': 'Sue', 'age': 28, 'gender': 'squid'},
                              {'name': 'Sam', 'age': 42},
                              {'name': 'Sacha', 'age': 20, 'gender': 'kid'}]

