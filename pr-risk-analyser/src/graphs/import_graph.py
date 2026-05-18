import networkx as nx

from src.schemas.symbols import FileAnalysis


class ImportGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_file_analysis(self, analysis: FileAnalysis):
        current_file = analysis.file_path.split("\\")[-1].replace(".py", "")

        self.graph.add_node(current_file)

        for imported_module in analysis.imports:
            imported_module = imported_module.split(".")[-1]

            self.graph.add_node(imported_module)

            self.graph.add_edge(current_file, imported_module)

    def show_dependencies(self):
        print("\n===== DEPENDENCY GRAPH =====\n")

        for source, target in self.graph.edges():
            print(f"{source} ---> {target}")

    def get_all_dependents(self, module_name: str):
        visited = set()
        affected = []

        def dfs(target_module):
            for source, target in self.graph.edges():
                if target == target_module and source not in visited: 
                    visited.add(source)
                    affected.append(source)

                    dfs(source)

        dfs(module_name)
        return affected