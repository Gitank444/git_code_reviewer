from pathlib import Path

from src.parser.ast_parser import analyze_file
from src.graphs.import_graph import ImportGraph
from src.graphs.call_graph import CallGraph
repo_path = Path("src/sample_repo")

python_files = repo_path.glob("*.py")

graph = ImportGraph()
call_graph = CallGraph()

for file in python_files:
    result = analyze_file(file)

    print("\n====================")
    print(f"FILE: {result.file_path}")

    print("\nImports:")
    for imp in result.imports:
        print(f" - {imp}")

    print("\nFunctions:")
    for func in result.functions:
        print(f" - {func.name}")
        print(f"   Calls: {func.calls}")

    graph.add_file_analysis(result)
    call_graph.add_file_analysis(result)

graph.show_dependencies()

print("\n===== BLAST RADIUS ANALYSIS =====")
print("If pricing changes:")

dependents = graph.get_all_dependents("pricing")

for dep in dependents:
    print(f" - {dep} may be affected")

call_graph.show_graph()

print("\n===== FUNCTION IMPACT ANALYSIS =====")
print("If calculate_total changes:")

downstream = call_graph.get_downstream_calls("calculate_total")

for func in downstream:
    print(f" - {func} may be affected")