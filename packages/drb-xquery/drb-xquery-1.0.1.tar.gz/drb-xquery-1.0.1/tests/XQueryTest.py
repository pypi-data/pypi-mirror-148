import html
import re
import unittest
from xml.etree import ElementTree

from drb import DrbNode

from drb_impl_xml import XmlNode
from drb_xquery import DrbXQuery
from drb_xquery.drb_xquery_context import DynamicContext, StaticContext
from drb_xquery.drb_xquery_item import DrbXqueryItem
from drb_xquery.drb_xquery_utils import DrbQueryFuncUtil


class XQueryTest:

    def __init__(self, node: DrbNode):
        self.node = node

        self.name = node.get_attribute("name")
        self.query = self.node['query']
        try:
            self.expected_result = self.node['result']
        except Exception as Error:
            self.expected_result = None

        self.dynamicError = False
        try:
            attr_value = self.query.get_attribute("dynamicError")
            if attr_value is not None and str(attr_value).lower() == "true":
                self.dynamicError = True
        except Exception as Error:
            pass
        self.staticError = False
        try:
            attr_value = self.query.get_attribute("staticError")
            if attr_value is not None and str(attr_value).lower() == "true":
                self.staticError = True
        except Exception as Error:
            pass

    @staticmethod
    def manage_prefix_namespace(namespace_uri,
                                context: StaticContext,
                                dynamic_context: DynamicContext,
                                namespace_declared):
        if namespace_uri is None:
            return '', ''
        prefix_ret = ''

        if dynamic_context is not None:
            prefix = dynamic_context.get_namespace_prefix_name(namespace_uri)
        if prefix is None or len(prefix) == 0:
            prefix = context.get_namespace_prefix_name(namespace_uri)
        if prefix is None or len(prefix) == 0:
            namespace_def = ' xmlns' + '="' \
                            + namespace_uri + '"'
        else:
            namespace_def = ' xmlns:' + prefix + '="' \
                            + namespace_uri + '"'
            prefix_ret = prefix + ':'

        if namespace_uri not in namespace_declared:
            namespace_declared.append(namespace_uri)
            return prefix_ret, namespace_def
        return prefix_ret, ''

    @staticmethod
    def drb_item_to_xml(item,
                        context: StaticContext,
                        namespace_declared: list,
                        dynamic_context: DynamicContext):
        if not isinstance(item, DrbXqueryItem):
            return item.name

        namespace_definition = ''
        result = '<'

        if dynamic_context is not None:
            for (ns_full, ns_prefix) in \
                    dynamic_context.name_space_map.namespace_prefix_map.\
                    items():
                if ns_full not in namespace_declared:
                    namespace_definition = namespace_definition +\
                                           ' xmlns:' + ns_prefix + '="' + \
                                           ns_full + '"'
                    namespace_declared.append(ns_full)

        prefix, namespace_def = XQueryTest.manage_prefix_namespace(
            item.namespace_uri,
            context,
            dynamic_context,
            namespace_declared)

        namespace_definition = namespace_definition + namespace_def

        result = result + prefix + item.name
        for key in item.attributes.keys():
            if isinstance(key, tuple):
                if len(key) == 2 and key[1] is not None:
                    prefix_attr, namespace_def = \
                        XQueryTest.manage_prefix_namespace(
                            key[1],
                            context,
                            dynamic_context,
                            namespace_declared)
                    name_key = prefix_attr + key[0]
                    namespace_definition = namespace_definition + namespace_def
                else:
                    name_key = key[0]
            else:
                name_key = key
            value_attr = item.attributes[key]
            if not isinstance(value_attr, str) or \
                    not value_attr.startswith('"'):
                value_attr = '"' + str(value_attr) + '"'

            result = result + ' ' + name_key + '=' + value_attr

        result = result + namespace_definition
        if item.value is None and len(item.children) == 0:
            return result + '/>'
        result = result + '>'

        for child in item.children:
            result = XQueryTest.add_item_to_result(
                result, child, '',
                context=context,
                namespace_declared=namespace_declared,
                dynamic_context=dynamic_context)
        if item.value is not None:
            result = result + str(item.value)
        result = result + '</'
        result = result + prefix + item.name + '>'

        return result

    @staticmethod
    def add_item_to_result(result_string: str, item, separator=',',
                           context: StaticContext = None,
                           dynamic_context: DynamicContext = None,
                           namespace_declared: list = None,
                           float_format_g=True):
        if namespace_declared is None:
            namespace_declared = []

        if result_string is None:
            result_string = ''
        else:
            result_string = result_string + separator

        if isinstance(item, DynamicContext):
            if isinstance(item.node, XmlNode):
                xml_bytes = ElementTree.tostring(item.node._elem)
                result_string = result_string + xml_bytes.decode()
                if result_string.find('ns0=') >= 0:
                    result_string = result_string.replace('xmlns:ns0=',
                                                          'xmlns=')
                    result_string = result_string.replace('ns0:', '')
                    result_string = re.sub('>\\s+<', '><', result_string)
            elif isinstance(item.node, DrbXqueryItem):
                result_string = result_string + \
                                XQueryTest.drb_item_to_xml(
                                    item.node,
                                    context=context,
                                    namespace_declared=namespace_declared,
                                    dynamic_context=item)
            else:
                result_string = result_string + item.name
        elif isinstance(item, DrbXqueryItem):
            result_string = result_string + XQueryTest.drb_item_to_xml(
                item, context=context,
                namespace_declared=namespace_declared,
                dynamic_context=dynamic_context)
        elif isinstance(item, DrbNode):
            result_string = result_string + item.name
        elif isinstance(item, float):
            if float_format_g is True:
                result_float = '{:g}'.format(item)
                result_float = result_float.replace('+', '')
                if 'inf' not in result_float and \
                        'e' not in result_float and \
                        '.' not in result_float:
                    result_float = result_float + ".0"
            else:
                result_float = str(item).replace('e+', 'e')
                if result_float.endswith(".0"):
                    result_float = result_float[:-2]
            result_string = result_string + result_float
        else:
            result_string = result_string + DrbQueryFuncUtil.get_string(item)
        return result_string

    @staticmethod
    def remove_blank(str_result):
        # Remove blank for simplify the compare operation
        str_result = str(str_result).lower()
        str_result = str_result.replace('\n', '')
        str_result = str_result.strip()
        str_result = re.sub('\\s+', ' ', str_result)
        str_result = str_result.replace(', ', ',')
        str_result = str_result.replace('> <', '><')
        str_result = str_result.replace(' />', '/>')

        return str_result

    @staticmethod
    def compare_result_and_expected(expected_str,
                                    result_string):
        expected_str = XQueryTest.remove_blank(expected_str)
        result_string = XQueryTest.remove_blank(result_string)

        if expected_str == result_string:
            return True

    def run_test(self, testClass: unittest.TestCase):
        try:
            query_string = self.query.value
            query_string = html.unescape(query_string)

            query = DrbXQuery(query_string)
            result = query.execute(None)
        except Exception as error_query:
            if self.dynamicError or self.staticError:
                return True
            else:
                raise Exception(error_query,
                                'Error raise  in ' + str(self.name))
        if result is None:
            if self.expected_result is None:
                return True
            else:
                return False

        if self.dynamicError or self.staticError:
            print("Test OK but error is waited")
            return False

        if not isinstance(result, list):
            result = [result]

        result_string = None
        for item in result:
            result_string = self.add_item_to_result(
                result_string, item,
                context=query.static_context)

        if result_string is None:
            result_string = ''

        if self.expected_result is None or self.expected_result.value is None:
            expected_result = ''
        else:
            expected_result = self.expected_result.value

        if XQueryTest.compare_result_and_expected(expected_result,
                                                  result_string):
            return True
        testClass.assertTrue(False, self.name
                             + ' result are not as expected\n'
                             + result_string + '\n != \n' +
                             expected_result)
