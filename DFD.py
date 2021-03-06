import ast
import codegen
import astunparse
import inspect
import re
import os

class CodeVisitor(ast.NodeVisitor):
    def __init__(self, table):
        self.table = table

    def visit_FunctionDef(self, node):
        self._handleFunction(node)

    def _handleAssign(self, node):
        return
    def _decide(self, node, affected_set):
        code = astunparse.unparse(ast.Module([node]))
        code = ' ' + code[code.find("=")+1:].strip()
        for item in affected_set:
            pattern = r'\W'+item
            if re.search(pattern, code):
                return True
        return False

    def _handleFunction(self, node): 
        affected_set = set([arg.arg for arg in node.args.args])
        for n in ast.iter_child_nodes(node):
            if isinstance(n, ast.Assign):
                if self._decide(n, affected_set):
                    for target in n.targets:
                        if isinstance(target, ast.Attribute):
                            target = target.value
                        if isinstance(target, ast.Name):
                            affected_set.add(target.id)
        self.table[node.name] = affected_set

def genDFD(path):
    dfd = {}
    for fpathe,dirs,fs in os.walk(path):
        for filename in fs:
            if filename[-3:] != ".py":
                continue
            if filename == "flaskext_compat.py":
                continue
            if filename == "flask-07-upgrade.py":
                continue
            if filename == "conf.py":
                continue
            if filename == "flaskext_test.py":
                continue
            if filename == "flaskext_test.py":
                continue
            if filename == "setup.py":
                continue
            if filename == "app.py":
                continue
            if filename == "config.py":
                continue
            if filename == "ctx.py":
                continue
            if filename == "debughelpers.py":
                continue
            if filename == "exthook.py":
                continue
            if filename == "helpers.py":
                continue
            if filename == "wrappers.py":
                continue
            if filename == "basic.py":
                continue
            if filename == "blueprints.py":
                continue
            if filename == "testing.py":
                continue
            if filename == "__init__.py":
                continue
            if filename == "flask_tests.py":
                continue
            f = open(fpathe + '/' + filename, 'r', encoding = 'utf-8')
            code_str = f.read()
            f.close()
            print(f)
            ast_str = ast.parse(code_str)
            visitor = CodeVisitor({})
            visitor.visit(ast_str)
            if len(fpathe) != len(path):
                key = fpathe[len(path)+1:] + '/' + filename
            else:
                key = filename
            dfd[key] = visitor.table
    return dfd
    #for filename, d in dfd.items():
        #print(filename, ":")
        #for funcname, table in d.items():
        #    print(funcname, [item for item in table['args']], [item for item in table['affected']])

if __name__ == "__main__":
    print(genDFD("C:\\Users\\13502\\flask"))