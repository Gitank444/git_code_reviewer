from dataclasses import dataclass, field


@dataclass
class FunctionSymbol:
    name: str
    calls: list[str] = field(default_factory=list)


@dataclass
class FileAnalysis:
    file_path: str
    imports: list[str] = field(default_factory=list)
    functions: list[FunctionSymbol] = field(default_factory=list)
    classes: list[str] = field(default_factory=list)