import ast
import sys

class Function(object):
    def __init__(self, source, name, class_name=None):
        self.source = source
        self.name = name
        self.class_name = class_name

        self.min_line = None
        self.max_line = None

    @property
    def header(self):
        if not self._header:
            if self.class_name:
                self._header = "Method %s.%s:\n" % (self.class_name, self.name)
            else:
                self._header = "Function %s:\n" % (self.name,)
        return self._header

    @property
    def body(self):
        if not self._body:
            self._body = ""
            indent = len(self.source[self.min_line]) - len(self.source[self.min_line].lstrip())
            for i in range(self.min_line, self.max_line + 1):
                self._body += self.source[i][indent:]
        return self._body

    def __str__(self):
        return self.header + self.body

    def add_line(self, lineno):
        if self.min_line is None or lineno < self.min_line:
            self.min_line = lineno
            self._header = None
            self._body = None

        if self.max_line is None or lineno > self.max_line:
            self.max_line = lineno
            self._header = None
            self._body = None

class FunctionVisitor(ast.NodeVisitor):
    def __init__(self, source):
        self.source = source
        self.current_class = None
        self.current_function = None
        self.functions = []

    def visit_ClassDef(self, node):
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node):
        reset = False
        if not self.current_function:
            reset = True
            self.current_function = Function(self.source, node.name, self.current_class)
            self.functions.append(self.current_function)

        self.current_function.add_line(node.lineno - 1)

        self.generic_visit(node)

        if reset:
            self.current_function = None

    def generic_visit(self, node):
        try:
            if self.current_function:
                self.current_function.add_line(node.lineno - 1)
        except AttributeError:
            pass

        super(FunctionVisitor, self).generic_visit(node)

class Parser(object):
    def __init__(self, f):
        self.f = f

    def parse_functions(self):
        source = self.f.readlines()
        text = "".join(source)

        top = ast.parse(text)
        
        v = FunctionVisitor(source)
        v.visit(top)

        return v.functions

if __name__ == "__main__":
    p = Parser(open(sys.argv[1]))
    functions = p.parse_functions()

    for fn in functions:
        print fn
