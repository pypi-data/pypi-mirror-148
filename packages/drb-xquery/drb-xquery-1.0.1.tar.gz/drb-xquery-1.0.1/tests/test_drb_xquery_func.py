import os
import unittest
from pathlib import Path

from drb_impl_file import DrbFileFactory
from drb_impl_xml import XmlNodeFactory
from drb_xquery.drb_xquery import DrbXQuery
from drb_xquery.execptions import ErrorXQUERY, DynamicException


class TestDrbXQueryFunc(unittest.TestCase):
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))

    xml_file = current_path / "files" / "MTD_TL.xml"
    xml_file = str(xml_file)

    def test_xquery_func_count(self):

        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery("count(/Level-2A_Tile_ID/Test_FLF)")
        node_result = query.execute(self.node)

        self.assertListEqual(node_result, [6])

    def test_xquery_func_name(self):

        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery("/Level-2A_Tile_ID/name(Test_FLF)")
        node_result = query.execute(self.node)

        # get the name of first elt
        self.assertEqual(len(node_result), 1)

        query = DrbXQuery("/Level-2A_Tile_ID/Test_FLF/french")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 5)

        query = DrbXQuery("/Level-2A_Tile_ID/Test_FLF/*[name()='french']")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 5)

    def test_xquery_func_namespace(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery("/Level-2A_Tile_ID/name(Test_FLF)")
        node_result = query.execute(self.node)

        # get the name of first elt
        self.assertEqual(len(node_result), 1)

        query = DrbXQuery("/Level-2A_Tile_ID/Test_FLF/*[namespace-uri()='SA']")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 3)
        self.assertEqual(node_result[0].namespace_uri, 'SA')

        query = DrbXQuery(
            "/Level-2A_Tile_ID/General_Info[namespace-uri('test')='SA']")
        with self.assertRaises(DynamicException) as error_exception:
            node_result = query.execute(self.node)
        self.assertIn(repr(ErrorXQUERY.XPTY0004),
                      str(error_exception.exception))

    def test_xquery_func_starts_with(self):

        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery("/Level-2A_Tile_ID/"
                          "Test_FLF[starts-with(elt,'This')]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 2)
        self.assertEqual(node_result[0].node['elt', 0].value, 'This is one')
        self.assertEqual(node_result[1].node['elt', 0].value, 'This is 4')

        query = DrbXQuery("/Level-2A_Tile_ID/"
                          "Test_FLF[starts-with(elt,'This', '4')]")

        with self.assertRaises(DynamicException) as error_exception:
            node_result = query.execute(self.node)

        self.assertIn(repr(ErrorXQUERY.FOAP0001),
                      str(error_exception.exception))

        query = DrbXQuery("/Level-2A_Tile_ID/"
                          "Test_FLF[starts-with(no_exists,'This')]")

        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 0)

        query = DrbXQuery("/Level-2A_Tile_ID/"
                          "Test_FLF[starts-with(elt,'no_found')]")

        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 0)

    def test_xquery_func_ends_with(self):

        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery("/Level-2A_Tile_ID/"
                          "Test_FLF[ends-with(elt,'4') or ends-with(elt,',')]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 2)
        self.assertEqual(node_result[0].node['elt', 0].value, 'I m three 3,')
        self.assertEqual(node_result[1].node['elt', 0].value, 'This is 4')

        query = DrbXQuery("/Level-2A_Tile_ID/"
                          "Test_FLF[ends-with(@no_exists, '4') or "
                          "ends-with(not_exist,',')]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 0)

    def test_xquery_func_contains(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[contains(@atr,'attri')]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 2)
        self.assertEqual(node_result[0].node['name'].value, 'third')
        self.assertEqual(node_result[1].node['name'].value, 'third_doublon')

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[contains(@atr_not_exist,'attri')]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 0)

    def test_xquery_func_true(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[contains(@atr,'attri') and true()]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 2)
        self.assertEqual(node_result[0].node['name'].value, 'third')
        self.assertEqual(node_result[1].node['name'].value, 'third_doublon')

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[contains(@atr,'attri') or true()]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 6)

    def test_xquery_func_false(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[contains(@atr,'attri') and false()]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 0)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[contains(@atr,'attri') or false()]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 2)
        self.assertEqual(node_result[0].node['name'].value, 'third')
        self.assertEqual(node_result[1].node['name'].value, 'third_doublon')

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[contains(@atr_not_exist,'attri')]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 0)

    def test_xquery_func_not(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[not(contains(@atr,'attri'))]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 4)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[not(elt)]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 0)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[not('0')]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 6)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[not(elt)]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 0)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[not(1)]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 0)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[not(0)]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 6)

    def test_xquery_func_match(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[matches(elt,'^.*[1-9]+$')]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 2)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[matches(elt,'.*[1-9]+')]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 2)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[matches(@no_exists,'.*[1-9]+')]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 0)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[matches(elt,'.*[1-9]notexist+')]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 0)

    def test_xquery_position(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/General_Info[myday = 2][position() = 1]"
            "/L1C_TILE_ID")

        node_result = query.execute(self.node)

        print("len :" + str(len(node_result)))
        self.assertEqual(len(node_result), 3)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/General_Info[myday = 2]"
            "[position() > 0]/"
            "L1C_TILE_ID")

        node_result = query.execute(self.node)

        print("len :" + str(len(node_result)))
        self.assertEqual(len(node_result), 3)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/General_Info[myday = 2]/"
            "L1C_TILE_ID[position() > 1 and position() < 3]")

        node_result = query.execute(self.node)

        print("len :" + str(len(node_result)))
        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0].value,
                         "S2B_OPER_MSI_L1C_TL_VGS4_20210913T120150_A023615_"
                         "T30UWU_N03.02_day2")

    def test_xquery_func_substring(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[substring(elt, 6, 2) = 'is']")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 2)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[substring(elt, 5.5, 2.4) = 'is']")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 2)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[substring(elt, 4.8, 3) = 'two']")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)

    def test_xquery_func_string_length(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[string-length(number) = 3]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 4)

    def test_xquery_func_exists(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[exists(@atr)]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 5)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[exists(@atr_not_exists)]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 0)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[exists(elt)]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 6)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[exists(elt_not)]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 0)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[exists('1')]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 6)

    def test_xquery_func_empty(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[empty(@atr)]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[empty(@atr_not_exists)]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 6)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[exists(elt)]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 6)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[empty(elt_not)]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 6)

    def test_xquery_func_avg(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "avg(2, 4, 4, 5, 0)")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0], 3)

        query = DrbXQuery(
            "avg(2, 0.4e1, 4.5, 3.5, 1)")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0], 3)

        query = DrbXQuery(
                "avg('a', 0.4e1, 4.5, 3.5, 1)")
        with self.assertRaises(DynamicException) as error_exception:
            node_result = query.execute(self.node)
        self.assertIn(repr(ErrorXQUERY.FORG0006),
                      str(error_exception.exception))

        query = DrbXQuery(
            "/Level-2A_Tile_ID/avg(Test_FLF/@occurence)")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0], 3.5)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[avg(2, 4)]/@occurence")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0].value, '3')

    def test_xquery_func_sum(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "sum(2, 4, 4, 5, 0)")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0], 15)

        query = DrbXQuery(
            "sum(2, 0.4e1, 4.5, 3.5, 1)")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0], 15)

        query = DrbXQuery(
                "sum('a', 0.4e1, 4.5, 3.5, 1)")
        with self.assertRaises(DynamicException) as error_exception:
            node_result = query.execute(self.node)
        self.assertIn(repr(ErrorXQUERY.FORG0006),
                      str(error_exception.exception))

        query = DrbXQuery(
            "/Level-2A_Tile_ID/sum(Test_FLF/@occurence)")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0], 21)

    def test_xquery_func_max(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "max(2, 4, 4, 5, 0)")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0], 5)

        query = DrbXQuery(
            "max(2, 0.4e1, 4.5, 3.5, 1)")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0], 4.5)

        query = DrbXQuery(
                "max('a', 0.4e1, 4.5, 3.5, 1)")
        with self.assertRaises(DynamicException) as error_exception:
            node_result = query.execute(self.node)
        self.assertIn(repr(ErrorXQUERY.FORG0006),
                      str(error_exception.exception))

        query = DrbXQuery(
            "/Level-2A_Tile_ID/max(Test_FLF/@occurence)")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0], '6')

    def test_xquery_func_min(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "min(2, 4, 4, 5, 0)")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0], 0)

        query = DrbXQuery(
            "min(2, 0.4e1, 4.5, -3.5, 1)")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0], -3.5)

        query = DrbXQuery(
                "min('a', 0.4e1, 4.5, 3.5, 1)")
        with self.assertRaises(DynamicException) as error_exception:
            node_result = query.execute(self.node)
        self.assertIn(repr(ErrorXQUERY.FORG0006),
                      str(error_exception.exception))

        query = DrbXQuery(
            "/Level-2A_Tile_ID/min(Test_FLF/@occurence)")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0], '1')

    def test_xquery_func_ceiling(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "ceiling(2.4)")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0], 3.0)

        query = DrbXQuery(
            "ceiling(3.9)")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0], 4.0)

        query = DrbXQuery("ceiling('a')")
        with self.assertRaises(DynamicException) as error_exception:
            node_result = query.execute(self.node)
        self.assertIn(repr(ErrorXQUERY.FORG0006),
                      str(error_exception.exception))

        query = DrbXQuery("ceiling(2, 3)")
        with self.assertRaises(DynamicException) as error_exception:
            node_result = query.execute(self.node)
        self.assertIn(repr(ErrorXQUERY.FOAP0001),
                      str(error_exception.exception))

    def test_xquery_func_floor(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "floor(2.4)")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0], 2)

        query = DrbXQuery(
            "floor(3.9)")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0], 3)

        query = DrbXQuery("floor('a')")
        with self.assertRaises(DynamicException) as error_exception:
            node_result = query.execute(self.node)
        self.assertIn(repr(ErrorXQUERY.FORG0006),
                      str(error_exception.exception))

        query = DrbXQuery("floor(2, 3)")
        with self.assertRaises(DynamicException) as error_exception:
            node_result = query.execute(self.node)
        self.assertIn(repr(ErrorXQUERY.FOAP0001),
                      str(error_exception.exception))

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_num/floor(num_to_test)")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 2)
        self.assertEqual(node_result[0], 3)
        self.assertEqual(node_result[1], 6)

    def test_xquery_func_abs(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)
        query = DrbXQuery(
            "abs(-2.56e10)")
        node_result = query.execute(self.node)
        self.assertEqual(float(node_result[0]), 2.56e10)

        query = DrbXQuery(
            "abs(-2.4)")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(float(node_result[0]), 2.4)

        query = DrbXQuery(
            "abs(3.9)")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(float(node_result[0]), 3.9)

        query = DrbXQuery("abs('a')")
        with self.assertRaises(DynamicException) as error_exception:
            node_result = query.execute(self.node)
        self.assertIn(repr(ErrorXQUERY.FORG0006),
                      str(error_exception.exception))

        query = DrbXQuery("abs(2, 3)")
        with self.assertRaises(DynamicException) as error_exception:
            node_result = query.execute(self.node)
        self.assertIn(repr(ErrorXQUERY.FOAP0001),
                      str(error_exception.exception))

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_num/abs(num_signed_to_test)")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 2)
        self.assertEqual(node_result[0], 3.4)
        self.assertEqual(node_result[1], 6.9)

    def test_xquery_func_round(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "round(-2.4)")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0], -2)

        query = DrbXQuery(
            "round(3.9)")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0], 4)

        query = DrbXQuery("round('a')")
        with self.assertRaises(DynamicException) as error_exception:
            node_result = query.execute(self.node)
        self.assertIn(repr(ErrorXQUERY.FORG0006),
                      str(error_exception.exception))

        query = DrbXQuery("round(2, 3)")
        with self.assertRaises(DynamicException) as error_exception:
            node_result = query.execute(self.node)
        self.assertIn(repr(ErrorXQUERY.FOAP0001),
                      str(error_exception.exception))

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_num/round(abs(num_signed_to_test))")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 2)
        self.assertEqual(node_result[0], 3)
        self.assertEqual(node_result[1], 7)

    def test_xquery_func_doc(self):
        query = DrbXQuery("count(doc('" + self.xml_file + "')" +
                          "/Level-2A_Tile_ID/Test_FLF)")
        node_result = query.execute(None)

        self.assertListEqual(node_result, [6])
