from src.orchestrator.pipeline import PRAnalysisPipeline
from src.diff.edge_analyzer import EdgeAnalyzer
from src.rules.architecture_rules import ArchitectureRuleEngine

# Setup
pipeline = PRAnalysisPipeline()
edge_analyzer = EdgeAnalyzer()
rule_engine = ArchitectureRuleEngine()

# Run against real GitHub PR
# result = pipeline.run_from_github_pr(
    
#     owner="",       # example: "torvalds"
#     repo="",        # example: "linux"
#     pr_number=42,     # example: 42
#     token="",       # your GitHub token
#     repo_path=""    # example: "C:/Users/Gitank/projects/linux"
# )
result = pipeline.run(
    repo_path="src/sample_repo",
    changed_files=["src/sample_repo/pricing.py"]
)

print("\n===== BLAST RADIUS =====")
for module in result.affected_modules:
    print(f" - {module}")

print("\n===== FUNCTION IMPACT =====")
for function in result.downstream_functions:
    print(f" - {function}")

print("\n===== RISK ANALYSIS =====")
print(f"Risk Score: {result.risk_result.score}/100")
print(f"Severity: {result.risk_result.severity}")
print("\nReasons:")
for reason in result.risk_result.reasons:
    print(f" - {reason}")

print("\n===== ARCHITECTURE VIOLATIONS =====")
if not result.violations:
    print("No violations detected")
else:
    for violation in result.violations:
        print(f" - {violation.message}")

print("\n===== CIRCULAR DEPENDENCIES =====")
if not result.cycles:
    print("No circular dependencies detected")
else:
    for cycle in result.cycles:
        print(f" - {' -> '.join(cycle.cycle)}")

