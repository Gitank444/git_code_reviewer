from src.schemas.symbols import RiskResult


class RiskScorer:

    CRITICAL_MODULES = [
        "pricing", "auth", "payment", "database"
    ]

    CORE_MODULES = [
        "routing", "applications", "main",
        "utils", "params", "models", "encoders",
        "datastructures", "types", "base",
        "dependencies", "security", "middleware"
    ]

    def calculate_risk(
        self,
        changed_module: str,
        affected_modules: list[str],
        downstream_functions: list[str]
    ) -> RiskResult:

        score = 0
        reasons = []

        # Critical module risk
        if changed_module in self.CRITICAL_MODULES:
            score += 40
            reasons.append(f"{changed_module} is a critical module")

        # Split affected modules into tiers
        core_affected = [m for m in affected_modules if m in self.CORE_MODULES]
        test_affected = [m for m in affected_modules if m.startswith("test_")]
        other_affected = [m for m in affected_modules
                          if m not in core_affected and m not in test_affected]

        # Score based on core modules only
        core_count = len(core_affected)
        blast_radius_score = (core_count / len(self.CORE_MODULES)) * 50
        score += blast_radius_score

        reasons.append(f"{core_count} core modules affected (critical)")
        reasons.append(f"{len(test_affected)} test files affected (low risk)")
        reasons.append(f"{len(other_affected)} other modules affected")

        # Function-chain depth risk
        function_depth = len(downstream_functions)
        score += function_depth * 5
        reasons.append(f"{function_depth} downstream function calls detected")

        # Cap score at 100
        score = min(score, 100)

        # Severity classification
        if score >= 70:
            severity = "HIGH"
        elif score >= 40:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        return RiskResult(
            score=score,
            severity=severity,
            reasons=reasons,
            core_affected=core_affected,
            test_affected=test_affected,
            other_affected=other_affected
        )