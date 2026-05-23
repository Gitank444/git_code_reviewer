# import hashlib
# import json
# from pathlib import Path

# class AnalysisCache:
#     def __init__(self, cache_path=".analysis_cache.json"):
#         self.cache_path = Path(cache_path)
#         self.cache = self._load()
    
#     def _load(self):
#         if self.cache_path.exists():
#             return json.loads(self.cache_path.read_text())
#         return {}
    
#     def has_changed(self, file_path: Path) -> bool:
#         current_hash = hashlib.md5(
#             file_path.read_bytes()
#         ).hexdigest()
#         return self.cache.get(str(file_path)) != current_hash
    
#     def update(self, file_path: Path):
#         self.cache[str(file_path)] = hashlib.md5(
#             file_path.read_bytes()
#         ).hexdigest()
#         self.cache_path.write_text(json.dumps(self.cache))