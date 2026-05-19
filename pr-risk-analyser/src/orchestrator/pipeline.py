from pathlib import Path

from src.parser.ast_parser import analyze_file
from src.graphs.import_graph import ImportGraph
from src.graphs.call_graph import CallGraph
from src.scorer.risk_scorer import RiskScorer
from src.rules.architecture_rules import (
    ArchitectureRuleEngine
)
from src.schemas.symbols import AnalysisResult
from src.graphs.cycle_detector import (
    CycleDetector
)

class PRAnalysisPipeline:

    def __init__(self):
        self.import_graph = ImportGraph()
        self.call_graph = CallGraph()

        self.risk_scorer = RiskScorer()

        self.rule_engine = ArchitectureRuleEngine()
        
        self.cycle_detector = CycleDetector()

    def run(
        self,
        repo_path: str,
        changed_module: str,
        changed_function: str
    ) -> AnalysisResult:

        repo = Path(repo_path)

        file_analyses = []

        python_files = repo.glob("*.py")

        # STEP 1 — Parse files
        for file in python_files:

            analysis = analyze_file(file)

            file_analyses.append(analysis)

            # STEP 2 — Build graphs
            self.import_graph.add_file_analysis(
                analysis
            )

            self.call_graph.add_file_analysis(
                analysis
            )

        # STEP 3 — Blast radius
        affected_modules = (
            self.import_graph.get_all_dependents(
                changed_module
            )
        )

        # STEP 4 — Function impact
        downstream_functions = (
            self.call_graph.get_downstream_calls(
                changed_function
            )
        )

        # STEP 5 — Risk scoring
        risk_result = (
            self.risk_scorer.calculate_risk(
                changed_module=changed_module,
                affected_modules=affected_modules,
                downstream_functions=downstream_functions
            )
        )

        # STEP 6 — Architecture validation
        violations = (
            self.rule_engine.validate(
                self.import_graph.graph
            )
        )
         
        # STEP 7 — Cycle detection
        cycles = self.cycle_detector.detect_cycles(
          self.import_graph.graph
        ) 
        return AnalysisResult(
            file_analyses=file_analyses,
            affected_modules=affected_modules,
            downstream_functions=downstream_functions,
            risk_result=risk_result,
            violations=violations,
            cycles=cycles
        )