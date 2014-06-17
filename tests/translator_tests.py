from unittest import TestCase
from missandei.translator import Translator, get_value_at_path, set_value_at_path


class TranslatorValidationTest(TestCase):
    def test_valid_spec(self):
        Translator({
            "some_field": "some_other_field"
        })

    def test_disallows_non_string_to_field(self):
        with self.assertRaises(Exception):
            Translator({
                "some_field": {"a": "dict"}
            })


class TestGetValueAtPath(TestCase):
    def test_value_at_root(self):
        value = get_value_at_path('a', {'a': 1})
        self.assertEqual(value, 1)

    def test_value_at_root_missing(self):
        value = get_value_at_path('b', {'a': 1})
        self.assertEqual(value, None)

    def test_value_at_leaf(self):
        value = get_value_at_path('a.b.c', {'a': {'b': {'c': 2}}})
        self.assertEqual(value, 2)

    def test_value_at_leaf_missing(self):
        value = get_value_at_path('a.b.c', {'a': {'b': {'d': 2}}})
        self.assertEqual(value, None)

    def test_branch_missing(self):
        value = get_value_at_path('a.b.c', {'a': {'d': {'c': 2}}})
        self.assertEqual(value, None)

    def test_expected_branch_is_not_a_branch(self):
        value = get_value_at_path('a.b.c', {'a': {'b': 'a string'}})
        self.assertEqual(value, None)


class TestSetValueAtPath(TestCase):
    def test_value_at_root(self):
        end = {}
        set_value_at_path(end, 'a', 1)
        self.assertEqual({'a': 1}, end)

    def test_value_nested(self):
        end = {}
        set_value_at_path(end, 'a.b.c', 1)
        self.assertEqual({'a': {'b': {'c': 1}}}, end)

    def test_value_nest_existing_branches(self):
        end = {'a': {'e': 3}, 'd': 2}
        set_value_at_path(end, 'a.b.c', 1)
        self.assertEqual({'a': {'b': {'c': 1}, 'e': 3}, 'd': 2}, end)



class TranslatorTest(TestCase):
    def setUp(self):
        self.translator = Translator({
            'a': 'a',
            'c': 'b',
            'e.f': 'd',
            'j.k': 'g.h.i'
        })

    def test_apply(self):
        start = {
            'a': 1,
            'b': 2,
            'd': 3,
            'g': {'h': {'i': 4}}
        }
        expected = {
            'a': 1,
            'c': 2,
            'e': {'f': 3},
            'j': {'k': 4}
        }
        self.assertEqual(expected, self.translator.apply(start))


    def test_apply_with_missing_start_fields(self):
        start = {
            'a': 1,
            'd': 3,
            'g': {'h': {'i': 4}}
        }
        expected = {
            'a': 1,
            'c': None,
            'e': {'f': 3},
            'j': {'k': 4}
        }
        self.assertEqual(expected, self.translator.apply(start))

    def test_apply_with_incorrectly_typed_branch_nodes(self):
        start = {
            'a': 1,
            'b': 2,
            'd': 3,
            'g': {'h': 'string'}
        }
        expected = {
            'a': 1,
            'c': 2,
            'e': {'f': 3},
            'j': {'k': None}
        }
        self.assertEqual(expected, self.translator.apply(start))

