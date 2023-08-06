import html
import unittest

from drb import DrbNode
from drb_impl_file import DrbFileFactory

from drb_impl_xml import XmlNodeFactory
from drb_xquery import DrbXQuery
from pathlib import Path
from tests.XQueryTest import XQueryTest

X_QUERY_PATH_FILES = 'tests/files/XQTS_1_0_3'


class XQueryTestXQTS:

    def import_var(self, node_input: DrbNode):
        variable_name = node_input.get_attribute('variable')

        if node_input.value != 'emptydoc':
            xml_path = X_QUERY_PATH_FILES + '/TestSources/' + \
                       node_input.value + ".xml"
            node_file = DrbFileFactory().create(xml_path)
            node_var = XmlNodeFactory().create(node_file)
            self.vars[variable_name] = node_var
        else:
            self.vars[variable_name] = None

    def import_var_uri(self, node_input: DrbNode):
        if node_input.value != 'emptydoc':
            xml_path = X_QUERY_PATH_FILES + '/TestSources/' + \
                       node_input.value + ".xml"
            variable_name = node_input.get_attribute('variable')
            self.vars[variable_name] = xml_path

    def import_var_xq(self, node_input: DrbNode, path_file):

        variable_name = node_input.get_attribute('variable')
        name_xq = node_input.get_attribute('name')

        try:
            txt_query = Path(X_QUERY_PATH_FILES + '/Queries/XQuery/' +
                             path_file + '/' + name_xq + '.xq').read_text()
            query = DrbXQuery(txt_query)
            result = query.execute(None)

            if isinstance(result, list):
                result = result[0]
            self.vars[variable_name] = result
        except Exception as error_query:
            raise Exception(error_query,
                            'Error not expected raise  in ' +
                            str(self.name) +
                            " When get var " + variable_name)

    def __init__(self, node: DrbNode):
        self.node = node
        self.name = self.node.get_attribute("name")
        self.expected_result = []
        self.vars = {}
        self.node_begin = None
        self.error = None

    def run_test(self, testClass: unittest.TestCase):

        path_file = self.node.get_attribute("FilePath")
        txt_query = Path(X_QUERY_PATH_FILES + '/Queries/XQuery/' +
                         path_file + '/' + self.name + '.xq').read_text()
        self.query = txt_query

        if self.node.has_child('output-file'):
            nodes_res = self.node['output-file', :]
            for node_res in nodes_res:
                file_res = node_res.value
                self.expected_result.append(Path(X_QUERY_PATH_FILES +
                                                 '/ExpectedTestResults/' +
                                                 path_file + '/' +
                                                 file_res).read_text())

        if self.node.has_child('input-query'):
            nodes_var = self.node['input-query', :]
            for node_var in nodes_var:
                self.import_var_xq(node_var, path_file)

        if self.node.has_child('input-file'):
            node_input = self.node['input-file']
            self.import_var(node_input)

        if self.node.has_child('input-URI'):
            node_input = self.node['input-URI']
            self.import_var_uri(node_input)

        if self.node.has_child('expected-error'):
            self.error = self.node['expected-error'].value

        try:
            query_string = self.query
            # query_string = html.unescape(query_string)

            query = DrbXQuery(query_string)
            result = query.execute(self.node_begin, external_var=self.vars)
        except Exception as error_query:
            if self.error:
                return True
            else:
                raise Exception(error_query,
                                'Error not expected raise  in ' +
                                str(self.name))
        if result is None:
            if len(self.expected_result) == 0:
                return True
            else:
                return False

        if not isinstance(result, list):
            result = [result]

        result_string = None
        for item in result:
            result_string = XQueryTest.add_item_to_result(
                result_string, item,
                separator=' ',
                context=query.static_context,
                float_format_g=False)

        if result_string is None:
            result_string = ''

        if self.error and len(self.expected_result) == 0:
            print("Test OK but error is waited")
            testClass.assertTrue(False, self.name + ' Error ' + self.error +
                                 " is expected, but not error raised " +
                                 " result is :\n" +
                                 result_string)

        if len(self.expected_result) == 0:
            if result_string == '':
                return True

        for expected_result_possible in self.expected_result:
            if XQueryTest.compare_result_and_expected(expected_result_possible,
                                                      result_string):
                return True
        testClass.assertTrue(False, self.name +
                             ' result are not as expected\n' +
                             "'" + result_string + "'" +
                             '\n != \n' +
                             "'" + expected_result_possible + "'")
