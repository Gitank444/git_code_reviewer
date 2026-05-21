import networkx as nx

from src.schemas.symbols import FileAnalysis
import matplotlib.pyplot as plt

class CallGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_file_analysis(self, analysis: FileAnalysis):
        for function in analysis.functions:

            self.graph.add_node(function.name)

            for called_function in function.calls:
                self.graph.add_node(called_function)

                self.graph.add_edge(function.name, called_function)

    def show_graph(self):
        print("\n===== FUNCTION CALL GRAPH =====\n")

        for source, target in self.graph.edges():
            print(f"{source} ---> {target}")

    def get_downstream_calls(self, function_name: str):
        visited = set()
        downstream = []

        def dfs(node):
            for neighbor in self.graph.successors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    downstream.append(neighbor)
                    dfs(neighbor)

        dfs(function_name)

        return downstream 
    
    def draw_graph(self):
        
        plt.figure(figsize=(10, 7))

        pos = nx.spring_layout(self.graph)

        nx.draw(
        self.graph,
        pos,
        with_labels=True,
        node_size=3000,
        node_color="lightblue",
        font_size=10,
        font_weight="bold",
        arrows=True
        )

        plt.title("Function Call Graph")

        plt.show()
     
    