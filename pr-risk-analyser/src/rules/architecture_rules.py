from src.schemas.symbols import ArchitectureViolation


class ArchitectureRuleEngine:

    FORBIDDEN_DEPENDENCIES = [
        ("analytics", "pricing"),
    ]

    def validate(self, graph):
        violations = []

        for source, target in graph.edges():

            for forbidden_source, forbidden_target in self.FORBIDDEN_DEPENDENCIES:

                if (
                    source == forbidden_source
                    and target == forbidden_target
                ):

                    violations.append(
                        ArchitectureViolation(
                            source=source,
                            target=target,
                            message=(
                                f"{source} is not allowed "
                                f"to directly depend on {target}"
                            )
                        )
                    )

        return violations