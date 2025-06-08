import time
import traceback
from typing import Callable, List

# Registry for test functions
TESTS: List[Callable] = []

# Decorator (optional — still usable)
def test(func: Callable):
    TESTS.append(func)
    return func

# Registration helper for external files
# Note: all tests registered must start with test_ in the name.
def register_tests(scope: dict):
    for name, obj in scope.items():
        if name.startswith("test_") and callable(obj):
            TESTS.append(obj)

# Main test runner
def run_tests():
    print("Running tests...\n")
    for func in TESTS:
        name = func.__name__
        start_wall = time.time()
        start_cpu = time.process_time()
        try:
            func()
            status = "[PASS]"
        except Exception as e:
            status = "[FAIL]"
            traceback.print_exc()
        end_wall = time.time()
        end_cpu = time.process_time()
        wall_time = end_wall - start_wall
        cpu_time = end_cpu - start_cpu
        print(f"{status} {name:<20} | Wall: {wall_time:.4f}s | CPU: {cpu_time:.4f}s")

# Allow importing this in test files
__all__ = ["test", "register_tests", "run_tests"]