import contextlib
import io
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from csv_reconcile_kit import reconcile, close_enough, main

class ReconcileTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.a, self.b = Path(self.tmp.name)/'a.csv', Path(self.tmp.name)/'b.csv'
    def files(self, a, b):
        self.a.write_text(a, encoding='utf-8')
        self.b.write_text(b, encoding='utf-8')
    def test_reorder_and_composite_keys(self):
        self.files('id,region,v\n1,eu,a\n1,us,b', 'v,region,id\nb,us,1\na,eu,1')
        self.assertFalse(any(reconcile(self.a, self.b, ['id', 'region']).values()))
    def test_add_remove_change_schema(self):
        self.files('id,v\n1,a\n2,b', 'id,v,x\n1,c,z\n3,d,w')
        result = reconcile(self.a, self.b, ['id'])
        self.assertEqual(result['changed'][0]['fields']['v'], {'before': 'a', 'after': 'c'})
        self.assertEqual(result['columns_added'], ['x'])
        self.assertEqual(result['removed'][0]['id'], '2')
        self.assertEqual(result['added'][0]['id'], '3')
    def test_decimal_tolerance(self):
        self.files('id,v\n1,0.10', 'id,v\n1,0.11')
        self.assertFalse(any(reconcile(self.a, self.b, ['id'], tolerances={'v': Decimal('.01')}).values()))
        self.assertFalse(close_enough('NaN', '0', Decimal(1)))
        self.assertFalse(close_enough('abc', '1', Decimal(1)))
    def test_duplicate_fails(self):
        self.files('id,v\n1,a\n1,b', 'id,v\n1,a')
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            reconcile(self.a, self.b, ['id'])
    def test_bad_headers_width_empty_keys(self):
        for bad in ['id,id\n1,1', 'id,v\n1,a,x', 'id,v\n,a', '']:
            self.files(bad, 'id,v\n1,a')
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                reconcile(self.a, self.b, ['id'])
    def test_multiline_unicode(self):
        text = 'id,v\n1,"hello\n世界"'
        self.files(text, text)
        self.assertFalse(any(reconcile(self.a, self.b, ['id']).values()))
    def test_ignore(self):
        self.files('id,v\n1,a', 'id,v\n1,b')
        self.assertFalse(any(reconcile(self.a, self.b, ['id'], ['v']).values()))
    def test_invalid_options(self):
        self.files('id,v\n1,a', 'id,v\n1,b')
        for kwargs in [{'ignore':['missing']}, {'ignore':['id']}, {'tolerances':{'v':Decimal('-1')}}]:
            with self.assertRaises(ValueError):
                reconcile(self.a, self.b, ['id'], **kwargs)
    def test_cli_status(self):
        self.files('id,v\n1,a', 'id,v\n1,b')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main([str(self.a), str(self.b), '--key', 'id']), 1)
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main([str(self.a), str(self.b), '--key', 'id', '--tolerance', 'v=NaN']), 2)
