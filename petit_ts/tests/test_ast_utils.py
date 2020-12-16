import random as rd
import unittest
from typing import Union

from ..ast_utils import AstFailure, get_variable_name, TooManyAssignments
from ..named_types import Named, get_extended_name, set_extended_name


class ASTUtilsTests(unittest.TestCase):
    def setUp(self):
        return super().setUp()

    def test_set_name(self):
        item = Named(Union[int, str])
        self.assertEqual(get_extended_name(item), 'item')

    def test_get_variable_name(self):
        def test():
            return get_variable_name()
        name = test()
        self.assertEqual('name', name)

    def test_missuse_get_variable_name(self):
        name = get_variable_name(with_raise=False)
        self.assertEqual(name, None)

        get_variable_name(with_raise=False)
        self.assertEqual(name, None)

    def test_other_missuse(self):
        def test():
            return get_variable_name(with_raise=True)
        with self.assertRaises(TooManyAssignments):
            a, b = test()

        def test():
            return get_variable_name(with_raise=True)
        a = {'test': 'deb'}
        with self.assertRaises(AstFailure):
            a['test'] = test()

    def test_without_raise(self):
        def test():
            return get_variable_name(with_raise=False)
        a = {'test': 'deb'}
        
        a['test'] = test()
        self.assertEqual(a['test'], None)

    def test_with_raise(self):
        def test():
            return get_variable_name(with_raise=True)
        
        with self.assertRaises(AstFailure):
            test()
