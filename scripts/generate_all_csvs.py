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

# MODULE 1: Basics I/O
m1_rows = [
    make_row("E001", "Print Integer", "Basics I/O", 1, "Easy", "Easy", "Read an integer and print it.\n\nRead input from stdin and print only the exact requested output.", False, [("5", "5"), ("-10", "-10"), ("0", "0"), ("100", "100"), ("42", "42")]),
    make_row("E002", "Sum Two Integers", "Basics I/O", 1, "Easy", "Easy", "Read two integers and print their sum.", False, [("1 2", "3"), ("-5 5", "0"), ("10 20", "30"), ("-3 -7", "-10"), ("100 200", "300")]),
    make_row("E003", "Product Two Integers", "Basics I/O", 1, "Easy", "Easy", "Read two integers and print their product.", False, [("2 3", "6"), ("-4 5", "-20"), ("0 10", "0"), ("7 8", "56"), ("-3 -3", "9")]),
    make_row("E004", "Rectangle Area", "Basics I/O", 1, "Easy", "Easy", "Read length and breadth and print rectangle area.", False, [("2 3", "6"), ("5 5", "25"), ("10 1", "10"), ("7 8", "56"), ("12 4", "48")]),
    make_row("E005", "ASCII Value", "Basics I/O", 1, "Easy", "Easy", "Read one character and print its ASCII value.", False, [("A", "65"), ("a", "97"), ("0", "48"), ("Z", "90"), ("z", "122")]),
    make_row("E006", "Subtract Two Integers", "Basics I/O", 1, "Easy", "Easy", "Read two integers a and b and print a - b.", False, [("5 3", "2"), ("10 20", "-10"), ("0 0", "0"), ("-5 -2", "-3"), ("100 50", "50")]),
    make_row("E007", "Divide Two Integers", "Basics I/O", 1, "Easy", "Easy", "Read two integers a and b and print integer quotient a / b.", False, [("10 2", "5"), ("15 3", "5"), ("7 2", "3"), ("-10 2", "-5"), ("100 10", "10")]),
    make_row("E008", "Remainder Two Integers", "Basics I/O", 1, "Easy", "Easy", "Read two integers a and b and print remainder a % b.", False, [("10 3", "1"), ("15 4", "3"), ("20 5", "0"), ("7 2", "1"), ("100 30", "10")]),
    make_row("E009", "Perimeter of Rectangle", "Basics I/O", 1, "Easy", "Easy", "Read length and breadth and print perimeter 2*(l+b).", False, [("2 3", "10"), ("5 5", "20"), ("10 1", "22"), ("7 8", "30"), ("12 4", "32")]),
    make_row("E010", "Area of Square", "Basics I/O", 1, "Easy", "Easy", "Read side s and print area s*s.", False, [("2", "4"), ("5", "25"), ("10", "100"), ("7", "49"), ("12", "144")]),
    make_row("M001", "Celsius to Fahrenheit", "Basics I/O", 1, "Medium", "Medium", "Read Celsius c and print Fahrenheit using integer formula c*9/5+32.", False, [("0", "32"), ("100", "212"), ("37", "98"), ("-40", "-40"), ("25", "77")]),
    make_row("M002", "Simple Interest", "Basics I/O", 1, "Medium", "Medium", "Read p r t and print simple interest p*r*t/100.", False, [("1000 5 2", "100"), ("5000 10 1", "500"), ("2500 4 3", "300"), ("100 1 1", "1"), ("12000 8 5", "4800")]),
    make_row("M003", "Square and Cube", "Basics I/O", 1, "Medium", "Medium", "Read n and print square and cube space separated.", False, [("2", "4 8"), ("3", "9 27"), ("4", "16 64"), ("5", "25 125"), ("10", "100 1000")]),
    make_row("M004", "Last Digit", "Basics I/O", 1, "Medium", "Medium", "Read non-negative integer and print last digit.", False, [("123", "3"), ("0", "0"), ("7", "7"), ("4560", "0"), ("999", "9")]),
    make_row("M005", "Swap Two Numbers", "Basics I/O", 1, "Medium", "Medium", "Read a b and print b a.", False, [("1 2", "2 1"), ("5 3", "3 5"), ("-1 9", "9 -1"), ("0 0", "0 0"), ("100 99", "99 100")]),
    make_row("M006", "Fahrenheit to Celsius", "Basics I/O", 1, "Medium", "Medium", "Read Fahrenheit f and print Celsius using integer formula (f-32)*5/9.", False, [("32", "0"), ("212", "100"), ("98", "36"), ("-40", "-40"), ("77", "25")]),
    make_row("M007", "Average of Four", "Basics I/O", 1, "Medium", "Medium", "Read four integers and print integer average.", False, [("1 2 3 4", "2"), ("10 20 30 40", "25"), ("5 5 5 5", "5"), ("0 0 0 4", "1"), ("100 200 300 400", "250")]),
    make_row("M008", "Double and Triple", "Basics I/O", 1, "Medium", "Medium", "Read n and print 2*n and 3*n space separated.", False, [("2", "4 6"), ("5", "10 15"), ("10", "20 30"), ("-3", "-6 -9"), ("0", "0 0")]),
    make_row("M009", "Seconds to Minutes", "Basics I/O", 1, "Medium", "Medium", "Read total seconds and print integer minutes.", False, [("60", "1"), ("130", "2"), ("3600", "60"), ("45", "0"), ("600", "10")]),
    make_row("M010", "Perimeter of Circle Approx", "Basics I/O", 1, "Medium", "Medium", "Read integer radius r and print integer perimeter using 2*22*r/7.", False, [("7", "44"), ("14", "88"), ("21", "132"), ("1", "6"), ("35", "220")]),
    make_row("LM001", "Quadratic Roots", "Lab Manual Basics", 1, "Hard", "Hard", "Write a C program to find the roots of a quadratic equation ax2+bx+c=0.\nRead coefficients a b c. Print 'Equal Real', 'Distinct Real', or 'Imaginary' based on discriminant b*b - 4*a*c.", True, [("1 -2 1", "Equal Real"), ("1 -5 6", "Distinct Real"), ("1 2 5", "Imaginary"), ("2 4 2", "Equal Real"), ("1 0 -4", "Distinct Real")]),
    make_row("LM002", "Digit Sum and Occurrence", "Lab Manual Basics", 1, "Hard", "Hard", "Write a C program to find the sum of all the digits and occurrence of a digit in the number.\nRead n and digit d. Print sum of digits of n, followed by space, followed by occurrence count of d in n.", True, [("1234 2", "10 1"), ("555 5", "15 3"), ("1010 1", "2 2"), ("999 3", "27 0"), ("8080 8", "16 2")]),
    make_row("H001", "Sum of First N Natural Numbers", "Basics I/O", 1, "Hard", "Hard", "Read n and print sum using n*(n+1)/2.", False, [("10", "55"), ("100", "5050"), ("1", "1"), ("5", "15"), ("50", "1275")]),
    make_row("H002", "Distance Squared", "Basics I/O", 1, "Hard", "Hard", "Read x1 y1 x2 y2 and print distance squared (x2-x1)^2 + (y2-y1)^2.", False, [("0 0 3 4", "25"), ("1 1 4 5", "25"), ("0 0 0 0", "0"), ("-1 -1 1 1", "8"), ("10 10 20 20", "200")]),
    make_row("H003", "Total and Percentage", "Basics I/O", 1, "Hard", "Hard", "Read marks of 5 subjects (out of 100 each). Print total and integer percentage space separated.", False, [("80 80 80 80 80", "400 80"), ("90 90 90 90 90", "450 90"), ("50 60 70 80 90", "350 70"), ("100 100 100 100 100", "500 100"), ("40 40 40 40 40", "200 40")]),
    make_row("H004", "Arithmetic Progression Term", "Basics I/O", 1, "Hard", "Hard", "Read a d n and print nth term of AP: a + (n-1)*d.", False, [("2 3 5", "14"), ("10 5 3", "20"), ("1 1 100", "100"), ("5 -2 4", "-1"), ("0 10 10", "90")]),
    make_row("H005", "Cube Surface Area", "Basics I/O", 1, "Hard", "Hard", "Read side s and print total surface area of cube 6*s*s.", False, [("2", "24"), ("3", "54"), ("5", "150"), ("10", "600"), ("1", "6")])
]
write_csv("Module1_Basics_IO_Levels.csv", m1_rows)

# MODULE 2: Operators & Expressions
m2_rows = [
    make_row("E001", "Quotient Remainder", "Operators", 2, "Easy", "Easy", "Read a b and print quotient and remainder space separated.", False, [("10 3", "3 1"), ("20 5", "4 0"), ("7 2", "3 1"), ("100 9", "11 1"), ("45 6", "7 3")]),
    make_row("E002", "Even Check", "Operators", 2, "Easy", "Easy", "Read n and print 1 if even else 0.", False, [("0", "1"), ("1", "0"), ("2", "1"), ("3", "0"), ("10", "1")]),
    make_row("E003", "Increment", "Operators", 2, "Easy", "Easy", "Read n and print n+1.", False, [("0", "1"), ("1", "2"), ("-1", "0"), ("99", "100"), ("1000", "1001")]),
    make_row("E004", "Expression A Plus B Times C", "Operators", 2, "Easy", "Easy", "Read a b c and print a+b*c.", False, [("1 2 3", "7"), ("10 5 2", "20"), ("0 7 8", "56"), ("-1 3 4", "11"), ("9 9 9", "90")]),
    make_row("E005", "Average Three", "Operators", 2, "Easy", "Easy", "Read three integers and print integer average.", False, [("1 2 3", "2"), ("10 20 30", "20"), ("5 5 5", "5"), ("0 0 1", "0"), ("-3 3 6", "2")]),
    make_row("E006", "Decrement", "Operators", 2, "Easy", "Easy", "Read n and print n-1.", False, [("1", "0"), ("0", "-1"), ("100", "99"), ("-5", "-6"), ("42", "41")]),
    make_row("E007", "Multiply by Two Shift", "Operators", 2, "Easy", "Easy", "Read n and print n << 1.", False, [("1", "2"), ("5", "10"), ("10", "20"), ("0", "0"), ("15", "30")]),
    make_row("E008", "Divide by Two Shift", "Operators", 2, "Easy", "Easy", "Read non-negative n and print n >> 1.", False, [("2", "1"), ("10", "5"), ("11", "5"), ("0", "0"), ("100", "50")]),
    make_row("E009", "Modulo Ten", "Operators", 2, "Easy", "Easy", "Read positive integer n and print n % 10.", False, [("123", "3"), ("45", "5"), ("100", "0"), ("7", "7"), ("999", "9")]),
    make_row("E010", "Square Expression", "Operators", 2, "Easy", "Easy", "Read a b and print (a+b)*(a+b).", False, [("1 2", "9"), ("3 4", "49"), ("0 5", "25"), ("-2 2", "0"), ("10 10", "400")]),
    make_row("M001", "Bitwise AND", "Operators", 2, "Medium", "Medium", "Read a b and print a & b.", False, [("5 3", "1"), ("12 10", "8"), ("7 1", "1"), ("0 9", "0"), ("15 8", "8")]),
    make_row("M002", "Bitwise OR", "Operators", 2, "Medium", "Medium", "Read a b and print a | b.", False, [("5 3", "7"), ("12 10", "14"), ("7 1", "7"), ("0 9", "9"), ("15 8", "15")]),
    make_row("M003", "Left Shift", "Operators", 2, "Medium", "Medium", "Read n k and print n shifted left by k.", False, [("1 1", "2"), ("2 2", "8"), ("5 1", "10"), ("7 3", "56"), ("10 0", "10")]),
    make_row("M004", "Absolute Difference", "Operators", 2, "Medium", "Medium", "Read a b and print absolute difference.", False, [("1 5", "4"), ("5 1", "4"), ("-2 3", "5"), ("10 10", "0"), ("0 9", "9")]),
    make_row("M005", "Precedence Difference", "Operators", 2, "Medium", "Medium", "Read a b c and print (a+b)*c.", False, [("1 2 3", "9"), ("10 5 2", "30"), ("0 7 8", "56"), ("-1 3 4", "8"), ("9 9 9", "162")]),
    make_row("M006", "Right Shift", "Operators", 2, "Medium", "Medium", "Read n k and print n shifted right by k.", False, [("8 1", "4"), ("16 2", "4"), ("15 1", "7"), ("100 3", "12"), ("7 0", "7")]),
    make_row("M007", "Bitwise XOR", "Operators", 2, "Medium", "Medium", "Read a b and print a ^ b.", False, [("5 3", "6"), ("12 10", "6"), ("7 7", "0"), ("15 0", "15"), ("255 1", "254")]),
    make_row("M008", "Is Multiple of 5", "Operators", 2, "Medium", "Medium", "Read n and print 1 if multiple of 5 else 0.", False, [("10", "1"), ("15", "1"), ("12", "0"), ("0", "1"), ("-25", "1")]),
    make_row("M009", "Opposite Signs Check", "Operators", 2, "Medium", "Medium", "Read non-zero a and b. Print 1 if opposite signs else 0.", False, [("5 -3", "1"), ("-2 4", "1"), ("5 10", "0"), ("-3 -7", "0"), ("100 -1", "1")]),
    make_row("M010", "Sum of Squares", "Operators", 2, "Medium", "Medium", "Read a b and print a*a + b*b.", False, [("3 4", "25"), ("1 2", "5"), ("0 5", "25"), ("-3 -4", "25"), ("10 10", "200")]),
    make_row("LM001", "GCD and LCM Euclid", "Lab Manual Operators", 2, "Hard", "Hard", "Write a C program to find the GCD and LCM of given two numbers using Euclid's method.\nRead two positive integers. Print GCD followed by space followed by LCM.", True, [("12 18", "6 36"), ("7 5", "1 35"), ("100 10", "10 100"), ("81 27", "27 81"), ("14 21", "7 42")]),
    make_row("H001", "Quadratic Discriminant", "Operators", 2, "Hard", "Hard", "Read a b c and print discriminant b*b-4*a*c.", False, [("1 -2 1", "0"), ("1 -5 6", "1"), ("1 2 5", "-16"), ("2 4 2", "0"), ("1 0 -4", "16")]),
    make_row("H002", "Mask Lower N Bits", "Operators", 2, "Hard", "Hard", "Read n and print (1<<n)-1.", False, [("0", "0"), ("1", "1"), ("2", "3"), ("3", "7"), ("4", "15")]),
    make_row("H003", "Toggle Bit", "Operators", 2, "Hard", "Hard", "Read n k and print n with kth bit toggled (0-indexed).", False, [("5 1", "7"), ("5 0", "4"), ("8 3", "0"), ("10 1", "8"), ("15 2", "11")]),
    make_row("H004", "Count Set Bits", "Operators", 2, "Hard", "Hard", "Read non-negative integer n and print count of set bits (1s in binary).", False, [("5", "2"), ("7", "3"), ("0", "0"), ("15", "4"), ("1024", "1")]),
    make_row("H005", "Power of Two Check", "Operators", 2, "Hard", "Hard", "Read positive integer n and print 1 if power of 2 else 0.", False, [("1", "1"), ("2", "1"), ("3", "0"), ("4", "1"), ("18", "0")])
]
write_csv("Module2_Operators_Expressions_Levels.csv", m2_rows)

# MODULE 3: Conditionals & Loops
m3_rows = [
    make_row("E001", "Maximum Two", "Conditionals", 3, "Easy", "Easy", "Read two integers and print maximum.", False, [("1 2", "2"), ("5 3", "5"), ("-1 -5", "-1"), ("0 0", "0"), ("100 99", "100")]),
    make_row("E002", "Sign Number", "Conditionals", 3, "Easy", "Easy", "Read n and print Positive Negative or Zero.", False, [("0", "Zero"), ("1", "Positive"), ("-1", "Negative"), ("25", "Positive"), ("-30", "Negative")]),
    make_row("E003", "Sum N", "Loops", 3, "Easy", "Easy", "Read n and print sum 1 to n using loop.", False, [("1", "1"), ("2", "3"), ("5", "15"), ("10", "55"), ("20", "210")]),
    make_row("E004", "Count Digits", "Loops", 3, "Easy", "Easy", "Read non-negative n and print digit count.", False, [("0", "1"), ("1", "1"), ("10", "2"), ("99", "2"), ("100", "3")]),
    make_row("E005", "Multiplication Ten", "Loops", 3, "Easy", "Easy", "Read n and print n*10.", False, [("1", "10"), ("2", "20"), ("5", "50"), ("7", "70"), ("10", "100")]),
    make_row("E006", "Minimum Two", "Conditionals", 3, "Easy", "Easy", "Read two integers and print minimum.", False, [("1 2", "1"), ("5 3", "3"), ("-1 -5", "-5"), ("0 0", "0"), ("100 99", "99")]),
    make_row("E007", "Voting Eligibility", "Conditionals", 3, "Easy", "Easy", "Read age and print Eligible if >= 18 else Not Eligible.", False, [("18", "Eligible"), ("20", "Eligible"), ("17", "Not Eligible"), ("5", "Not Eligible"), ("65", "Eligible")]),
    make_row("E008", "Vowel or Consonant", "Conditionals", 3, "Easy", "Easy", "Read lowercase char c and print Vowel if a,e,i,o,u else Consonant.", False, [("a", "Vowel"), ("b", "Consonant"), ("e", "Vowel"), ("z", "Consonant"), ("u", "Vowel")]),
    make_row("E009", "Pass or Fail", "Conditionals", 3, "Easy", "Easy", "Read marks out of 100 and print Pass if >= 40 else Fail.", False, [("40", "Pass"), ("39", "Fail"), ("85", "Pass"), ("0", "Fail"), ("100", "Pass")]),
    make_row("E010", "Print N to 1", "Loops", 3, "Easy", "Easy", "Read n and print numbers from n down to 1 space separated.", False, [("3", "3 2 1"), ("5", "5 4 3 2 1"), ("1", "1"), ("2", "2 1"), ("4", "4 3 2 1")]),
    make_row("M001", "Leap Year", "Conditionals", 3, "Medium", "Medium", "Read year and print Leap or Not Leap.", False, [("2000", "Leap"), ("1900", "Not Leap"), ("2024", "Leap"), ("2023", "Not Leap"), ("2100", "Not Leap")]),
    make_row("M002", "Factorial", "Loops", 3, "Medium", "Medium", "Read n (0 to 12) and print factorial.", False, [("0", "1"), ("1", "1"), ("2", "2"), ("3", "6"), ("5", "120")]),
    make_row("M003", "Reverse Number", "Loops", 3, "Medium", "Medium", "Read non-negative integer and print reverse.", False, [("0", "0"), ("12", "21"), ("120", "21"), ("1234", "4321"), ("900", "9")]),
    make_row("M004", "Prime Check", "Loops", 3, "Medium", "Medium", "Read positive integer n and print Prime or Not Prime.", False, [("1", "Not Prime"), ("2", "Prime"), ("3", "Prime"), ("4", "Not Prime"), ("11", "Prime")]),
    make_row("M005", "Fibonacci", "Loops", 3, "Medium", "Medium", "Read n and print nth Fibonacci (0th=0, 1st=1).", False, [("0", "0"), ("1", "1"), ("2", "1"), ("3", "2"), ("6", "8")]),
    make_row("M006", "Sum of Even up to N", "Loops", 3, "Medium", "Medium", "Read n and print sum of all even integers from 1 to n.", False, [("1", "0"), ("2", "2"), ("5", "6"), ("10", "30"), ("6", "12")]),
    make_row("M007", "Palindrome Number Check", "Loops", 3, "Medium", "Medium", "Read non-negative n and print Palindrome or Not Palindrome.", False, [("121", "Palindrome"), ("123", "Not Palindrome"), ("0", "Palindrome"), ("7", "Palindrome"), ("1221", "Palindrome")]),
    make_row("M008", "Factors Count", "Loops", 3, "Medium", "Medium", "Read positive integer n and print number of divisors of n.", False, [("1", "1"), ("6", "4"), ("7", "2"), ("10", "4"), ("12", "6")]),
    make_row("M009", "Count Even Digits", "Loops", 3, "Medium", "Medium", "Read non-negative n and print count of even digits.", False, [("1234", "2"), ("2468", "4"), ("1357", "0"), ("0", "1"), ("802", "3")]),
    make_row("M010", "Sum of Odd Digits", "Loops", 3, "Medium", "Medium", "Read non-negative n and print sum of odd digits.", False, [("1234", "4"), ("2468", "0"), ("1357", "16"), ("0", "0"), ("901", "10")]),
    make_row("LM001", "Prime Range Print", "Lab Manual Loops", 3, "Hard", "Hard", "Write a C program to print the prime numbers in a given range.\nRead start and end (inclusive). Print all prime numbers in range space separated. If none, print empty line or nothing.", True, [("10 20", "11 13 17 19"), ("1 10", "2 3 5 7"), ("14 16", ""), ("20 30", "23 29"), ("2 5", "2 3 5")]),
    make_row("H001", "Armstrong Check", "Loops", 3, "Hard", "Hard", "Read n and print Armstrong or Not Armstrong (sum of cubes of digits == n for 3-digit numbers).", False, [("153", "Armstrong"), ("370", "Armstrong"), ("123", "Not Armstrong"), ("407", "Armstrong"), ("10", "Not Armstrong")]),
    make_row("H002", "Perfect Number", "Loops", 3, "Hard", "Hard", "Read n and print Perfect or Not Perfect (sum of proper divisors == n).", False, [("6", "Perfect"), ("28", "Perfect"), ("12", "Not Perfect"), ("496", "Perfect"), ("100", "Not Perfect")]),
    make_row("H003", "Pattern Count", "Loops", 3, "Hard", "Hard", "Read n and print number of stars in n-row triangle n*(n+1)/2.", False, [("1", "1"), ("2", "3"), ("3", "6"), ("4", "10"), ("5", "15")]),
    make_row("H004", "Collatz Steps", "Loops", 3, "Hard", "Hard", "Read n and print steps to reach 1 by Collatz rule (if even n/2 else 3*n+1).", False, [("1", "0"), ("2", "1"), ("3", "7"), ("4", "2"), ("5", "5")]),
    make_row("H005", "Strong Number Check", "Loops", 3, "Hard", "Hard", "Read n and print Strong or Not Strong (sum of factorials of digits == n).", False, [("145", "Strong"), ("1", "Strong"), ("2", "Strong"), ("123", "Not Strong"), ("40585", "Strong")])
]
write_csv("Module3_Conditionals_Loops_Levels.csv", m3_rows)

# MODULE 4: Arrays
m4_rows = [
    make_row("E001", "Array Sum", "Arrays", 4, "Easy", "Easy", "Read n and n integers and print sum.", False, [("1 1", "1"), ("3 1 2 3", "6"), ("3 5 5 5", "15"), ("3 -1 2 -3", "-2"), ("4 10 20 30 40", "100")]),
    make_row("E002", "Array Maximum", "Arrays", 4, "Easy", "Easy", "Read n and n integers and print maximum.", False, [("1 1", "1"), ("3 1 2 3", "3"), ("3 5 5 5", "5"), ("3 -1 2 -3", "2"), ("4 10 20 30 40", "40")]),
    make_row("E003", "Count Even", "Arrays", 4, "Easy", "Easy", "Read n and n integers and print count of even elements.", False, [("1 1", "0"), ("3 1 2 3", "1"), ("3 5 5 5", "0"), ("3 -1 2 -3", "1"), ("4 10 20 30 40", "4")]),
    make_row("E004", "Positive Count", "Arrays", 4, "Easy", "Easy", "Read n and n integers and print count of positive numbers.", False, [("1 1", "1"), ("3 1 2 3", "3"), ("3 5 5 5", "3"), ("3 -1 2 -3", "1"), ("4 10 20 30 40", "4")]),
    make_row("E005", "Array Average", "Arrays", 4, "Easy", "Easy", "Read n and n integers and print integer average.", False, [("1 1", "1"), ("3 1 2 3", "2"), ("3 5 5 5", "5"), ("3 -1 2 -3", "-1"), ("4 10 20 30 40", "25")]),
    make_row("E006", "Array Minimum", "Arrays", 4, "Easy", "Easy", "Read n and n integers and print minimum.", False, [("1 1", "1"), ("3 1 2 3", "1"), ("3 5 5 5", "5"), ("3 -1 2 -3", "-3"), ("4 10 20 30 40", "10")]),
    make_row("E007", "Count Odd", "Arrays", 4, "Easy", "Easy", "Read n and n integers and print count of odd elements.", False, [("1 1", "1"), ("3 1 2 3", "2"), ("3 5 5 5", "3"), ("3 -1 2 -3", "2"), ("4 10 20 30 40", "0")]),
    make_row("E008", "Negative Count", "Arrays", 4, "Easy", "Easy", "Read n and n integers and print count of strictly negative numbers.", False, [("1 1", "0"), ("3 1 2 -3", "1"), ("3 -5 -5 -5", "3"), ("3 -1 2 -3", "2"), ("4 10 0 30 -40", "1")]),
    make_row("E009", "First Element", "Arrays", 4, "Easy", "Easy", "Read n and n integers and print the first element.", False, [("1 42", "42"), ("3 1 2 3", "1"), ("3 5 5 5", "5"), ("3 -1 2 -3", "-1"), ("4 10 20 30 40", "10")]),
    make_row("E010", "Last Element", "Arrays", 4, "Easy", "Easy", "Read n and n integers and print the last element.", False, [("1 42", "42"), ("3 1 2 3", "3"), ("3 5 5 5", "5"), ("3 -1 2 -3", "-3"), ("4 10 20 30 40", "40")]),
    make_row("M001", "Linear Search", "Arrays", 4, "Medium", "Medium", "Read n, n integers, key. Print Found or Not Found.", False, [("3 1 2 3 2", "Found"), ("3 1 2 3 5", "Not Found"), ("1 9 9", "Found"), ("3 4 5 6 4", "Found"), ("3 4 5 6 7", "Not Found")]),
    make_row("M002", "Array Reverse", "Arrays", 4, "Medium", "Medium", "Read n and n integers and print reverse space separated.", False, [("1 1", "1"), ("3 1 2 3", "3 2 1"), ("3 5 5 5", "5 5 5"), ("3 -1 2 -3", "-3 2 -1"), ("4 10 20 30 40", "40 30 20 10")]),
    make_row("M003", "Second Largest", "Arrays", 4, "Medium", "Medium", "Read n and n distinct integers and print second largest.", False, [("2 1 2", "1"), ("3 1 2 3", "2"), ("3 5 4 3", "4"), ("4 10 20 30 40", "30"), ("3 -1 2 -3", "-1")]),
    make_row("M004", "Frequency Key", "Arrays", 4, "Medium", "Medium", "Read n, n integers, key. Print frequency of key.", False, [("3 1 2 1 1", "2"), ("3 1 2 3 4", "0"), ("3 5 5 5 5", "3"), ("3 0 0 1 0", "2"), ("3 -1 2 -1 -1", "2")]),
    make_row("M005", "Adjacent Pair Sum", "Arrays", 4, "Medium", "Medium", "Read n and n integers and print maximum adjacent pair sum.", False, [("2 1 2", "3"), ("3 1 2 3", "5"), ("3 5 4 3", "9"), ("4 10 20 30 40", "70"), ("3 -1 2 -3", "1")]),
    make_row("M006", "Check Sorted Ascending", "Arrays", 4, "Medium", "Medium", "Read n and n integers. Print Sorted if non-decreasing else Not Sorted.", False, [("3 1 2 3", "Sorted"), ("3 3 2 1", "Not Sorted"), ("1 5", "Sorted"), ("4 1 1 2 2", "Sorted"), ("3 1 3 2", "Not Sorted")]),
    make_row("M007", "Sum of Even Indexed", "Arrays", 4, "Medium", "Medium", "Read n and n integers. Print sum of elements at 0-based even indices.", False, [("3 10 20 30", "40"), ("4 1 2 3 4", "4"), ("1 5", "5"), ("2 10 20", "10"), ("5 1 1 1 1 1", "3")]),
    make_row("M008", "Replace Negatives Zero", "Arrays", 4, "Medium", "Medium", "Read n and n integers. Print array replacing negative values with 0 space separated.", False, [("3 1 -2 3", "1 0 3"), ("2 -5 -1", "0 0"), ("3 1 2 3", "1 2 3"), ("1 -10", "0"), ("4 -1 2 -3 4", "0 2 0 4")]),
    make_row("M009", "Count Greater Average", "Arrays", 4, "Medium", "Medium", "Read n and n integers. Print count of elements strictly greater than exact average.", False, [("3 1 2 3", "1"), ("4 10 10 10 10", "0"), ("3 1 10 1", "1"), ("2 0 10", "1"), ("5 1 2 3 4 5", "2")]),
    make_row("M010", "Copy Array", "Arrays", 4, "Medium", "Medium", "Read n and n integers. Copy into second array and print second array space separated.", False, [("3 1 2 3", "1 2 3"), ("1 42", "42"), ("2 -1 -2", "-1 -2"), ("4 0 0 0 0", "0 0 0 0"), ("3 9 8 7", "9 8 7")]),
    # Hard Mandatory (Lab Manual Q6, Q9, Q10)
    make_row("LM001", "Mean Variance StdDev", "Lab Manual Arrays", 4, "Hard", "Hard", "Write a C program to input N real numbers in 1-D array. Compute mean, variance and Standard Deviation.\n[Mean= sum/N, Variance = Σ (Xi-mean)^2 /N, STD Deviation= √variance.]\nRead integer N then N float numbers. Print Mean, Variance, and Std Dev rounded to 2 decimal places space separated (e.g. '2.00 0.67 0.82').", True, [("3 1 2 3", "2.00 0.67 0.82"), ("4 2 4 4 4", "3.50 0.75 0.87"), ("1 5.0", "5.00 0.00 0.00"), ("2 10 20", "15.00 25.00 5.00"), ("5 1 1 1 1 1", "1.00 0.00 0.00")]),
    make_row("LM002", "Binary Search Sorted", "Lab Manual Arrays", 4, "Hard", "Hard", "Write a C program to perform a binary search for a given key integer in a single dimensional array of numbers in ascending order and report success or failure in the form of a suitable message.\nRead N, N sorted integers, then Key. Print 'Success: Found at index X' (0-based) or 'Failure: Key not found'.", True, [("5 10 20 30 40 50 30", "Success: Found at index 2"), ("5 10 20 30 40 50 25", "Failure: Key not found"), ("1 5 5", "Success: Found at index 0"), ("3 1 2 3 1", "Success: Found at index 0"), ("3 1 2 3 4", "Failure: Key not found")]),
    make_row("LM003", "Selection Sort Display", "Lab Manual Arrays", 4, "Hard", "Hard", "Write a C program to input N integer numbers into a single dimension array, sort them into ascending order using selection sort technique, and print both given array and sorted array with suitable headings.\nRead N then N integers. Output exact format:\nGiven Array: <space separated elements>\nSorted Array: <space separated elements>", True, [("3 3 1 2", "Given Array: 3 1 2\nSorted Array: 1 2 3"), ("4 10 5 8 2", "Given Array: 10 5 8 2\nSorted Array: 2 5 8 10"), ("1 42", "Given Array: 42\nSorted Array: 42"), ("3 5 5 5", "Given Array: 5 5 5\nSorted Array: 5 5 5"), ("2 9 1", "Given Array: 9 1\nSorted Array: 1 9")]),
    # Hard Filler (5)
    make_row("H001", "Pair Sum Target", "Arrays", 4, "Hard", "Hard", "Read n, n distinct integers, target. Print Yes if any pair sums to target else No.", False, [("4 1 2 3 4 5", "Yes"), ("3 1 2 3 7", "No"), ("2 5 5 10", "No"), ("2 4 6 10", "Yes"), ("3 10 20 30 50", "Yes")]),
    make_row("H002", "Majority Element", "Arrays", 4, "Hard", "Hard", "Read n and n integers. Print element appearing strictly more than n/2 times else -1.", False, [("3 1 1 2", "1"), ("4 1 2 3 4", "-1"), ("5 2 2 2 1 3", "2"), ("1 42", "42"), ("3 5 6 7", "-1")]),
    make_row("H003", "Rotate Left One", "Arrays", 4, "Hard", "Hard", "Read n and n integers. Rotate array left by 1 position and print space separated.", False, [("3 1 2 3", "2 3 1"), ("1 5", "5"), ("4 10 20 30 40", "20 30 40 10"), ("2 1 2", "2 1"), ("5 1 1 1 1 2", "1 1 1 2 1")]),
    make_row("H004", "Longest Increasing Subarray", "Arrays", 4, "Hard", "Hard", "Read n and n integers. Print length of longest strictly increasing contiguous subarray.", False, [("5 1 2 3 1 2", "3"), ("4 4 3 2 1", "1"), ("1 10", "1"), ("6 1 3 5 4 7 8", "3"), ("3 1 2 3", "3")]),
    make_row("H005", "Max Min Difference", "Arrays", 4, "Hard", "Hard", "Read n and n integers. Print difference between maximum and minimum elements.", False, [("3 1 5 2", "4"), ("1 10", "0"), ("4 -10 0 10 20", "30"), ("3 5 5 5", "0"), ("5 100 1 50 20 10", "99")])
]
write_csv("Module4_Arrays_Levels.csv", m4_rows)

# MODULE 5: Strings
m5_rows = [
    make_row("E001", "String Length", "Strings", 5, "Easy", "Easy", "Read a word and print its length.", False, [("hello", "5"), ("a", "1"), ("programming", "11"), ("code", "4"), ("openai", "6")]),
    make_row("E002", "First Character", "Strings", 5, "Easy", "Easy", "Read a word and print first character.", False, [("hello", "h"), ("apple", "a"), ("banana", "b"), ("cat", "c"), ("zebra", "z")]),
    make_row("E003", "Last Character", "Strings", 5, "Easy", "Easy", "Read a word and print last character.", False, [("hello", "o"), ("apple", "e"), ("banana", "a"), ("cat", "t"), ("zebra", "a")]),
    make_row("E004", "Count A", "Strings", 5, "Easy", "Easy", "Read a lowercase word and print count of 'a'.", False, [("banana", "3"), ("apple", "1"), ("hello", "0"), ("aaaa", "4"), ("code", "0")]),
    make_row("E005", "Has Digit", "Strings", 5, "Easy", "Easy", "Read a word and print Yes if it contains a digit else No.", False, [("code123", "Yes"), ("hello", "No"), ("a1b", "Yes"), ("test", "No"), ("9nine", "Yes")]),
    make_row("E006", "Convert to Uppercase", "Strings", 5, "Easy", "Easy", "Read a lowercase word and print in uppercase.", False, [("hello", "HELLO"), ("abc", "ABC"), ("code", "CODE"), ("a", "A"), ("xyz", "XYZ")]),
    make_row("E007", "Convert to Lowercase", "Strings", 5, "Easy", "Easy", "Read an uppercase word and print in lowercase.", False, [("HELLO", "hello"), ("ABC", "abc"), ("CODE", "code"), ("A", "a"), ("XYZ", "xyz")]),
    make_row("E008", "Count E", "Strings", 5, "Easy", "Easy", "Read a lowercase word and print count of 'e'.", False, [("elephant", "2"), ("hello", "1"), ("banana", "0"), ("eeee", "4"), ("code", "1")]),
    make_row("E009", "Starts with A", "Strings", 5, "Easy", "Easy", "Read a lowercase word and print Yes if starts with 'a' else No.", False, [("apple", "Yes"), ("banana", "No"), ("a", "Yes"), ("hello", "No"), ("ant", "Yes")]),
    make_row("E010", "Ends with Z", "Strings", 5, "Easy", "Easy", "Read a lowercase word and print Yes if ends with 'z' else No.", False, [("buzz", "Yes"), ("hello", "No"), ("z", "Yes"), ("topz", "Yes"), ("zebra", "No")]),
    make_row("M001", "Count Vowels", "Strings", 5, "Medium", "Medium", "Read a lowercase word and print vowel count.", False, [("hello", "2"), ("education", "5"), ("sky", "0"), ("apple", "2"), ("banana", "3")]),
    make_row("M002", "Count Consonants", "Strings", 5, "Medium", "Medium", "Read a lowercase alphabetic word and print consonant count.", False, [("hello", "3"), ("education", "4"), ("sky", "3"), ("apple", "3"), ("banana", "3")]),
    make_row("M003", "Lexicographic Compare", "Strings", 5, "Medium", "Medium", "Read two words space separated. Print First, Second, or Equal.", False, [("apple banana", "First"), ("cat bat", "Second"), ("same same", "Equal"), ("abc abd", "First"), ("z a", "Second")]),
    make_row("M004", "Reverse Word", "Strings", 5, "Medium", "Medium", "Read a word and print reverse.", False, [("hello", "olleh"), ("abc", "cba"), ("a", "a"), ("code", "edoc"), ("racecar", "racecar")]),
    make_row("M005", "Count Digits in String", "Strings", 5, "Medium", "Medium", "Read a word and print number of numeric digit characters.", False, [("a1b2c3", "3"), ("hello", "0"), ("12345", "5"), ("c0de", "1"), ("x9y8z7", "3")]),
    make_row("M006", "Replace Vowels X", "Strings", 5, "Medium", "Medium", "Read a lowercase word and replace all vowels with 'X'. Print result.", False, [("hello", "hXllX"), ("apple", "XpplX"), ("sky", "sky"), ("aeiou", "XXXXX"), ("banana", "bXnXnX")]),
    make_row("M007", "Char Frequency", "Strings", 5, "Medium", "Medium", "Read word and character space separated. Print frequency of char in word.", False, [("hello l", "2"), ("banana a", "3"), ("code z", "0"), ("test t", "2"), ("abc a", "1")]),
    make_row("M008", "Is Uppercase Word", "Strings", 5, "Medium", "Medium", "Read alphabetic word. Print Yes if all letters are uppercase else No.", False, [("HELLO", "Yes"), ("Hello", "No"), ("hello", "No"), ("A", "Yes"), ("CODE", "Yes")]),
    make_row("M009", "Concatenate Words", "Strings", 5, "Medium", "Medium", "Read two words space separated and print them joined together without space.", False, [("hello world", "helloworld"), ("foo bar", "foobar"), ("a b", "ab"), ("code lab", "codelab"), ("test case", "testcase")]),
    make_row("M010", "Print Alternating Chars", "Strings", 5, "Medium", "Medium", "Read word and print characters at even indices (0, 2, 4...).", False, [("hello", "hlo"), ("abcdef", "ace"), ("a", "a"), ("code", "cd"), ("banana", "bnn")]),
    # Hard Mandatory (Lab Manual Q5)
    make_row("LM001", "Palindrome String Check", "Lab Manual Strings", 5, "Hard", "Hard", "Write a C program to find if a given string is a palindrome or not.\nRead a word. Print 'Palindrome' if it reads the same backwards else 'Not Palindrome'.", True, [("madam", "Palindrome"), ("hello", "Not Palindrome"), ("racecar", "Palindrome"), ("level", "Palindrome"), ("code", "Not Palindrome")]),
    # Hard Filler (5)
    make_row("H001", "Longest Unique Substring", "Strings", 5, "Hard", "Hard", "Read word and print length of longest substring without repeating characters.", False, [("abcabcbb", "3"), ("bbbbb", "1"), ("pwwkew", "3"), ("abcdef", "6"), ("aab", "2")]),
    make_row("H002", "Anagram Check", "Strings", 5, "Hard", "Hard", "Read two lowercase words space separated. Print Anagram or Not Anagram.", False, [("listen silent", "Anagram"), ("hello bello", "Not Anagram"), ("earth heart", "Anagram"), ("cat act", "Anagram"), ("abc abd", "Not Anagram")]),
    make_row("H003", "Word Score", "Strings", 5, "Hard", "Hard", "Read lowercase word and print sum of alphabet positions (a=1, b=2... z=26).", False, [("abc", "6"), ("hello", "52"), ("a", "1"), ("z", "26"), ("code", "27")]),
    make_row("H004", "Remove Duplicate Chars", "Strings", 5, "Hard", "Hard", "Read lowercase word. Remove consecutive duplicate characters and print result.", False, [("aabccba", "abcba"), ("hello", "helo"), ("aaaaa", "a"), ("code", "code"), ("bookkeeper", "bokeper")]),
    make_row("H005", "Max Frequency Char", "Strings", 5, "Hard", "Hard", "Read lowercase word. Print the lexicographically smallest character with highest frequency.", False, [("banana", "a"), ("hello", "l"), ("abc", "a"), ("aabbcc", "a"), ("Mississippi", "s")])
]
write_csv("Module5_Strings_Levels.csv", m5_rows)

print("Modules 1 to 5 generated successfully.")
