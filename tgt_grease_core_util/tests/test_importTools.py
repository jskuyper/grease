from unittest import TestCase
from tgt_grease_core_util import ImportTools
import collections
from tgt_grease_core_util import Logging

class test_importTools(TestCase):
    def test_load(self):
        obj = ImportTools.Importer(Logging.Logger())
        loaded_module = obj.load('collections', 'defaultdict', True)
        self.assertEqual(type(loaded_module), collections.defaultdict)
        del obj, loaded_module

    def test_attribute_err(self):
        obj = ImportTools.Importer(Logging.Logger())

        def load_the_mod(obj2):
            obj2.load('collections', 'defeaultdict1', True)
        self.assertRaises(AttributeError, load_the_mod(obj))
        del obj

    def test_import_err(self):
        obj = ImportTools.Importer(Logging.Logger())

        def load_the_mod(obj2):
            obj2.load('collections1', 'defeaultdict', True)
        self.assertRaises(ImportError, load_the_mod(obj))
        del obj
