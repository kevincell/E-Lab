import os
from django.utils.text import slugify
from core.models import Module, Question, TestCase

modules_data = [
    {
        "name": "Introduction to Programming",
        "questions": [
            ("Hello World", "Print 'Hello, World!' to the console."),
            ("Sum of Two Numbers", "Given two integers, print their sum."),
            ("Area of Circle", "Given radius r, find area of circle (pi=3.14)."),
            ("Temperature Conversion", "Convert Celsius to Fahrenheit."),
            ("Simple Interest", "Calculate simple interest for given P, R, T."),
            ("Even or Odd", "Determine if a number is even or odd."),
            ("Find Maximum", "Find max of two numbers."),
            ("ASCII Value", "Print ASCII value of a character."),
            ("Swap Two Numbers", "Swap two numbers without third variable."),
            ("Vowel or Consonant", "Check if a character is vowel or consonant.")
        ]
    },
    {
        "name": "Decision Making and Looping",
        "questions": [
            ("Leap Year", "Check if a given year is a leap year."),
            ("Factorial", "Calculate the factorial of a number."),
            ("Fibonacci Series", "Print the first n terms of Fibonacci series."),
            ("Prime Number", "Check if a number is prime."),
            ("Sum of Digits", "Find the sum of digits of a number."),
            ("Reverse Number", "Reverse a given integer."),
            ("Palindrome Number", "Check if a number is palindrome."),
            ("Armstrong Number", "Check if a number is Armstrong."),
            ("Multiplication Table", "Print multiplication table of N."),
            ("Count Digits", "Count the number of digits in an integer.")
        ]
    },
    {
        "name": "Logic Building",
        "questions": [
            ("Bitwise AND of Range", "Find bitwise AND of all numbers in [left, right]."),
            ("Power of Two", "Check if a number is a power of 2."),
            ("Count Set Bits", "Count number of 1s in binary representation."),
            ("Toggle Bits", "Toggle all bits of a number."),
            ("Missing Number", "Find the missing number in an array of size n containing 1 to n."),
            ("Number of Trailing Zeroes", "Find number of trailing zeroes in N!."),
            ("Perfect Number", "Check if a number is a perfect number."),
            ("Check Kth Bit", "Check if Kth bit is set or not."),
            ("Set Kth Bit", "Set the Kth bit of a number."),
            ("Square Root", "Find the integer square root of a number.")
        ]
    },
    {
        "name": "Functions and Arrays",
        "questions": [
            ("Max Element in Array", "Find maximum element in an array."),
            ("Reverse Array", "Reverse the given array."),
            ("Array Sum", "Find sum of all array elements."),
            ("Linear Search", "Search for an element x in array."),
            ("Remove Duplicates", "Remove duplicates from sorted array."),
            ("Rotate Array", "Rotate array to the right by k steps."),
            ("Second Largest", "Find the second largest element in array."),
            ("Move Zeroes", "Move all zeroes to the end of the array."),
            ("Majority Element", "Find the majority element in array."),
            ("Intersection of Two Arrays", "Find intersection of two arrays.")
        ]
    },
    {
        "name": "Strings and Pointers",
        "questions": [
            ("Reverse String", "Reverse the given string."),
            ("Palindrome String", "Check if a string is palindrome."),
            ("Anagrams", "Check if two strings are anagrams."),
            ("Count Vowels", "Count vowels in a string."),
            ("First Unique Character", "Find first non-repeating character."),
            ("String Length", "Find length of string without library function."),
            ("Concatenate Strings", "Concatenate two strings."),
            ("Longest Common Prefix", "Find longest common prefix string among an array of strings."),
            ("Valid Parentheses", "Check if string has valid parentheses."),
            ("String to Integer (atoi)", "Convert string to integer.")
        ]
    },
    {
        "name": "Language Deep Dive and Debugging",
        "questions": [
            ("Memory Allocation", "Allocate memory for N integers and print sum."),
            ("Pointer Arithmetic", "Use pointers to print array elements."),
            ("Dangling Pointer Fix", "Correct a code snippet to fix dangling pointer."),
            ("Memory Leak Fix", "Fix a memory leak in the given code."),
            ("Segmentation Fault Debug", "Fix out of bounds access."),
            ("Macro Expansion", "Write a macro to find max of two numbers."),
            ("Command Line Arguments", "Print all command line arguments."),
            ("Struct Padding", "Calculate struct size with padding."),
            ("Function Pointers", "Use function pointer to call add()."),
            ("Bit Fields", "Use bit fields to store flags.")
        ]
    },
    {
        "name": "Structures, Recursion, File Handling",
        "questions": [
            ("Student Struct", "Create a struct Student and print its details."),
            ("Complex Number Addition", "Add two complex numbers using structs."),
            ("Factorial (Recursive)", "Find factorial using recursion."),
            ("Fibonacci (Recursive)", "Find Nth Fibonacci number recursively."),
            ("Tower of Hanoi", "Solve Tower of Hanoi for N disks."),
            ("Read File", "Read contents of a file and print."),
            ("Write File", "Write \"Hello\" to a file."),
            ("Copy File", "Copy contents from one file to another."),
            ("Count Lines in File", "Count number of lines in a file."),
            ("Recursive Array Sum", "Find sum of array elements recursively.")
        ]
    },
    {
        "name": "Searching and Sorting Algorithms",
        "questions": [
            ("Binary Search", "Implement Binary Search."),
            ("Bubble Sort", "Implement Bubble Sort."),
            ("Selection Sort", "Implement Selection Sort."),
            ("Insertion Sort", "Implement Insertion Sort."),
            ("Merge Sort", "Implement Merge Sort."),
            ("Quick Sort", "Implement Quick Sort."),
            ("First and Last Position", "Find first and last position of element in sorted array."),
            ("Search in Rotated Sorted Array", "Search element in a rotated sorted array."),
            ("Peak Element", "Find peak element in array."),
            ("Kth Largest Element", "Find Kth largest element in array.")
        ]
    },
    {
        "name": "Introduction to Data Structures",
        "questions": [
            ("Implement Stack", "Implement stack using array."),
            ("Implement Queue", "Implement queue using array."),
            ("Valid Parentheses Stack", "Check valid parentheses using stack."),
            ("Next Greater Element", "Find next greater element for each array element."),
            ("Reverse Queue", "Reverse a queue."),
            ("Min Stack", "Implement stack that supports getMin()."),
            ("Implement Deque", "Implement double ended queue."),
            ("Evaluate Postfix", "Evaluate postfix expression."),
            ("Queue using Stacks", "Implement queue using two stacks."),
            ("Stack using Queues", "Implement stack using two queues.")
        ]
    },
    {
        "name": "Linked Lists and Recursion-Based Problems",
        "questions": [
            ("Reverse Linked List", "Reverse a singly linked list."),
            ("Middle of Linked List", "Find the middle node of a linked list."),
            ("Merge Two Sorted Lists", "Merge two sorted linked lists."),
            ("Remove Nth Node From End", "Remove Nth node from end of list."),
            ("Linked List Cycle", "Detect cycle in a linked list."),
            ("Palindrome Linked List", "Check if linked list is palindrome."),
            ("Intersection of Two Linked Lists", "Find intersection node of two lists."),
            ("Delete Node", "Delete a given node from linked list."),
            ("Add Two Numbers", "Add two numbers represented by linked lists."),
            ("Flatten a Multilevel Doubly Linked List", "Flatten the list.")
        ]
    },
    {
        "name": "Competitive Programming Basics",
        "questions": [
            ("Maximum Subarray Sum", "Find contiguous subarray with max sum (Kadane's)."),
            ("Two Sum", "Find indices of two numbers that add up to target."),
            ("Climbing Stairs", "Find distinct ways to climb n stairs."),
            ("Best Time to Buy and Sell Stock", "Maximize profit from stock prices."),
            ("Coin Change", "Find minimum coins to make amount."),
            ("Longest Increasing Subsequence", "Find length of LIS."),
            ("Edit Distance", "Find minimum operations to convert word1 to word2."),
            ("0/1 Knapsack", "Solve 0/1 Knapsack problem."),
            ("Subset Sum", "Check if there is a subset with given sum."),
            ("Grid Unique Paths", "Find unique paths from top-left to bottom-right.")
        ]
    }
]

print("Starting to seed database...")

order = 1
for mod_data in modules_data:
    module, created = Module.objects.get_or_create(
        name=mod_data["name"],
        category='placement_training',
        defaults={'level': 2, 'order': order}
    )
    if not created:
        module.level = 2
        module.order = order
        module.save()
        
    print(f"Created/Updated Module: {module.name}")
    order += 1
    
    for i, (title, desc) in enumerate(mod_data["questions"]):
        slug = slugify(f"{mod_data['name']}-{title}-{i}")
        question, q_created = Question.objects.get_or_create(
            slug=slug,
            defaults={
                'title': title,
                'description': desc,
                'sample_input': '1\n2',
                'sample_output': '3',
                'allow_multiple_languages': True,
                'language_id': 50,
                'module': module
            }
        )
        if not q_created:
            question.title = title
            question.description = desc
            question.module = module
            question.save()
            
        # Create at least 2 TestCases
        for tc_i in range(1, 3):
            TestCase.objects.get_or_create(
                question=question,
                stdin=f"test input {tc_i}",
                expected_output=f"test output {tc_i}",
                is_sample=False
            )
        
        print(f"  - Created/Updated Question: {question.title}")

print("Seeding completed successfully!")
