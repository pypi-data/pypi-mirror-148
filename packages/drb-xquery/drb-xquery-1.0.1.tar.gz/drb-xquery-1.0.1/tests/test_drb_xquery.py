import os
import unittest
from decimal import Decimal
from pathlib import Path

from drb_impl_file import DrbFileFactory
from drb_impl_xml import XmlNodeFactory
from drb_xquery.drb_xquery import DrbXQuery
from drb_xquery.drb_xquery_utils import DrbQueryFuncUtil


class NodeTest:
    def __init__(self):
        self.value = 'test'


class TestDrbXQuery(unittest.TestCase):
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))

    xml_file = current_path / "files" / "MTD_TL.xml"
    xml_file = str(xml_file)

    def test_xml(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)
        #
        # self.node_file = DrbHttpFactory().create(self.xml_file)
        # self.node = XmlNodeFactory().create(self.node_file)

        print(len(self.node))
        # self.assertEqual(len(self.node), 1)

        self.assertEqual(self.node[0].name, "Level-2A_Tile_ID")
        print(self.node[0]["General_Info"]['L1C_TILE_ID'].value)
        print(self.node[0]["General_Info", 'nc3'].namespace_uri)

    def test_xquery_simple(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID")

        node_result = query.execute(self.node)
        print(node_result[0].value)

        self.assertTrue(node_result[0].name,
                        "Level-2A_Tile_ID")

    def test_xquery_double(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "123E+14")

        node_result = query.execute(self.node)
        self.assertEqual(node_result[0], 123e+14)

    def test_xquery_decimal(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)
        query = DrbXQuery(
            "1.40")

        node_result = query.execute(self.node)
        self.assertEqual(node_result[0], Decimal('1.40'))

    def test_xquery_last(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/General_Info[myday = 1]/L1C_TILE_ID[last()]")

        node_result = query.execute(self.node)
        print(node_result[0].value)

        self.assertTrue(node_result[0].value,
                        "S2B_OPER_MSI_L1C_TL_VGS4_20210913T120150_"
                        "A023615_T30UWU_N03.03")

    def test_xquery_index(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/General_Info[myday = 1]/L1C_TILE_ID[2]")

        node_result = query.execute(self.node)

        print(node_result[0].value)
        self.assertTrue(node_result[0].value,
                        "S2B_OPER_MSI_L1C_TL_VGS4_20210913T120150_")

    def test_xquery_string(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[\"A\"]")

        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 6)

    def test_xquery_sequence(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[3, 5]")

        node_result = query.execute(self.node)
        self.assertEqual(len(node_result), 2)

        self.assertTrue(node_result[0].name, "second")
        self.assertTrue(node_result[1].name, "first_doublon")

        # query = DrbXQuery(
        #     "/Level-2A_Tile_ID/Test_FLF[serie='A', number='one']")
        # node_result = query.execute(self.node)
        #
        # self.assertEqual(len(node_result), 4)
        #
        # query = DrbXQuery(
        #     "/Level-2A_Tile_ID/Test_FLF[serie='A', 4, 5]")
        # node_result = query.execute(self.node)
        #
        # self.assertEqual(len(node_result), 5)

    def test_xquery_range(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[2 to 4]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 3)
        self.assertTrue(node_result[0].name, "third")
        self.assertTrue(node_result[2].name, "second_doublon")

    def test_xquery_range_and_index(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[2 to 4, 5]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 4)
        self.assertTrue(node_result[0].name, "third")
        self.assertTrue(node_result[2].name, "second_doublon")

    def test_xquery_equal(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/General_Info[myday = 2]/L1C_TILE_ID[1]")

        node_result = query.execute(self.node)

        print(node_result[0].value)
        self.assertTrue(node_result[0].value,
                        "S2B_OPER_MSI_L1C_TL_VGS4_20210913T120150_"
                        "A023615_T30UWU_N03.01_day2")

    def test_xquery_greater(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/General_Info[myday = 2]/"
            "L1C_TILE_ID[position() > 2]")

        node_result = query.execute(self.node)

        print("len :" + str(len(node_result)))
        self.assertEqual(len(node_result), 1)

    def test_xquery_wilcard(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/*/SENSING_TIME")

        node_result = query.execute(self.node)

        print("len :" + str(len(node_result)))
        self.assertEqual(len(node_result), 3)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/*/NOT_EXIST")

        node_result = query.execute(self.node)
        self.assertEqual(len(node_result), 0)

    def test_xquery_attribute(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/General_Info[@month=11]/myday")

        node_result = query.execute(self.node)

        print("len :" + str(len(node_result)))
        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0].value, "2")

    def test_xquery_namespace(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/nc3:General_Info[@month=11]/myday")

        node_result = query.execute(self.node)

        print("len :" + str(len(node_result)))
        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0].value, "2")

        query = DrbXQuery(
            "/Level-2A_Tile_ID/nc2:General_Info")

        node_result = query.execute(self.node)
        self.assertEqual(len(node_result), 0)

    def test_xquery_before_last(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/General_Info[myday = 1]/L1C_TILE_ID[last()-1]")

        node_result = query.execute(self.node)
        print(node_result[0].value)

        self.assertTrue(node_result[0].value,
                        "S2B_OPER_MSI_L1C_TL_VGS4_20210913T120150_"
                        "A023615_T30UWU_N03.02")

    def test_xquery_wilcard_attribute(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/General_Info[@*=11]/myday")

        node_result = query.execute(self.node)

        print("len :" + str(len(node_result)))
        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0].value, "2")

        query = DrbXQuery(
            "/Level-2A_Tile_ID/General_Info[@*=14]/myday")

        node_result = query.execute(self.node)
        self.assertEqual(len(node_result), 0)

    def test_xquery_axe_child(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/child::General_Info/myday")

        node_result = query.execute(self.node)

        print("len :" + str(len(node_result)))
        self.assertEqual(len(node_result), 2)
        self.assertEqual(node_result[0].value, "1")
        self.assertEqual(node_result[1].value, "2")

        self.node_file.close()
        self.node.close()

    def test_xquery_axe_attribute(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/General_Info/attribute::month")

        node_result = query.execute(self.node)

        print("len :" + str(len(node_result)))
        self.assertEqual(node_result[0].value, "01")
        self.assertEqual(node_result[1].value, "11")

    def test_xquery_axe_following(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/General_Info/following::month")
        with self.assertRaises(NotImplementedError):
            query.execute(self.node)

    def test_xquery_axe_not_exist(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/General_Info/test::myday")
        node_result = query.execute(self.node)
        self.assertEqual(len(node_result), 0)

        # if we ask an axe that not exist the
        query = DrbXQuery(
            "/Level-2A_Tile_ID/General_Info/myday::test")
        node_result = query.execute(self.node)
        self.assertEqual(len(node_result), 2)

    def test_xquery_and(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            '/Level-2A_Tile_ID/Test_FLF[@name_attr="test_one"]')
        node_result = query.execute(self.node)
        self.assertEqual(len(node_result), 2)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[serie='B']")
        node_result = query.execute(self.node)
        self.assertEqual(len(node_result), 3)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[serie='B' and @name_attr='test_one']")
        node_result = query.execute(self.node)
        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0].node['name'].value, 'first_doublon')

    def test_xquery_or(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            '/Level-2A_Tile_ID/Test_FLF[@name_attr="test_two"]')
        node_result = query.execute(self.node)
        self.assertEqual(len(node_result), 2)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[serie='B']")
        node_result = query.execute(self.node)
        self.assertEqual(len(node_result), 3)
        self.assertEqual(node_result[0].node['serie'].value, 'B')

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[@name_attr='test_two' or serie='B']")
        node_result = query.execute(self.node)
        self.assertEqual(len(node_result), 4)

        self.assertEqual(node_result[0].node['name'].value, 'second')

    def test_xquery_list_predicate(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[@name_attr='test_two' "
            "or serie='B'][last()]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0].node['name'].value, 'third_doublon')

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[@name_attr='test_two' "
            "or serie='B'][position() < 5]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 4)
        self.assertEqual(node_result[0].node['name'].value, 'second')

        query = DrbXQuery(
            "/Level-2A_Tile_ID/Test_FLF[@name_attr='test_two' "
            "or serie='B'][position() < 5][2]")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0].node['name'].value, 'first_doublon')

    def test_xquery_func_range_fix(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery("1 to 5")
        node_result = query.execute(self.node)

        self.assertListEqual(node_result, [1, 2, 3, 4, 5])

    def test_xquery_namespace(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery("/nc3:Level-2A_Tile_ID")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(len(node_result[0].node['Test_FLF', :]), 6)

    def test_xquery_namespace_bis(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery("/nc3:Level-2A_Tile_ID/(nc3:Test_num[1], "
                          "nc3:Test_FLF[1])")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 2)

        self.assertEqual(node_result[1].node['name'].value, 'first')

    def test_xquery_namespace_not_exist(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery("/nc3:Level-2A_Tile_ID/(nc3:Test_num[1], "
                          "nc4:Test_FLF[1])")
        node_result = query.execute(self.node)

        self.assertEqual(len(node_result), 1)

        self.assertEqual(node_result[0].node['num_to_test'].value, '3.4')

    def test_xquery_external_var(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery("declare variable $x external; $x+1")

        list_var = {'x': 2}

        node_result = query.execute(self.node, list_var)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0], 3)

    def test_xquery_external_var_error(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery("declare variable $x external; $x+1")

        list_var = {'y': 2}

        with self.assertRaises(Exception) as error:
            node_result = query.execute(self.node, list_var)
        self.assertIn("XPDY0002", str(error.exception))

    def test_xquery_external_var_default_not_defined(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery("declare variable $x external; "
                          "declare variable $y external := 5; $x+$y")

        list_var = {'x': 9}

        node_result = query.execute(self.node, list_var)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0], 14)

    def test_xquery_external_var_default_defined(self):
        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        query = DrbXQuery("declare variable $x external; "
                          "declare variable $y external := 5; $x+$y")

        list_var = {'x': 9, 'y': 12}

        node_result = query.execute(self.node, list_var)

        self.assertEqual(len(node_result), 1)
        self.assertEqual(node_result[0], 21)

    def test_xquery_progess(self):

        self.node_file = DrbFileFactory().create(self.xml_file)
        self.node = XmlNodeFactory().create(self.node_file)

        # query = DrbXQuery('string(<a attr="content"><!-- NOTINC -->1<b>2<c><'
        #                   '!-- NOTINC -->34</c><!-- NOTINC -->56</b>7</a>) ')
        query = DrbXQuery('empty(abs(()))')

        list_var = {'x': 9, 'y': 12}

        node_result = query.execute(self.node, list_var)

        print(len(node_result))

        for res in node_result:
            print(DrbQueryFuncUtil.get_string(res))
