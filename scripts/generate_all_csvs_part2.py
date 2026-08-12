import csv
import os

OUTPUT_DIR = "d:/New folder/E-Lab/generated_level_question_csvs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

STARTER_CODE = """#include <stdio.h>

int main(void)
{
    /* Read from stdin and print exact output only. */
    return 0;
}
"""

HEADERS = [
    "Question_ID", "Title", "Topic", "Level", "Level_Range", "Difficulty", "Status",
    "Score", "Max_Score", "Problem_Statement", "Starter_Code", "Is_Active", "Is_Mandatory",
    "Time_Limit", "Memory_Limit_KB",
    "Test1_Input", "Test1_Output", "Test2_Input", "Test2_Output", "Test3_Input", "Test3_Output",
    "Test4_Input", "Test4_Output", "Test5_Input", "Test5_Output", "Test6_Input", "Test6_Output",
    "Test7_Input", "Test7_Output", "Test8_Input", "Test8_Output", "Test9_Input", "Test9_Output",
    "Test10_Input", "Test10_Output"
]

def make_row(qid, title, topic, level, level_range, diff, prob_stmt, is_mand, tests):
    row = [
        qid, title, topic, str(level), level_range, diff, "Not Attempted",
        "0", "1", prob_stmt.strip(), STARTER_CODE, "true", "true" if is_mand else "false",
        "2", "128000"
    ]
    test_cells = []
    for i in range(10):
        if i < len(tests):
            inp, outp = tests[i]
            test_cells.extend([str(inp), str(outp)])
        else:
            inp, outp = tests[i % len(tests)]
            test_cells.extend([str(inp), str(outp)])
    row.extend(test_cells)
    return row

def write_csv(filename, rows):
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)
        writer.writerows(rows)
    print(f"Generated {filename} with {len(rows)} questions.")

# MODULE 6: Functions
m6_rows = [
    make_row("E001", "Square Value", "Functions", 6, "Easy", "Easy", "Write a function to return square of n. Read n and print square.", False, [("2", "4"), ("5", "25"), ("0", "0"), ("-3", "9"), ("10", "100")]),
    make_row("E002", "Maximum Two", "Functions", 6, "Easy", "Easy", "Write a function to return max of two integers. Read a b and print max.", False, [("1 2", "2"), ("5 3", "5"), ("-1 -5", "-1"), ("0 0", "0"), ("100 99", "100")]),
    make_row("E003", "Sum Three", "Functions", 6, "Easy", "Easy", "Write a function to return sum of three integers. Read a b c and print sum.", False, [("1 2 3", "6"), ("10 20 30", "60"), ("5 5 5", "15"), ("0 0 1", "1"), ("-3 3 6", "6")]),
    make_row("E004", "Even Flag", "Functions", 6, "Easy", "Easy", "Write a function returning 1 if even else 0. Read n and print result.", False, [("0", "1"), ("1", "0"), ("2", "1"), ("3", "0"), ("10", "1")]),
    make_row("E005", "Digit Sum", "Functions", 6, "Easy", "Easy", "Write a function returning sum of digits. Read non-negative n and print result.", False, [("123", "6"), ("0", "0"), ("999", "27"), ("1001", "2"), ("4567", "22")]),
    make_row("E006", "Cube Value", "Functions", 6, "Easy", "Easy", "Write a function returning cube of n. Read n and print cube.", False, [("2", "8"), ("3", "27"), ("0", "0"), ("-2", "-8"), ("5", "125")]),
    make_row("E007", "Minimum Two", "Functions", 6, "Easy", "Easy", "Write a function returning min of two integers. Read a b and print min.", False, [("1 2", "1"), ("5 3", "3"), ("-1 -5", "-5"), ("0 0", "0"), ("100 99", "99")]),
    make_row("E008", "Absolute Value", "Functions", 6, "Easy", "Easy", "Write a function returning absolute value. Read n and print abs(n).", False, [("-5", "5"), ("5", "5"), ("0", "0"), ("-100", "100"), ("42", "42")]),
    make_row("E009", "Is Positive", "Functions", 6, "Easy", "Easy", "Write a function returning 1 if n > 0 else 0. Read n and print result.", False, [("5", "1"), ("-5", "0"), ("0", "0"), ("100", "1"), ("-1", "0")]),
    make_row("E010", "Double Value", "Functions", 6, "Easy", "Easy", "Write a function returning 2*n. Read n and print result.", False, [("5", "10"), ("0", "0"), ("-3", "-6"), ("50", "100"), ("42", "84")]),
    make_row("M001", "Power Function", "Functions", 6, "Medium", "Medium", "Write a function to compute base^exp. Read base exp (>=0) and print result.", False, [("2 3", "8"), ("5 0", "1"), ("3 4", "81"), ("10 2", "100"), ("7 2", "49")]),
    make_row("M002", "GCD Function", "Functions", 6, "Medium", "Medium", "Write a function to compute GCD of two positive integers. Read a b and print GCD.", False, [("12 18", "6"), ("7 5", "1"), ("100 10", "10"), ("81 27", "27"), ("14 21", "7")]),
    make_row("M003", "Array Sum Function", "Functions", 6, "Medium", "Medium", "Write a function taking array and length, returning sum. Read n and n integers, print sum.", False, [("3 1 2 3", "6"), ("1 5", "5"), ("4 10 20 30 40", "100"), ("2 -1 1", "0"), ("3 5 5 5", "15")]),
    make_row("M004", "Array Max Function", "Functions", 6, "Medium", "Medium", "Write a function taking array and length, returning max. Read n and n integers, print max.", False, [("3 1 2 3", "3"), ("1 5", "5"), ("4 10 20 30 40", "40"), ("2 -1 1", "1"), ("3 5 5 5", "5")]),
    make_row("M005", "Reverse Array Function", "Functions", 6, "Medium", "Medium", "Write a function to reverse array in place. Read n and n integers, print reversed array.", False, [("3 1 2 3", "3 2 1"), ("1 5", "5"), ("4 10 20 30 40", "40 30 20 10"), ("2 -1 1", "1 -1"), ("3 5 5 5", "5 5 5")]),
    make_row("M006", "Factorial Function", "Functions", 6, "Medium", "Medium", "Write a function computing factorial of n (0 to 12). Read n and print result.", False, [("5", "120"), ("0", "1"), ("3", "6"), ("6", "720"), ("4", "24")]),
    make_row("M007", "Is Prime Function", "Functions", 6, "Medium", "Medium", "Write a function returning 1 if prime else 0. Read positive n and print result.", False, [("7", "1"), ("4", "0"), ("2", "1"), ("1", "0"), ("11", "1")]),
    make_row("M008", "Fibonacci Function", "Functions", 6, "Medium", "Medium", "Write a function returning nth Fibonacci number (0th=0, 1st=1). Read n and print result.", False, [("6", "8"), ("0", "0"), ("1", "1"), ("7", "13"), ("10", "55")]),
    make_row("M009", "Count Vowels Function", "Functions", 6, "Medium", "Medium", "Write a function taking string and returning vowel count. Read lowercase word and print count.", False, [("hello", "2"), ("sky", "0"), ("education", "5"), ("apple", "2"), ("code", "2")]),
    make_row("M010", "Average Function", "Functions", 6, "Medium", "Medium", "Write a function taking array and length, returning integer average. Read n and n integers, print average.", False, [("3 1 2 3", "2"), ("4 10 20 30 40", "25"), ("1 5", "5"), ("2 0 10", "5"), ("5 5 5 5 5", "5")]),
    # Hard Mandatory (Lab Manual Q12, Q13, Q14, Q16)
    make_row("LM001", "Matrix Multiplication", "Lab Manual Functions", 6, "Hard", "Hard", "Write a C program using functions to read two matrices A (M x N) and B (P x Q) and compute product if compatible.\nRead M N then M*N integers. Read P Q then P*Q integers. If N != P print 'Incompatible'. Else print resultant matrix row by row (space separated elements).", True, [("2 2 1 2 3 4 2 2 1 0 0 1", "1 2\n3 4"), ("2 3 1 2 3 4 5 6 2 2 1 2 3 4", "Incompatible"), ("1 2 1 2 2 1 3 4", "11"), ("2 1 2 3 1 2 4 5", "8 10\n12 15"), ("1 1 5 1 1 6", "30")]),
    make_row("LM002", "Matrix Operations 2D", "Lab Manual Functions", 6, "Hard", "Hard", "Write a C program using functions readmat(), rowsum(), colsum(), totsum() and printmat() for 2D array A.\nRead R C then R*C integers. Output exact format:\nRow Sums: <space separated sum of each row>\nCol Sums: <space separated sum of each col>\nTotal Sum: <sum of all elements>", True, [("2 2 1 2 3 4", "Row Sums: 3 7\nCol Sums: 4 6\nTotal Sum: 10"), ("2 3 1 1 1 2 2 2", "Row Sums: 3 6\nCol Sums: 3 3 3\nTotal Sum: 9"), ("1 3 10 20 30", "Row Sums: 60\nCol Sums: 10 20 30\nTotal Sum: 60"), ("3 1 5 5 5", "Row Sums: 5 5 5\nCol Sums: 15\nTotal Sum: 15"), ("2 2 0 0 0 0", "Row Sums: 0 0\nCol Sums: 0 0\nTotal Sum: 0")]),
    make_row("LM003", "Linear Search Function", "Lab Manual Functions", 6, "Hard", "Hard", "Write a C program to perform a linear search for a given key integer in a single dimensional array of numbers and report success or failure using functions.\nRead N, N integers, then Key. Print 'Success: Element found' or 'Failure: Element not found'.", True, [("4 10 20 30 40 30", "Success: Element found"), ("4 10 20 30 40 25", "Failure: Element not found"), ("1 5 5", "Success: Element found"), ("3 1 2 3 1", "Success: Element found"), ("3 1 2 3 99", "Failure: Element not found")]),
    make_row("LM004", "Bubble Sort Function Choice", "Lab Manual Functions", 6, "Hard", "Hard", "Write a C program to implement bubble sort technique using function to sort N integers in ascending/descending as per user preference.\nRead integer choice (1 for Ascending, 2 for Descending), then N, then N integers. Print sorted array space separated.", True, [("1 4 4 3 2 1", "1 2 3 4"), ("2 4 1 2 3 4", "4 3 2 1"), ("1 3 5 1 3", "1 3 5"), ("2 3 5 1 3", "5 3 1"), ("1 1 42", "42")]),
    # Hard Filler (5)
    make_row("H001", "Recursive Fibonacci", "Functions", 6, "Hard", "Hard", "Write a recursive function for nth Fibonacci number. Read n and print result.", False, [("6", "8"), ("7", "13"), ("0", "0"), ("1", "1"), ("10", "55")]),
    make_row("H002", "Recursive Factorial", "Functions", 6, "Hard", "Hard", "Write a recursive function for factorial. Read n (0 to 12) and print result.", False, [("5", "120"), ("0", "1"), ("3", "6"), ("6", "720"), ("4", "24")]),
    make_row("H003", "Matrix Trace Function", "Functions", 6, "Hard", "Hard", "Write a function returning trace of square matrix. Read N then N*N integers of matrix, print trace.", False, [("2 1 2 3 4", "5"), ("3 1 0 0 0 2 0 0 0 3", "6"), ("1 42", "42"), ("2 0 0 0 0", "0"), ("3 1 1 1 1 1 1 1 1 1", "3")]),
    make_row("H004", "Prime Range Count Function", "Functions", 6, "Hard", "Hard", "Write a function counting primes in range [start, end]. Read start end, print count.", False, [("1 10", "4"), ("10 20", "4"), ("1 100", "25"), ("14 16", "0"), ("2 5", "3")]),
    make_row("H005", "Second Min Function", "Functions", 6, "Hard", "Hard", "Write a function returning second smallest distinct element. Read n and n distinct integers, print second min.", False, [("3 3 1 2", "2"), ("4 10 5 8 2", "5"), ("3 5 4 3", "4"), ("4 1 2 3 4", "2"), ("5 10 20 30 40 50", "20")])
]
write_csv("Module6_Functions_Levels.csv", m6_rows)

# MODULE 7: Pointers
m7_rows = [
    make_row("E001", "Pointer Dereference", "Pointers", 7, "Easy", "Easy", "Read integer n. Using a pointer to n, print its value.", False, [("5", "5"), ("-10", "-10"), ("0", "0"), ("100", "100"), ("42", "42")]),
    make_row("E002", "Pointer Update", "Pointers", 7, "Easy", "Easy", "Read n. Add 10 to n using a pointer and print updated value.", False, [("5", "15"), ("0", "10"), ("-10", "0"), ("90", "100"), ("42", "52")]),
    make_row("E003", "Pointer Swap", "Pointers", 7, "Easy", "Easy", "Write a function swap(int *a, int *b). Read two integers, swap via pointers, and print space separated.", False, [("1 2", "2 1"), ("5 3", "3 5"), ("-1 9", "9 -1"), ("0 0", "0 0"), ("100 99", "99 100")]),
    make_row("E004", "Pointer Add Two", "Pointers", 7, "Easy", "Easy", "Read a b. Compute sum using pointers and print sum.", False, [("1 2", "3"), ("10 20", "30"), ("-5 5", "0"), ("100 200", "300"), ("7 8", "15")]),
    make_row("E005", "Pointer Is Equal", "Pointers", 7, "Easy", "Easy", "Read two integers. Compare them using pointers. Print 1 if equal else 0.", False, [("5 5", "1"), ("5 3", "0"), ("0 0", "1"), ("-1 1", "0"), ("42 42", "1")]),
    make_row("E006", "Pointer Increment", "Pointers", 7, "Easy", "Easy", "Read n. Increment via pointer (*ptr)++ and print.", False, [("5", "6"), ("0", "1"), ("-1", "0"), ("99", "100"), ("42", "43")]),
    make_row("E007", "Pointer Decrement", "Pointers", 7, "Easy", "Easy", "Read n. Decrement via pointer (*ptr)-- and print.", False, [("5", "4"), ("1", "0"), ("0", "-1"), ("100", "99"), ("42", "41")]),
    make_row("E008", "Pointer Max Two", "Pointers", 7, "Easy", "Easy", "Read a b. Find maximum using pointers and print.", False, [("1 2", "2"), ("5 3", "5"), ("-1 -5", "-1"), ("0 0", "0"), ("100 99", "100")]),
    make_row("E009", "Pointer Min Two", "Pointers", 7, "Easy", "Easy", "Read a b. Find minimum using pointers and print.", False, [("1 2", "1"), ("5 3", "3"), ("-1 -5", "-5"), ("0 0", "0"), ("100 99", "99")]),
    make_row("E010", "Pointer Copy Value", "Pointers", 7, "Easy", "Easy", "Read n. Copy its value to variable m using pointer and print m.", False, [("42", "42"), ("0", "0"), ("-5", "-5"), ("100", "100"), ("7", "7")]),
    make_row("M001", "Pointer Array Traversal", "Pointers", 7, "Medium", "Medium", "Read n and n integers. Traverse array using pointer arithmetic (ptr + i) and print elements space separated.", False, [("3 1 2 3", "1 2 3"), ("1 5", "5"), ("4 10 20 30 40", "10 20 30 40"), ("2 -1 1", "-1 1"), ("3 5 5 5", "5 5 5")]),
    make_row("M002", "Pointer Array Max", "Pointers", 7, "Medium", "Medium", "Read n and n integers. Find maximum using pointer traversal and print.", False, [("3 1 2 3", "3"), ("1 5", "5"), ("4 10 20 30 40", "40"), ("2 -1 1", "1"), ("3 5 5 5", "5")]),
    make_row("M003", "Pointer Reverse Array", "Pointers", 7, "Medium", "Medium", "Read n and n integers. Reverse array using two pointers (left and right) and print space separated.", False, [("3 1 2 3", "3 2 1"), ("1 5", "5"), ("4 10 20 30 40", "40 30 20 10"), ("2 -1 1", "1 -1"), ("3 5 5 5", "5 5 5")]),
    make_row("M004", "Pointer String Length", "Pointers", 7, "Medium", "Medium", "Read a word. Compute length using pointer traversal (while (*str != '\\0')) and print.", False, [("hello", "5"), ("a", "1"), ("programming", "11"), ("code", "4"), ("openai", "6")]),
    make_row("M005", "Pointer Count Vowels", "Pointers", 7, "Medium", "Medium", "Read lowercase word. Count vowels using pointer traversal and print.", False, [("hello", "2"), ("sky", "0"), ("education", "5"), ("apple", "2"), ("code", "2")]),
    make_row("M006", "Pointer Array Min", "Pointers", 7, "Medium", "Medium", "Read n and n integers. Find minimum using pointer traversal and print.", False, [("3 1 2 3", "1"), ("1 5", "5"), ("4 10 20 30 40", "10"), ("2 -1 1", "-1"), ("3 5 5 5", "5")]),
    make_row("M007", "Pointer Copy Array", "Pointers", 7, "Medium", "Medium", "Read n and n integers. Copy to second array using pointers and print second array space separated.", False, [("3 1 2 3", "1 2 3"), ("1 42", "42"), ("2 -1 -2", "-1 -2"), ("4 0 0 0 0", "0 0 0 0"), ("3 9 8 7", "9 8 7")]),
    make_row("M008", "Pointer Count Evens", "Pointers", 7, "Medium", "Medium", "Read n and n integers. Count even numbers using pointer arithmetic and print.", False, [("3 1 2 3", "1"), ("4 10 20 30 40", "4"), ("1 5", "0"), ("2 2 4", "2"), ("3 1 3 5", "0")]),
    make_row("M009", "Pointer Search Key", "Pointers", 7, "Medium", "Medium", "Read n, n integers, key. Search key using pointer arithmetic. Print 1 if found else 0.", False, [("3 1 2 3 2", "1"), ("3 1 2 3 5", "0"), ("1 9 9", "1"), ("3 4 5 6 4", "1"), ("3 4 5 6 7", "0")]),
    make_row("M010", "Pointer Array Average", "Pointers", 7, "Medium", "Medium", "Read n and n integers. Compute integer average using pointer sum and print.", False, [("3 1 2 3", "2"), ("4 10 20 30 40", "25"), ("1 5", "5"), ("2 0 10", "5"), ("5 5 5 5 5", "5")]),
    # Hard Mandatory (Lab Manual Q7)
    make_row("LM001", "Pointer Array Sum Manual", "Lab Manual Pointers", 7, "Hard", "Hard", "Write a C program to read N integers into an array A and find the sum of elements using pointers.\nRead integer N then N integers. Traverse array using pointers and print exact integer sum.", True, [("4 10 20 30 40", "100"), ("3 1 2 3", "6"), ("1 5", "5"), ("3 -1 2 -3", "-2"), ("5 1 1 1 1 1", "5")]),
    # Hard Filler (5)
    make_row("H001", "Pointer String Reverse", "Pointers", 7, "Hard", "Hard", "Read a word. Reverse string in place using two pointers and print.", False, [("hello", "olleh"), ("abc", "cba"), ("a", "a"), ("code", "edoc"), ("racecar", "racecar")]),
    make_row("H002", "Pointer Palindrome Check", "Pointers", 7, "Hard", "Hard", "Read a word. Check palindrome using two pointers. Print Palindrome or Not Palindrome.", False, [("madam", "Palindrome"), ("hello", "Not Palindrome"), ("racecar", "Palindrome"), ("level", "Palindrome"), ("code", "Not Palindrome")]),
    make_row("H003", "Pointer Sort Array", "Pointers", 7, "Hard", "Hard", "Read n and n integers. Sort array ascending using pointer arithmetic and print space separated.", False, [("3 3 1 2", "1 2 3"), ("4 10 5 8 2", "2 5 8 10"), ("1 42", "42"), ("3 5 5 5", "5 5 5"), ("2 9 1", "1 9")]),
    make_row("H004", "Pointer Count Words", "Pointers", 7, "Hard", "Hard", "Read sentence (words separated by single space). Count words using pointer traversal and print.", False, [("hello world", "2"), ("code lab test", "3"), ("a", "1"), ("one two three four", "4"), ("openai", "1")]),
    make_row("H005", "Pointer Second Largest", "Pointers", 7, "Hard", "Hard", "Read n and n distinct integers. Find second largest using pointer traversal and print.", False, [("3 1 2 3", "2"), ("4 10 20 30 40", "30"), ("3 5 4 3", "4"), ("2 1 2", "1"), ("5 10 50 20 30 40", "40")])
]
write_csv("Module7_Pointers_Levels.csv", m7_rows)

# MODULE 8: Structures
m8_rows = [
    make_row("E001", "Point X Y Sum", "Structures", 8, "Easy", "Easy", "Define struct Point {int x; int y;}. Read x y and print x+y.", False, [("2 3", "5"), ("10 20", "30"), ("-5 5", "0"), ("0 0", "0"), ("100 200", "300")]),
    make_row("E002", "Rectangle Area Struct", "Structures", 8, "Easy", "Easy", "Define struct Rect {int l; int b;}. Read l b and print area l*b.", False, [("2 3", "6"), ("5 5", "25"), ("10 1", "10"), ("7 8", "56"), ("12 4", "48")]),
    make_row("E003", "Student Marks Sum", "Structures", 8, "Easy", "Easy", "Define struct Student {int m1; int m2;}. Read m1 m2 and print sum.", False, [("40 50", "90"), ("80 90", "170"), ("0 0", "0"), ("100 100", "200"), ("35 45", "80")]),
    make_row("E004", "Book Price", "Structures", 8, "Easy", "Easy", "Define struct Book {int id; int price;}. Read id price and print price.", False, [("101 500", "500"), ("102 250", "250"), ("1 100", "100"), ("5 999", "999"), ("42 50", "50")]),
    make_row("E005", "Time Total Minutes", "Structures", 8, "Easy", "Easy", "Define struct Time {int h; int m;}. Read h m and print total minutes h*60+m.", False, [("1 30", "90"), ("2 0", "120"), ("0 45", "45"), ("10 10", "610"), ("5 15", "315")]),
    make_row("E006", "Complex Real Part", "Structures", 8, "Easy", "Easy", "Define struct Complex {int real; int imag;}. Read real imag and print real.", False, [("5 3", "5"), ("-2 4", "-2"), ("0 10", "0"), ("100 -50", "100"), ("42 7", "42")]),
    make_row("E007", "Circle Area Approx", "Structures", 8, "Easy", "Easy", "Define struct Circle {int r;}. Read r and print integer area 22*r*r/7.", False, [("7", "154"), ("14", "616"), ("1", "3"), ("21", "1386"), ("35", "3850")]),
    make_row("E008", "Item Total Cost", "Structures", 8, "Easy", "Easy", "Define struct Item {int qty; int price;}. Read qty price and print total qty*price.", False, [("2 50", "100"), ("5 10", "50"), ("10 100", "1000"), ("1 99", "99"), ("3 30", "90")]),
    make_row("E009", "Distance Origin Squared", "Structures", 8, "Easy", "Easy", "Define struct Point {int x; int y;}. Read x y and print x*x + y*y.", False, [("3 4", "25"), ("1 2", "5"), ("0 5", "25"), ("-3 -4", "25"), ("10 10", "200")]),
    make_row("E010", "Employee Salary", "Structures", 8, "Easy", "Easy", "Define struct Emp {int id; int sal;}. Read id sal and print sal.", False, [("1 50000", "50000"), ("2 60000", "60000"), ("101 10000", "10000"), ("5 75000", "75000"), ("42 99999", "99999")]),
    make_row("M001", "Point Distance Squared", "Structures", 8, "Medium", "Medium", "Read two points x1 y1 x2 y2. Print squared distance (x2-x1)^2 + (y2-y1)^2.", False, [("0 0 3 4", "25"), ("1 1 4 5", "25"), ("0 0 0 0", "0"), ("-1 -1 1 1", "8"), ("10 10 20 20", "200")]),
    make_row("M002", "Complex Add", "Structures", 8, "Medium", "Medium", "Read r1 i1 r2 i2. Compute sum of two complex numbers and print real imag space separated.", False, [("1 2 3 4", "4 6"), ("5 -3 -2 4", "3 1"), ("0 0 1 1", "1 1"), ("10 20 30 40", "40 60"), ("-5 -5 5 5", "0 0")]),
    make_row("M003", "Student Average", "Structures", 8, "Medium", "Medium", "Read marks m1 m2 m3. Print integer average (m1+m2+m3)/3.", False, [("80 90 100", "90"), ("40 50 60", "50"), ("70 70 70", "70"), ("30 40 50", "40"), ("100 100 100", "100")]),
    make_row("M004", "Time Add", "Structures", 8, "Medium", "Medium", "Read h1 m1 h2 m2. Add times properly handling minutes >= 60. Print total hours and minutes space separated.", False, [("1 30 2 45", "4 15"), ("0 50 0 20", "1 10"), ("2 0 3 0", "5 0"), ("10 45 1 15", "12 0"), ("5 55 0 10", "6 5")]),
    make_row("M005", "Rectangle Perimeter Struct", "Structures", 8, "Medium", "Medium", "Read l b of struct Rect. Print perimeter 2*(l+b).", False, [("2 3", "10"), ("5 5", "20"), ("10 1", "22"), ("7 8", "30"), ("12 4", "32")]),
    make_row("M006", "Student Pass Check", "Structures", 8, "Medium", "Medium", "Read id m1 m2. Print Pass if average >= 40 else Fail.", False, [("101 40 40", "Pass"), ("102 30 40", "Fail"), ("103 80 90", "Pass"), ("104 0 100", "Pass"), ("105 39 39", "Fail")]),
    make_row("M007", "Oldest Employee", "Structures", 8, "Medium", "Medium", "Read age of 3 employees age1 age2 age3. Print max age.", False, [("25 30 28", "30"), ("40 50 60", "60"), ("22 22 22", "22"), ("55 45 35", "55"), ("18 20 19", "20")]),
    make_row("M008", "Highest Priced Book", "Structures", 8, "Medium", "Medium", "Read prices of 3 books p1 p2 p3. Print max price.", False, [("100 250 150", "250"), ("500 400 300", "500"), ("99 99 99", "99"), ("10 20 30", "30"), ("1000 800 1200", "1200")]),
    make_row("M009", "Vector Dot Product", "Structures", 8, "Medium", "Medium", "Read 3D vectors x1 y1 z1 x2 y2 z2. Print dot product x1*x2 + y1*y2 + z1*z2.", False, [("1 2 3 4 5 6", "32"), ("1 0 0 0 1 0", "0"), ("2 2 2 3 3 3", "18"), ("-1 -1 -1 1 1 1", "-3"), ("10 20 30 1 1 1", "60")]),
    make_row("M010", "Fraction Simplify Approx", "Structures", 8, "Medium", "Medium", "Read num den. Print integer quotient num/den.", False, [("10 2", "5"), ("15 3", "5"), ("7 2", "3"), ("100 10", "10"), ("42 7", "6")]),
    # Hard Mandatory (Lab Manual Q15)
    make_row("LM001", "Student Grades Struct Array", "Lab Manual Structures", 8, "Hard", "Hard", "Write a C program to enter info (name, reg no, marks in 6 subjects) of N students into an array of structures, find average & display grade based on average.\nAverage Grade mapping:\n80-100 Distinction\n60-79 First Class\n40-59 Second Class\n<40 Fail\nRead N. For each student read Name, RegNo, then 6 integer marks. Output exact line per student: '<Name> <RegNo> <Average> <Grade>' where Average is rounded integer.", True, [("2 Alice 101 80 80 80 80 80 80 Bob 102 50 50 50 50 50 50", "Alice 101 80 Distinction\nBob 102 50 Second Class"), ("1 Charlie 103 65 65 65 65 65 65", "Charlie 103 65 First Class"), ("1 David 104 30 30 30 30 30 30", "David 104 30 Fail"), ("2 Eve 105 90 90 90 90 90 90 Frank 106 70 70 70 70 70 70", "Eve 105 90 Distinction\nFrank 106 70 First Class"), ("1 Grace 107 45 45 45 45 45 45", "Grace 107 45 Second Class")]),
    # Hard Filler (5)
    make_row("H001", "Complex Multiply", "Structures", 8, "Hard", "Hard", "Read r1 i1 r2 i2. Compute product (r1*r2 - i1*i2) + i*(r1*i2 + r2*i1). Print real imag space separated.", False, [("1 2 3 4", "-5 10"), ("2 0 3 0", "6 0"), ("0 1 0 1", "-1 0"), ("2 3 4 5", "-7 22"), ("1 1 1 -1", "2 0")]),
    make_row("H002", "Time Difference Seconds", "Structures", 8, "Hard", "Hard", "Read h1 m1 s1 h2 m2 s2 (time 2 >= time 1). Compute difference in total seconds and print.", False, [("1 0 0 1 1 30", "90"), ("0 0 0 1 0 0", "3600"), ("10 15 20 10 15 50", "30"), ("5 0 0 6 30 0", "5400"), ("12 0 0 12 0 10", "10")]),
    make_row("H003", "Top Student Among N", "Structures", 8, "Hard", "Hard", "Read N. Read N pairs of (name, total_marks). Print name of student with highest marks.", False, [("3 Alice 80 Bob 95 Charlie 70", "Bob"), ("2 Dave 50 Eve 60", "Eve"), ("1 Frank 99", "Frank"), ("3 Grace 88 Heidi 88 Ivan 70", "Grace"), ("2 Judy 40 Mallory 90", "Mallory")]),
    make_row("H004", "Department Salary Sum", "Structures", 8, "Hard", "Hard", "Read N. Read N pairs of (dept_id, salary). Read target dept_id. Print sum of salaries for target dept.", False, [("4 101 5000 102 6000 101 7000 103 4000 101", "12000"), ("3 1 100 2 200 1 300 2", "200"), ("2 10 50 10 50 10", "100"), ("3 5 1000 6 2000 7 3000 8", "0"), ("1 42 999 42", "999")]),
    make_row("H005", "Vector Cross Product Z", "Structures", 8, "Hard", "Hard", "Read 2D vectors x1 y1 x2 y2. Compute z-component of cross product x1*y2 - y1*x2 and print.", False, [("1 0 0 1", "1"), ("2 3 4 6", "0"), ("5 2 1 3", "13"), ("1 1 2 2", "0"), ("3 4 -4 3", "25")])
]
write_csv("Module8_Structures_Levels.csv", m8_rows)

# MODULE 9: File Handling
m9_rows = [
    make_row("E001", "Char Count Sim", "File Handling", 9, "Easy", "Easy", "Simulate counting characters in file. Read a word and print character count.", False, [("hello", "5"), ("a", "1"), ("programming", "11"), ("code", "4"), ("openai", "6")]),
    make_row("E002", "Line Count Sim", "File Handling", 9, "Easy", "Easy", "Read integer N representing lines in file and print N.", False, [("5", "5"), ("10", "10"), ("1", "1"), ("100", "100"), ("42", "42")]),
    make_row("E003", "Digit Count Sim", "File Handling", 9, "Easy", "Easy", "Read word simulating file content. Print count of digit characters.", False, [("code123", "3"), ("hello", "0"), ("a1b2c", "2"), ("999", "3"), ("test0", "1")]),
    make_row("E004", "Vowel Count Sim", "File Handling", 9, "Easy", "Easy", "Read lowercase word simulating file content. Print count of vowels.", False, [("hello", "2"), ("sky", "0"), ("education", "5"), ("apple", "2"), ("code", "2")]),
    make_row("E005", "Uppercase Count Sim", "File Handling", 9, "Easy", "Easy", "Read word simulating file content. Print count of uppercase letters.", False, [("Hello", "1"), ("HELLO", "5"), ("hello", "0"), ("CodeLab", "2"), ("A", "1")]),
    make_row("E006", "Starts With Vowel Sim", "File Handling", 9, "Easy", "Easy", "Read lowercase word. Print Yes if file starts with vowel else No.", False, [("apple", "Yes"), ("banana", "No"), ("education", "Yes"), ("code", "No"), ("item", "Yes")]),
    make_row("E007", "Ends With Period Sim", "File Handling", 9, "Easy", "Easy", "Read string. Print Yes if ends with '.' else No.", False, [("end.", "Yes"), ("hello", "No"), ("a.", "Yes"), ("test.", "Yes"), ("word", "No")]),
    make_row("E008", "Has Number Sim", "File Handling", 9, "Easy", "Easy", "Read word. Print Yes if contains any digit else No.", False, [("file1", "Yes"), ("text", "No"), ("data2024", "Yes"), ("doc", "No"), ("0zero", "Yes")]),
    make_row("E009", "Consonant Count Sim", "File Handling", 9, "Easy", "Easy", "Read lowercase alphabetic word. Print count of consonants.", False, [("hello", "3"), ("education", "4"), ("sky", "3"), ("apple", "3"), ("code", "2")]),
    make_row("E010", "File Size Bytes Sim", "File Handling", 9, "Easy", "Easy", "Read string. Assume 1 byte per char. Print file size in bytes.", False, [("hello", "5"), ("a", "1"), ("programming", "11"), ("code", "4"), ("openai", "6")]),
    make_row("M001", "Copy Sim", "File Handling", 9, "Medium", "Medium", "Simulate file copy. Read word and print exact copy.", False, [("hello", "hello"), ("world", "world"), ("data", "data"), ("file.txt", "file.txt"), ("code", "code")]),
    make_row("M002", "Find Word Sim", "File Handling", 9, "Medium", "Medium", "Read two words space separated (content and query). Print Found if equal else Not Found.", False, [("hello hello", "Found"), ("hello world", "Not Found"), ("data data", "Found"), ("abc abd", "Not Found"), ("test test", "Found")]),
    make_row("M003", "Replace Char Sim", "File Handling", 9, "Medium", "Medium", "Read word. Replace all 'a' with '@' and print.", False, [("banana", "b@n@n@"), ("apple", "@pple"), ("hello", "hello"), ("data", "d@t@"), ("cat", "c@t")]),
    make_row("M004", "Reverse Line Sim", "File Handling", 9, "Medium", "Medium", "Read word representing line and print reversed.", False, [("hello", "olleh"), ("abc", "cba"), ("data", "atad"), ("code", "edoc"), ("file", "elif")]),
    make_row("M005", "Check Empty Sim", "File Handling", 9, "Medium", "Medium", "Read integer N representing file length. Print Empty if N == 0 else Not Empty.", False, [("0", "Empty"), ("5", "Not Empty"), ("10", "Not Empty"), ("1", "Not Empty"), ("0", "Empty")]),
    make_row("M006", "Count Specific Char Sim", "File Handling", 9, "Medium", "Medium", "Read word and query char space separated. Print frequency of query char.", False, [("hello l", "2"), ("banana a", "3"), ("code z", "0"), ("test t", "2"), ("data d", "1")]),
    make_row("M007", "Longest Word Sim", "File Handling", 9, "Medium", "Medium", "Read two words space separated. Print length of the longer word.", False, [("hello programming", "11"), ("cat apple", "5"), ("a ab", "2"), ("same same", "4"), ("code data", "4")]),
    make_row("M008", "Average Word Length Sim", "File Handling", 9, "Medium", "Medium", "Read two words space separated. Compute total length divided by 2 (integer average) and print.", False, [("hello world", "5"), ("a abc", "2"), ("code data", "4"), ("programming lab", "7"), ("test case", "4")]),
    make_row("M009", "Remove Vowels Sim", "File Handling", 9, "Medium", "Medium", "Read lowercase word. Remove all vowels and print remaining string.", False, [("hello", "hll"), ("apple", "ppl"), ("sky", "sky"), ("banana", "bnn"), ("education", "dctn")]),
    make_row("M010", "Count Words Sim", "File Handling", 9, "Medium", "Medium", "Read integer N representing word count in file and print N.", False, [("10", "10"), ("50", "50"), ("1", "1"), ("100", "100"), ("42", "42")]),
    # Hard Mandatory (Lab Manual Q8)
    make_row("LM001", "Copy File Contents", "Lab Manual File Handling", 9, "Hard", "Hard", "Write a C program to copy contents of one file to another file.\nSimulated via standard I/O: Read number of lines N. Then read N lines of text representing source file. Print exact copy of text representing destination file.", True, [("2\nHello World\nFile Copy Test", "Hello World\nFile Copy Test"), ("1\nSingle Line Data", "Single Line Data"), ("3\nLine 1\nLine 2\nLine 3", "Line 1\nLine 2\nLine 3"), ("1\nE-Lab Lab Manual", "E-Lab Lab Manual"), ("2\nC Programming\nFile Handling", "C Programming\nFile Handling")]),
    # Hard Filler (5)
    make_row("H001", "Merge Two Streams Sim", "File Handling", 9, "Hard", "Hard", "Read word1 word2 space separated. Print merged string word1word2.", False, [("hello world", "helloworld"), ("foo bar", "foobar"), ("file copy", "filecopy"), ("data base", "database"), ("open ai", "openai")]),
    make_row("H002", "Extract Numbers Sum Sim", "File Handling", 9, "Hard", "Hard", "Read two integers representing extracted numbers from file. Print their sum.", False, [("10 20", "30"), ("100 50", "150"), ("5 5", "10"), ("0 42", "42"), ("1000 2000", "3000")]),
    make_row("H003", "Encrypt Shift Sim", "File Handling", 9, "Hard", "Hard", "Read lowercase word. Shift each letter by +1 (z->a) and print encrypted text.", False, [("abc", "bcd"), ("hello", "ifmmp"), ("xyz", "yza"), ("code", "dpef"), ("zebra", "afcsb")]),
    make_row("H004", "Decrypt Shift Sim", "File Handling", 9, "Hard", "Hard", "Read lowercase word. Shift each letter by -1 (a->z) and print decrypted text.", False, [("bcd", "abc"), ("ifmmp", "hello"), ("yza", "xyz"), ("dpef", "code"), ("afcsb", "zebra")]),
    make_row("H005", "Line Numbering Sim", "File Handling", 9, "Hard", "Hard", "Read word representing line text. Print with line number prefix '1: <word>'.", False, [("hello", "1: hello"), ("data", "1: data"), ("code", "1: code"), ("test", "1: test"), ("file", "1: file")])
]
write_csv("Module9_File_Handling_Levels.csv", m9_rows)

# MODULE 10: Advanced Concepts
m10_rows = [
    make_row("E001", "Macro Square", "Advanced Concepts", 10, "Easy", "Easy", "Define macro SQ(x) ((x)*(x)). Read n and print SQ(n).", False, [("5", "25"), ("2", "4"), ("10", "100"), ("0", "0"), ("-3", "9")]),
    make_row("E002", "Macro Max Two", "Advanced Concepts", 10, "Easy", "Easy", "Define macro MAX(a,b). Read a b and print MAX(a,b).", False, [("1 2", "2"), ("5 3", "5"), ("-1 -5", "-1"), ("0 0", "0"), ("100 99", "100")]),
    make_row("E003", "Macro Cube", "Advanced Concepts", 10, "Easy", "Easy", "Define macro CUBE(x) ((x)*(x)*(x)). Read n and print CUBE(n).", False, [("2", "8"), ("3", "27"), ("0", "0"), ("-2", "-8"), ("5", "125")]),
    make_row("E004", "Recursion Countdown", "Advanced Concepts", 10, "Easy", "Easy", "Read n. Using recursion, print numbers n down to 1 space separated.", False, [("3", "3 2 1"), ("5", "5 4 3 2 1"), ("1", "1"), ("2", "2 1"), ("4", "4 3 2 1")]),
    make_row("E005", "Recursion Sum N", "Advanced Concepts", 10, "Easy", "Easy", "Read n. Using recursion, return sum 1 to n and print.", False, [("5", "15"), ("1", "1"), ("10", "55"), ("2", "3"), ("20", "210")]),
    make_row("E006", "Bitwise Parity Check", "Advanced Concepts", 10, "Easy", "Easy", "Read n. Print 1 if number of set bits is odd else 0.", False, [("1", "1"), ("2", "1"), ("3", "0"), ("7", "1"), ("15", "0")]),
    make_row("E007", "Macro Absolute", "Advanced Concepts", 10, "Easy", "Easy", "Define macro ABS(x). Read n and print ABS(n).", False, [("-5", "5"), ("5", "5"), ("0", "0"), ("-100", "100"), ("42", "42")]),
    make_row("E008", "Enum Day Type", "Advanced Concepts", 10, "Easy", "Easy", "Read day number (1-7). Print Weekend if 6 or 7 else Weekday.", False, [("1", "Weekday"), ("5", "Weekday"), ("6", "Weekend"), ("7", "Weekend"), ("3", "Weekday")]),
    make_row("E009", "Typedef Point Sum", "Advanced Concepts", 10, "Easy", "Easy", "Use typedef struct {int x; int y;} Point; Read x y and print x+y.", False, [("2 3", "5"), ("10 20", "30"), ("-5 5", "0"), ("0 0", "0"), ("100 200", "300")]),
    make_row("E010", "Function Pointer Call Sim", "Advanced Concepts", 10, "Easy", "Easy", "Read a b. Using a function pointer to an add function, compute and print sum.", False, [("1 2", "3"), ("10 20", "30"), ("-5 5", "0"), ("100 200", "300"), ("7 8", "15")]),
    make_row("M001", "Matrix 2x2 Trace", "Advanced Concepts", 10, "Medium", "Medium", "Read 4 integers of 2x2 matrix row-wise. Print trace (sum of diagonal).", False, [("1 2 3 4", "5"), ("0 0 0 0", "0"), ("5 6 7 8", "13"), ("1 0 0 1", "2"), ("10 20 30 40", "50")]),
    make_row("M002", "Matrix 2x2 Transpose", "Advanced Concepts", 10, "Medium", "Medium", "Read 4 integers of 2x2 matrix row-wise. Print transpose row-wise space separated.", False, [("1 2 3 4", "1 3 2 4"), ("0 0 0 0", "0 0 0 0"), ("5 6 7 8", "5 7 6 8"), ("1 0 0 1", "1 0 0 1"), ("10 20 30 40", "10 30 20 40")]),
    make_row("M003", "Recursive GCD", "Advanced Concepts", 10, "Medium", "Medium", "Write recursive GCD function. Read positive a b and print GCD.", False, [("12 18", "6"), ("7 5", "1"), ("100 10", "10"), ("81 27", "27"), ("14 21", "7")]),
    make_row("M004", "2D Array Row Sums", "Advanced Concepts", 10, "Medium", "Medium", "Read 2x2 matrix (4 integers). Print sum of row 0 and row 1 space separated.", False, [("1 2 3 4", "3 7"), ("10 10 20 20", "20 40"), ("0 0 0 0", "0 0"), ("5 5 1 1", "10 2"), ("2 3 4 5", "5 9")]),
    make_row("M005", "2D Array Col Sums", "Advanced Concepts", 10, "Medium", "Medium", "Read 2x2 matrix (4 integers). Print sum of col 0 and col 1 space separated.", False, [("1 2 3 4", "4 6"), ("10 10 20 20", "30 30"), ("0 0 0 0", "0 0"), ("5 5 1 1", "6 6"), ("2 3 4 5", "6 8")]),
    make_row("M006", "Matrix 2x2 Determinant", "Advanced Concepts", 10, "Medium", "Medium", "Read 2x2 matrix a b c d. Print determinant a*d - b*c.", False, [("1 2 3 4", "-2"), ("2 0 0 2", "4"), ("1 0 0 1", "1"), ("5 6 7 8", "-2"), ("10 2 3 1", "4")]),
    make_row("M007", "Dynamic Array Sum Sim", "Advanced Concepts", 10, "Medium", "Medium", "Read n and n integers. Simulate dynamic array allocation, compute sum and print.", False, [("3 1 2 3", "6"), ("1 5", "5"), ("4 10 20 30 40", "100"), ("2 -1 1", "0"), ("3 5 5 5", "15")]),
    make_row("M008", "Recursive Power", "Advanced Concepts", 10, "Medium", "Medium", "Write recursive power function. Read base exp (>=0) and print result.", False, [("2 3", "8"), ("5 0", "1"), ("3 4", "81"), ("10 2", "100"), ("7 2", "49")]),
    make_row("M009", "Bit Field Mask 4", "Advanced Concepts", 10, "Medium", "Medium", "Read integer n. Mask lower 4 bits (n & 15) and print.", False, [("255", "15"), ("16", "0"), ("18", "2"), ("7", "7"), ("31", "15")]),
    make_row("M010", "Union Size Sim", "Advanced Concepts", 10, "Medium", "Medium", "Assume union with int (4 bytes) and double (8 bytes). Print size of union (8).", False, [("0", "8"), ("1", "8"), ("42", "8"), ("100", "8"), ("999", "8")]),
    # Hard Mandatory (Lab Manual Q11)
    make_row("LM001", "Matrix Transpose and Trace", "Lab Manual Advanced Concepts", 10, "Hard", "Hard", "Write a C program to transpose a matrix of order M x N and find the trace of the resultant matrix.\nRead M N then M*N integers. Print transposed matrix row by row (space separated elements). Then on a new line print 'Trace: X' (if square matrix, sum of diagonal of resultant matrix; if not square, print 'Trace: Not Square').", True, [("2 2 1 2 3 4", "1 3\n2 4\nTrace: 5"), ("2 3 1 2 3 4 5 6", "1 4\n2 5\n3 6\nTrace: Not Square"), ("3 3 1 0 0 0 1 0 0 0 1", "1 0 0\n0 1 0\n0 0 1\nTrace: 3"), ("1 1 42", "42\nTrace: 42"), ("2 2 5 6 7 8", "5 7\n6 8\nTrace: 13")]),
    # Hard Filler (5)
    make_row("H001", "Matrix Product 2x2 Manual", "Advanced Concepts", 10, "Hard", "Hard", "Read two 2x2 matrices (4 integers each). Print resultant 2x2 matrix row by row space separated.", False, [("1 0 0 1 1 2 3 4", "1 2\n3 4"), ("2 0 0 2 1 1 1 1", "2 2\n2 2"), ("1 2 3 4 0 0 0 0", "0 0\n0 0"), ("1 1 1 1 1 1 1 1", "2 2\n2 2"), ("2 1 1 2 1 0 0 1", "2 1\n1 2")]),
    make_row("H002", "Magic Square Check 3x3", "Advanced Concepts", 10, "Hard", "Hard", "Read 3x3 matrix (9 integers). Print Yes if all row, col, and diagonal sums are equal else No.", False, [("8 1 6 3 5 7 4 9 2", "Yes"), ("1 2 3 4 5 6 7 8 9", "No"), ("5 5 5 5 5 5 5 5 5", "Yes"), ("2 7 6 9 5 1 4 3 8", "Yes"), ("0 0 0 0 0 0 0 0 0", "Yes")]),
    make_row("H003", "Recursive Tower of Hanoi Moves", "Advanced Concepts", 10, "Hard", "Hard", "Read n disks. Compute total moves 2^n - 1 using recursion or formula and print.", False, [("1", "1"), ("2", "3"), ("3", "7"), ("4", "15"), ("5", "31")]),
    make_row("H004", "Linked List Traversal Sum Sim", "Advanced Concepts", 10, "Hard", "Hard", "Simulate linked list node sum. Read n and n node values. Print sum.", False, [("3 10 20 30", "60"), ("1 42", "42"), ("4 1 2 3 4", "10"), ("2 5 5", "10"), ("5 1 1 1 1 1", "5")]),
    make_row("H005", "Spiral Matrix Print Sim", "Advanced Concepts", 10, "Hard", "Hard", "Read 2x2 matrix (4 integers row-wise). Print spiral order (top row left-right, bottom row right-left: a b d c).", False, [("1 2 3 4", "1 2 4 3"), ("10 20 30 40", "10 20 40 30"), ("5 6 7 8", "5 6 8 7"), ("0 0 0 0", "0 0 0 0"), ("9 8 7 6", "9 8 6 7")])
]
write_csv("Module10_Advanced_Concepts_Levels.csv", m10_rows)

print("Modules 6 to 10 generated successfully.")
