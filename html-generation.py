import parser

import sys

import tornado
import tornado.template
import pygments
import pygments.lexers
import pygments.formatters

if __name__ == "__main__":
    filename = sys.argv[1]
    p = parser.Parser(open(filename))
    functions = p.parse_functions()

    loader = tornado.template.Loader('./', autoescape=None)
    template = loader.load('base.html')

    lexer = pygments.lexers.PythonLexer()
    formatter = pygments.formatters.HtmlFormatter(cssclass='highlight', style='monokai', linenos='inline', nobackground=False) # TODO get start lineno right

    cssfilename = './style.css'
    cssfile = open(cssfilename, 'w')
    cssfile.write(formatter.get_style_defs('.highlight'))
    cssfile.close()

    def highlight(code):
        return pygments.highlight(code.body, lexer, formatter)

    styled_functions = map(highlight, functions)

    print template.generate(functions=functions, styled_functions=styled_functions, filename=filename, cssfilename=cssfilename)
