import networkx as nx

from src.schemas.symbols import (
    CircularDependency
)


class CycleDetector:

    def detect_cycles(self, graph):

        cycles = nx.simple_cycles(graph)

        results = []

        for cycle in cycles:

            results.append(
                CircularDependency(
                    cycle=cycle
                )
            )

        return results