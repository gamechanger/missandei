from unittest import TestCase
from transl8.translator import Translator, get_value_at_path, set_value_at_path


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
        found, value = get_value_at_path({'a': 1}, 'a')
        self.assertTrue(found)
        self.assertEqual(value, 1)

    def test_value_at_root_missing(self):
        found, value = get_value_at_path({'a': 1}, 'b')
        self.assertFalse(found)
        self.assertEqual(value, None)

    def test_value_at_leaf(self):
        found, value = get_value_at_path({'a': {'b': {'c': 2}}}, 'a.b.c')
        self.assertTrue(found)
        self.assertEqual(value, 2)

    def test_value_at_leaf_missing(self):
        found, value = get_value_at_path({'a': {'b': {'d': 2}}}, 'a.b.c')
        self.assertFalse(found)
        self.assertEqual(value, None)

    def test_branch_missing(self):
        found, value = get_value_at_path({'a': {'d': {'c': 2}}}, 'a.b.c')
        self.assertFalse(found)
        self.assertEqual(value, None)

    def test_expected_branch_is_not_a_branch(self):
        found, value = get_value_at_path({'a': {'b': 'a string'}}, 'a.b.c')
        self.assertFalse(found)
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
            'b': 'c',
            'd': 'e.f',
            'g.h.i': 'j.k'
        })

    def test_backward(self):
        end = {
            'a': 1,
            'c': 2,
            'e': {'f': 3},
            'j': {'k': 4}
        }
        expected = {
            'a': 1,
            'b': 2,
            'd': 3,
            'g': {'h': {'i': 4}}
        }
        self.assertEqual(expected, self.translator.backward(end))

    def test_forward(self):
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
        self.assertEqual(expected, self.translator.forward(start))


    def test_forward_with_missing_start_fields(self):
        start = {
            'a': 1,
            'd': 3,
            'g': {'h': {'i': 4}}
        }
        expected = {
            'a': 1,
            'e': {'f': 3},
            'j': {'k': 4}
        }
        self.assertEqual(expected, self.translator.forward(start))

    def test_forward_with_incorrectly_typed_branch_nodes(self):
        start = {
            'a': 1,
            'b': 2,
            'd': 3,
            'g': {'h': 'string'}
        }
        expected = {
            'a': 1,
            'c': 2,
            'e': {'f': 3}
        }
        self.assertEqual(expected, self.translator.forward(start))

