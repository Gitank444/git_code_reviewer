class PRDiffAnalyzer:

    def analyze_changed_files(
        self,
        changed_files: list[str]
    ):

        changed_modules = []

        for file_path in changed_files:

            module_name = (
                file_path
                .split("\\")[-1]
                .replace(".py", "")
            )

            changed_modules.append(
                module_name
            )

        return changed_modules