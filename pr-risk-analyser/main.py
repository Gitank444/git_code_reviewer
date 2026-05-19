from src.orchestrator.pipeline import (
    PRAnalysisPipeline
)


pipeline = PRAnalysisPipeline()

result = pipeline.run(
    repo_path="src/sample_repo",
    changed_module="pricing",
    changed_function="calculate_total"
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