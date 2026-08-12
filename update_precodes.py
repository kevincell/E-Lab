import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Question

starter_c = """#include <stdio.h>

int main() {
    // Write your C code here
    
    return 0;
}
"""

starter_cpp = """#include <iostream>
using namespace std;

int main() {
    // Write your C++ code here
    
    return 0;
}
"""

starter_java = """import java.util.Scanner;

public class Solution {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        // Write your Java code here
        
    }
}
"""

starter_python = """import sys

def solve():
    # Write your Python code here
    pass

if __name__ == '__main__':
    solve()
"""

questions = Question.objects.filter(module__category="placement_training")
for q in questions:
    q.starter_codes = {
        "50": starter_c,
        "54": starter_cpp,
        "62": starter_java,
        "71": starter_python
    }
    q.save()

print(f"Updated starter_codes for {questions.count()} questions.")
