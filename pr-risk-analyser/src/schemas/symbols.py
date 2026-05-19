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
    
@dataclass
class ArchitectureViolation:
    source: str
    target: str
    message: str
 
@dataclass
class RiskResult:
    score: int
    severity: str
    reasons: list[str] = field(default_factory=list)
    
        
@dataclass
class AnalysisResult:
    file_analyses: list[FileAnalysis]
    affected_modules: list[str]
    downstream_functions: list[str]
    risk_result: RiskResult
    violations: list[ArchitectureViolation]
    
