from src.orchestrator.pipeline import (
    PRAnalysisPipeline
)
from src.diff.git_diff_parser import (
    GitDiffParser
)
from src.diff.edge_analyzer import (
    EdgeAnalyzer
)
from src.rules.architecture_rules import (
    ArchitectureRuleEngine
)

rule_engine = ArchitectureRuleEngine()

diff_text = """
+from pricing import calculate_total

+def risky_checkout():
+     pass

-def old_checkout():
-     pass
"""

parser = GitDiffParser()
edge_analyzer = EdgeAnalyzer()

diff_result = parser.parse_diff(
    diff_text
)

print("\n===== GIT DIFF ANALYSIS =====")

print("\nAdded Imports:")
for item in diff_result["added_imports"]:
    print(f" - {item}")

print("\nRemoved Imports:")
for item in diff_result["removed_imports"]:
    print(f" - {item}")

print("\nChanged Functions:")
for item in diff_result["changed_functions"]:
    print(f" - {item}")
pipeline = PRAnalysisPipeline()

result = pipeline.run(
    repo_path="src/sample_repo",
    changed_files=[
        "src/sample_repo/pricing.py"
    ]
)
    

print("\n===== BLAST RADIUS =====")

for module in result.affected_modules:
    print(f" - {module}")

print("\n===== FUNCTION IMPACT =====")

for function in result.downstream_functions:
    print(f" - {function}")

print("\n===== RISK ANALYSIS =====")

print(
    f"Risk Score: "
    f"{result.risk_result.score}/100"
)

print(
    f"Severity: "
    f"{result.risk_result.severity}"
)

print("\nReasons:")

for reason in result.risk_result.reasons:
    print(f" - {reason}")

print("\n===== ARCHITECTURE VIOLATIONS =====")

if not result.violations:
    print("No violations detected")

else:
    for violation in result.violations:
        print(f" - {violation.message}")

print("\n===== CIRCULAR DEPENDENCY ANALYSIS =====")

if not result.cycles:
    print("No circular dependencies detected")

else:
    for cycle in result.cycles:

        cycle_path = " -> ".join(cycle.cycle)

        print(f" - {cycle_path}")

        
new_edges = edge_analyzer.extract_new_edges(
    diff_result["added_imports"],
    source_module="analytics"
)

print("\n===== NEW EDGES =====")

for edge in new_edges:
    print(f" - {edge[0]} ---> {edge[1]}")
    
new_violations = (
    rule_engine.validate_new_edges(
        new_edges
    )
)

print("\n===== NEW VIOLATIONS =====")

for violation in new_violations:
    print(f" - {violation.message}")
    
