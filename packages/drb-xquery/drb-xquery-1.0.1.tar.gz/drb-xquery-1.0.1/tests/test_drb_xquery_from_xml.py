import os
import unittest
from pathlib import Path

from drb_impl_file import DrbFileFactory
from drb_impl_xml import XmlNodeFactory

from tests.XQueryTest import XQueryTest


class TestDrbXQueryFunc(unittest.TestCase):
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))

    xml_path = current_path / "files"

    def test_xquery_gael(self):
        xml_file = str(self.xml_path / "test_gael.xml")
        self.from_xml_node(xml_file)

    def test_xquery_operator(self):
        xml_file = str(self.xml_path / "xquery-gael-operators.xml")
        self.from_xml_node(xml_file)

    def test_xquery_doc(self):
        xml_file = str(self.xml_path / "xquery-gael-doc.xml")
        self.from_xml_node(xml_file)

    def test_xquery_functions(self):
        xml_file = str(self.xml_path / "xquery-gael-functions.xml")
        self.from_xml_node(xml_file)

    def test_xquery_queries(self):
        xml_file = str(self.xml_path / "xquery-gael-queries.xml")
        self.from_xml_node(xml_file)

    def test_xquery_module(self):
        xml_file = str(self.xml_path / "xquery-gael-module.xml")
        self.from_xml_node(xml_file)

    # def test_xquery_in_progress(self):
    #     xml_file = str(self.xml_path / "test.xml")
    #     self.from_xml_node(xml_file)

    def from_xml_node(self, xml_path):
        node_file = DrbFileFactory().create(xml_path)
        node = XmlNodeFactory().create(node_file)

        document = node[0]

        for child in document.children:
            current_test_node = child
            test = XQueryTest(current_test_node)
            with self.subTest(test.name):
                self.assertTrue(test.run_test(self), 'error in test '
                                + test.name)
        node.close()
        node_file.close()
