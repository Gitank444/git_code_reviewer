class EdgeAnalyzer:

    def extract_new_edges(
        self,
        added_imports: list[str],
        source_module: str
    ):

        edges = []

        for import_stmt in added_imports:

            # from pricing import x
            if import_stmt.startswith("from"):

                target = (
                    import_stmt
                    .split()[1]
                    .split(".")[-1]
                )

                edges.append(
                    (
                        source_module,
                        target
                    )
                )

            # import pricing
            elif import_stmt.startswith("import"):

                target = (
                    import_stmt
                    .split()[1]
                    .split(".")[-1]
                )

                edges.append(
                    (
                        source_module,
                        target
                    )
                )

        return edges