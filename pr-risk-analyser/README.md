# PR Risk Analyzer

A static analysis tool that analyzes GitHub Pull Requests before they get merged into production. It scans your codebase, builds dependency graphs, and calculates the blast radius of any change — telling you exactly what will break before it breaks in production.

---

## The Problem

When you change one file in a large codebase, you rarely know what else breaks. You run your local tests, everything passes, you merge — and then something completely unrelated fails in production. This invisible chain of breakage is the blast radius of your change.

I built this tool because I felt this pain personally. PR Risk Analyzer makes that blast radius visible before merge.

---

## Demo — Real Output on FastAPI Codebase

```
===== BLAST RADIUS =====

CRITICAL — Core modules affected (8):
 - routing
 - applications
 - utils
 - models
 - types
 - encoders
 - datastructures
 - params

TEST FILES affected (89):
 (89 test files — low production risk)

OTHER modules affected (5):
 - shared
 - v2
 - docs

===== RISK ANALYSIS =====
Risk Score: 67/100
Severity: HIGH

Reasons:
 - 8 core modules affected (critical)
 - 89 test files affected (low risk)
 - 5 other modules affected

===== CIRCULAR DEPENDENCIES =====
 - utils -> routing
 - utils -> oauth2
 - models -> base
 - responses -> sse
 (+ 16 more cycles detected)
```

---

## How It Works

### Step 1 — AST Parsing
Every Python file in the repository is parsed using Python's built-in `ast` library. The parser extracts functions, classes, and imports from each file — including async functions. This gives us raw symbol data for the entire codebase.

### Step 2 — Graph Construction
From the parsed symbols, two directed graphs are built using NetworkX:

**Call Graph** — maps which function calls which other function. Directed edges represent call relationships. Used for function-level impact analysis.

**Import Graph** — maps which file imports which other file. Directed edges represent dependency relationships. Used for module-level blast radius calculation.

### Step 3 — Blast Radius (DFS on Reversed Import Graph)
When a PR changes a file, the tool runs Depth First Search on the reversed import graph — following edges backwards to find everything that depends on the changed module. Time complexity is O(N+E) where N is nodes and E is edges.

### Step 4 — Risk Scoring
Affected modules are split into three tiers:
- **Core modules** — routing, applications, utils, models, etc. High weight.
- **Test files** — anything prefixed with `test_`. Low weight.
- **Other** — tutorials, docs, utilities.

Score is calculated based on core modules affected only. A PR breaking 89 test files but 0 core modules is genuinely low risk. A PR breaking 8 core modules is genuinely high risk.

### Step 5 — Cycle Detection
Circular dependencies are detected in the import graph using NetworkX's `simple_cycles` (Johnson's Algorithm, O((N+E)(C+1))). Import cycles are structural failures — they prevent the program from loading. Function cycles are excluded because they may be intentional recursion.

### Step 6 — Architecture Validation
New imports introduced by the PR are extracted and validated against architecture rules — catching forbidden dependencies before they enter the codebase.

---

## Architecture

## Architecture

```
src/
├── parser/
│   └── ast_parser.py           # AST-based code analysis
├── graphs/
│   ├── import_graph.py         # Module dependency graph
│   ├── call_graph.py           # Function call graph
│   └── cycle_detector.py       # Cycle detection
├── diff/
│   ├── github_pr_fetcher.py    # GitHub API integration
│   ├── git_diff_parser.py      # Diff text parsing
│   ├── pr_diff_analyzer.py     # Changed module extraction
│   └── edge_analyzer.py        # New dependency detection
├── scorer/
│   └── risk_scorer.py          # Tiered risk calculation
├── rules/
│   └── architecture_rules.py   # Forbidden dependency rules
├── schemas/
│   └── symbols.py              # Data models
├── code_optimization/
│   └── caching.py              # File hash caching
└── orchestrator/
    └── pipeline.py             # Full analysis pipeline
```
---

## Tech Stack

- **Python** — core language
- **AST** — built-in Python library for static code parsing
- **NetworkX** — graph construction and traversal
- **GitHub API** — real PR diff fetching

---

## Installation

```bash
git clone https://github.com/yourusername/pr-risk-analyser
cd pr-risk-analyser
pip install -r requirements.txt
```

---

## Usage

```python
from src.orchestrator.pipeline import PRAnalysisPipeline

pipeline = PRAnalysisPipeline()

result = pipeline.run_from_github_pr(
    owner="fastapi",
    repo="fastapi",
    pr_number=1234,
    token="your_github_token",
    repo_path="path/to/cloned/repo"
)
```

Or against a local repo directly:

```python
result = pipeline.run(
    repo_path="path/to/your/repo",
    changed_files=["src/payments/checkout.py"]
)
```

---

## Complexity Analysis

| Component | Time Complexity | Notes |
|-----------|----------------|-------|
| AST Parsing | O(F×L) | F files, L avg lines |
| Graph Construction | O(N+E) | N nodes, E edges |
| Blast Radius (DFS) | O(N+E) | Reversed graph traversal |
| Cycle Detection | O((N+E)(C+1)) | Johnson's Algorithm |
| Risk Scoring | O(M) | M affected modules |

---

## Known Limitations

- **Python only** — does not analyze JavaScript, Java, or other languages
- **Static analysis** — cannot detect runtime issues or dynamic imports
- **Local clone required** — repository must be cloned locally for graph construction
- **New functions** — functions added by a PR have no existing dependents, so function impact correctly shows zero

---

## Planned Improvements

- GitHub Actions integration for automatic CI/CD triggering
- Multi-language support starting with JavaScript
- Cognitive layer using AI agents for contextual risk reasoning
- Repo-scoped caching for O(changed×L) repeated run performance
- Percentage-based scoring relative to total codebase size

---

## What I Learned

This project taught me how production engineering teams think about code safety. Static analysis, dependency graphs, and blast radius are real concepts used at companies like Google, Meta, and Semgrep. Building this from scratch gave me deep understanding of AST parsing, graph algorithms, DFS traversal, and the difference between structural failures (import cycles) and runtime failures (function cycles).

---

*Built by a 1st year CS student who got tired of mysterious production failures.*