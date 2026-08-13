import os
import sys

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from core.sandbox import run_code

# Test Python
print("Testing Python...")
python_code = """
print("Hello from Python!")
"""
res = run_code("python", python_code)
print(res)
assert res["status_id"] == 3
assert res["stdout"] == "Hello from Python!"

# Test Java
print("Testing Java...")
java_code = """
public class Solution {
    public static void main(String[] args) {
        System.out.println("Hello from Java!");
    }
}
"""
res = run_code("java", java_code)
print(res)
assert res["status_id"] == 3
assert res["stdout"] == "Hello from Java!"

print("ALL TESTS PASSED")
