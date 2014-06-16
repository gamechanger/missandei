from unittest import TestCase
from transl8.translator import Translator


class TranslatorTest(TestCase):
    def test_valid_spec(self):
        Translator({
            "some_field": "some_other_field"
        })

    def test_disallows_non_string_to_field(self):
        with self.assertRaises(Exception):
            Translator({
                "some_field": {"a": "dict"}
            })
