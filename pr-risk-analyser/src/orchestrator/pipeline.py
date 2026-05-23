from pathlib import Path
from src.parser.ast_parser import analyze_file
from src.graphs.import_graph import ImportGraph
from src.graphs.call_graph import CallGraph
from src.scorer.risk_scorer import RiskScorer
from src.rules.architecture_rules import ArchitectureRuleEngine
from src.schemas.symbols import AnalysisResult
from src.graphs.cycle_detector import CycleDetector
from src.diff.pr_diff_analyzer import PRDiffAnalyzer
from src.diff.github_pr_fetcher import GitHubPRFetcher
from src.diff.git_diff_parser import GitDiffParser


class PRAnalysisPipeline:

    def __init__(self):
        self.import_graph = ImportGraph()
        self.call_graph = CallGraph()
        self.risk_scorer = RiskScorer()
        self.rule_engine = ArchitectureRuleEngine()
        self.cycle_detector = CycleDetector()
        self.diff_analyzer = PRDiffAnalyzer()

    def run_from_github_pr(self, owner, repo, pr_number, token, repo_path):
        fetcher = GitHubPRFetcher(token)
        files = fetcher.get_pr_files(owner, repo, pr_number)
        diff_text = fetcher.get_diff_text(files)

        parser = GitDiffParser()
        diff_result = parser.parse_diff(diff_text)

        changed_files = []
        for file in files:
            
            if isinstance(file, dict) and "filename" in file:
                changed_files.append(file["filename"])

        return self.run(repo_path, changed_files, diff_result)

    def run(
        self,
        repo_path: str,
        changed_files: list[str],
        diff_result: dict = None
    ) -> AnalysisResult:
        # print(f"DEBUG diff_result received: {diff_result}")

        if diff_result is None:
            diff_result = {"changed_functions": [], "added_imports": [], "removed_imports": []}

        repo = Path(repo_path)
        file_analyses = []
        python_files = repo.rglob("*.py")

        # STEP 1 — Parse files
        for file in python_files:
            analysis = analyze_file(file)
            file_analyses.append(analysis)

            # STEP 2 — Build graphs
            self.import_graph.add_file_analysis(analysis)
            self.call_graph.add_file_analysis(analysis)

        # STEP 3 — Extract changed modules
        changed_modules = self.diff_analyzer.analyze_changed_files(changed_files)

        # STEP 4 — Blast radius
        affected_modules = []
        for module in changed_modules:
            impacted = self.import_graph.get_all_dependents(module)
            affected_modules.extend(impacted)
        affected_modules = list(set(affected_modules))

        # STEP 5 — Function impact
        downstream_functions = []
        # print(f"DEBUG changed_functions: {changed_functions}")
        changed_functions = diff_result["changed_functions"]
        for function in changed_functions:
            results = self.call_graph.get_downstream_calls(function)
            downstream_functions.extend(results)
        # print(f"DEBUG total nodes in call graph: {len(self.call_graph.graph.nodes)}")
        # print(f"DEBUG first 10 nodes: {list(self.call_graph.graph.nodes)[:10]}")
        # print(f"DEBUG looking for: {changed_functions[0]}")
        # print(f"DEBUG found in graph: {changed_functions[0] in self.call_graph.graph}")
        # print(f"DEBUG found in graph: {changed_functions[0] in self.call_graph.graph}")


        # STEP 6 — Risk scoring
        risk_result = self.risk_scorer.calculate_risk(
            changed_module=changed_modules[0] if changed_modules else None,
            affected_modules=affected_modules,
            downstream_functions=downstream_functions
        )

        # STEP 7 — Architecture validation
        violations = self.rule_engine.validate(self.import_graph.graph)

        # STEP 8 — Cycle detection
        cycles = self.cycle_detector.detect_cycles(self.import_graph.graph)

        return AnalysisResult(
            file_analyses=file_analyses,
            affected_modules=affected_modules,
            downstream_functions=downstream_functions,
            risk_result=risk_result,
            violations=violations,
            cycles=cycles
        )