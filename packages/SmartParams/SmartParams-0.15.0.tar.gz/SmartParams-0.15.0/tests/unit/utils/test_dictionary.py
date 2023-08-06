import smartparams.utils.dictionary as dictutil
from tests.unit import UnitCase


class TestFindNested(UnitCase):
    def setUp(self) -> None:
        self.dict = dict(arg1='arg1', arg2=['arg2'], arg3={'arg31': 'a31', 'arg32': 'a32'})

    def test(self) -> None:
        key = 'arg3.arg31'

        dictionary, last_key = dictutil.find_nested(dictionary=self.dict, key=key)

        self.assertEqual('arg31', last_key)
        self.assertTupleEqual((('arg31', 'a31'), ('arg32', 'a32')), tuple(dictionary.items()))

    def test__not_in_dictionary(self) -> None:
        key = 'missing.any'

        self.assertRaises(KeyError, dictutil.find_nested, dictionary=self.dict, key=key)

    def test__required_true(self) -> None:
        key = 'arg3.missing'

        self.assertRaises(
            KeyError,
            dictutil.find_nested,
            dictionary=self.dict,
            key=key,
            required=True,
        )

    def test__is_not_dictionary(self) -> None:
        key = 'arg3.arg31.a31'

        self.assertRaises(ValueError, dictutil.find_nested, dictionary=self.dict, key=key)

    def test__set_mode(self) -> None:
        key = 'arg3.missing.key'

        dictionary, last_key = dictutil.find_nested(
            dictionary=self.dict,
            key=key,
            set_mode=True,
        )

        self.assertIsInstance(dictionary, dict)
        self.assertFalse(bool(dictionary))
        self.assertEqual('key', last_key)

    def test__set_mode_not_is_not_dictionary(self) -> None:
        key = 'arg3.arg31.a31'

        dictionary, last_key = dictutil.find_nested(
            dictionary=self.dict,
            key=key,
            set_mode=True,
        )

        self.assertIsInstance(dictionary, dict)
        self.assertFalse(bool(dictionary))
        self.assertEqual('a31', last_key)
