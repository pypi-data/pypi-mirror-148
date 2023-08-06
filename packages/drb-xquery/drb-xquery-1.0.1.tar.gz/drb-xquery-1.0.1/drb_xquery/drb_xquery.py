
from antlr4 import InputStream, CommonTokenStream

from drb import DrbNode

from drb_xquery.XQueryLexer import XQueryLexer
from drb_xquery.XQueryParser import XQueryParser
from drb_xquery.drb_xquery_context import DynamicContext
from drb_xquery.drb_xquery_visitor import DrbQueryVisitor, \
    DrbXqueryParserErrorListener


class DrbXQuery:

    def __init__(self, xquery_string):
        self.static_context = None

        # init Lexer with query
        lexer = XQueryLexer(InputStream(xquery_string))

        self.stream = CommonTokenStream(lexer)
        self.parser = XQueryParser(self.stream)

        self.parser.addErrorListener(DrbXqueryParserErrorListener())
        # parse query and reject it if error
        self.tree = self.parser.module()

    def execute(self, node: DrbNode, external_var: dict = None):
        # Execute the query on the node
        visitor = DrbQueryVisitor(DynamicContext(node), tokens=self.stream)
        visitor.external_var_map = external_var
        self.static_context = visitor.static_context

        output = visitor.visitModule(self.tree)
        if not isinstance(output, list):
            output = [output]
        return output
