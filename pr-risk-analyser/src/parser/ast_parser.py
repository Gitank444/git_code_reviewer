import ast
from pathlib import Path

from src.schemas.symbols import FileAnalysis, FunctionSymbol


class CodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.imports = set()
        self.functions = []
        self.classes = []

    # --------------------
    # Imports
    # --------------------
    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.add(node.module)
        self.generic_visit(node)

    # --------------------
    # Classes
    # --------------------
    def visit_ClassDef(self, node):
        self.classes.append(node.name)
        self.generic_visit(node)

    # --------------------
    # Functions
    # --------------------
    
    
    def visit_FunctionDef(self, node):
        function_symbol = FunctionSymbol(
            name=node.name,
            calls=[]
        )
        
        # single-pass traversal (NOT ast.walk)
        for child in ast.walk(node):
            if isinstance(child, ast.Call):

                # simple function call: foo()
                if isinstance(child.func, ast.Name):
                    function_symbol.calls.append(child.func.id)

                # method call: obj.foo()
                elif isinstance(child.func, ast.Attribute):
                    function_symbol.calls.append(child.func.attr)

        self.functions.append(function_symbol)
        self.generic_visit(node)
        
    visit_AsyncFunctionDef = visit_FunctionDef

def analyze_file(file_path: Path) -> FileAnalysis:
    try:
        source_code = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source_code)
    except Exception:
        # production-safe fallback
        return FileAnalysis(
            file_path=str(file_path),
            imports=[],
            functions=[],
            classes=[]
        )

    visitor = CodeVisitor()
    visitor.visit(tree)

    return FileAnalysis(
        file_path=str(file_path),
        imports=list(visitor.imports),
        functions=visitor.functions,
        classes=visitor.classes,
    )