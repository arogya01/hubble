import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from lib.semantic_search import SemanticSearch

search = SemanticSearch()

# 1. Test shape (should be 384)
vec = search.generate_embedding("apple")
assert vec.shape[0] == 384, f"Expected 384, got {vec.shape[0]}"

# 2. Test whitespace error
try:
    search.generate_embedding("   ")
    assert False, "Should have raised ValueError"
except ValueError:
    print("✓ Whitespace validation passed")

# 3. Test case insensitivity (dot product should be ~1.0)
v1 = search.generate_embedding("Paddington")
v2 = search.generate_embedding("paddington")
dot = sum(a * b for a, b in zip(v1, v2))
assert dot > 0.99, f"Expected high similarity, got {dot}"
print("✓ Case-insensitivity passed")
