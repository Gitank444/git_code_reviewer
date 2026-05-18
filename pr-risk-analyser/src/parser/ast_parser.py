import ast
from pathlib import Path

from src.schemas.symbols import FileAnalysis, FunctionSymbol




class CodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.imports = []
        self.functions = []
        self.classes = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.append(node.module)

    def visit_ClassDef(self, node):
        self.classes.append(node.name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        function_symbol = FunctionSymbol(name=node.name)

        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    function_symbol.calls.append(child.func.id)

        self.functions.append(function_symbol)

        self.generic_visit(node)


def analyze_file(file_path: Path) -> FileAnalysis:
    source_code = file_path.read_text()

    tree = ast.parse(source_code)

    visitor = CodeVisitor()
    visitor.visit(tree)

    return FileAnalysis(
        file_path=str(file_path),
        imports=visitor.imports,
        functions=visitor.functions,
        classes=visitor.classes,
    )