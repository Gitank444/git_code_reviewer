class GitDiffParser:

    def parse_diff(
        self,
        diff_text: str
    ):

        added_imports = []

        removed_imports = []

        changed_functions = []

        lines = diff_text.splitlines()

        for line in lines:
            
            # print(f"DEBUG:{repr(line)}")

            line = line.strip()

            # Added imports
            if (
                line.startswith("+import ")
                or line.startswith("+from ")
            ):
                import_statement = line[1:]
                
                added_imports.append(
                    import_statement
                    )

                

            # Removed imports
            elif (
                line.startswith("-import ")
                or line.startswith("-from ")
            ):

                removed_imports.append(
                    line[1:]
                )

            # Changed functions
            elif (
                line.startswith("+def ")
                or line.startswith("-def ")
            ):

                function_name = (
                    line.split("def ")[1]
                    .split("(")[0]
                )

                changed_functions.append(
                    function_name
                )

        return {
            "added_imports": added_imports,
            "removed_imports": removed_imports,
            "changed_functions": changed_functions
        }