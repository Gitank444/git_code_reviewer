from src.schemas.symbols import RiskResult


class RiskScorer:

    CRITICAL_MODULES = [
        "pricing",
        "auth",
        "payment",
        "database"
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

            reasons.append(
                f"{changed_module} is a critical module"
            )

        # Blast radius risk
        affected_count = len(affected_modules)

        blast_radius_score = affected_count * 10

        score += blast_radius_score

        reasons.append(
            f"{affected_count} downstream modules affected"
        )

        # Function-chain depth risk
        function_depth = len(downstream_functions)

        function_score = function_depth * 5

        score += function_score

        reasons.append(
            f"{function_depth} downstream function calls detected"
        )

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
            reasons=reasons
        )