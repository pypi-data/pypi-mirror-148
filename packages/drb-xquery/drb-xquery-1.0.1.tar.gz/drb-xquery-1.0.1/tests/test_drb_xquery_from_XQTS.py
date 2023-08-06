import os
import unittest
from pathlib import Path

from drb_impl_file import DrbFileFactory
from drb_impl_xml import XmlNodeFactory

from tests.XQueryTestXQTS import XQueryTestXQTS


class TestDrbXQueryXQTS(unittest.TestCase):
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))

    xml_path = current_path / "files"

    def test_xquery_xqts_func_abs(self):
        xml_file = str(self.xml_path / "XQTS_1_0_3/cat/ABSFunc.xml")
        #
        self.from_xml_xqts(xml_file)

    def test_xquery_xqts_analyse_string(self):

        xml_file = str(self.xml_path / "XQTS_1_0_3/cat/AnalyzeString.xml")
        self.from_xml_xqts(xml_file)

    def test_xquery_xqts_direct_con_elt(self):
        xml_file = str(self.xml_path / "XQTS_1_0_3/cat/DirectConElem.xml")
        self.from_xml_xqts(xml_file)

    def test_xquery_xqts_FLWOR(self):
        xml_file = str(self.xml_path / "XQTS_1_0_3/cat/FLWORExprSI.xml")
        self.from_xml_xqts(xml_file)

    def test_xquery_xqts_fn_substring(self):
        xml_file = str(
            self.xml_path / "XQTS_1_0_3/cat/functx-fn-substring.xml")
        self.from_xml_xqts(xml_file)

    def test_xquery_xqts_fn_substring_after(self):
        xml_file = str(
            self.xml_path / "XQTS_1_0_3/cat/functx-fn-substring-after.xml")
        self.from_xml_xqts(xml_file)

    def test_xquery_xqts_fn_substring_before(self):
        xml_file = str(
            self.xml_path / "XQTS_1_0_3/cat/functx-fn-substring-before.xml")
        self.from_xml_xqts(xml_file)

    def test_xquery_xqts_fn_sum(self):
        xml_file = str(
            self.xml_path / "XQTS_1_0_3/cat/functx-fn-sum.xml")
        self.from_xml_xqts(xml_file)

    def test_xquery_xqts_filter_expr(self):
        xml_file = str(self.xml_path / "XQTS_1_0_3/cat/FilterExpr.xml")
        self.from_xml_xqts(xml_file)

    def test_xquery_xqts_for_exp_wtih(self):
        xml_file = str(self.xml_path / "XQTS_1_0_3/cat/ForExprWith.xml")
        self.from_xml_xqts(xml_file)

    def test_xquery_xqts_module_import(self):
        xml_file = str(self.xml_path / "XQTS_1_0_3/cat/ModuleImport.xml")
        self.from_xml_xqts(xml_file)

    def test_xquery_xqts_module_predicates(self):
        xml_file = str(self.xml_path / "XQTS_1_0_3/cat/Predicates.xml")
        self.from_xml_xqts(xml_file)

    # def test_xquery_xqts_fn_in_progess(self):
    #     xml_file = str(self.xml_path /
    #                    "XQTS_1_0_3/cat/in_progress.xml")
    #     self.from_xml_xqts(xml_file)

    def from_xml_xqts(self, xml_path):
        node_file = DrbFileFactory().create(xml_path)
        node = XmlNodeFactory().create(node_file)

        document = node['test-group']

        for child in document['test-case', :]:
            current_test_node = child
            test = XQueryTestXQTS(current_test_node)
            with self.subTest(test.name):
                self.assertTrue(test.run_test(self), 'error in test '
                                + test.name)
