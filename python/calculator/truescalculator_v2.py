#!/usr/bin/env python3
# TRUE's Calculator-Version 2.0
# Built by JCTRUECONDE, guided by Paladin Raven

# Now with Functions, ERROR Handling and a LOOP.

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
       return "ERROR: cannot divide by Zero"
    return a / b


def get_number(prompt):
    while True:
       try:
          return float(input(prompt))
       except ValueError:
          print("That's not a valid number. Try Again.")


def get_operation():
    while True:
       op =  input("Choose an operation(+, -, *, /) or 'q' to quit:")
       if op in ["+", "-", "*", "/", "q"]:
           return op
       else:
           print("Invalid Choice. Please Enter +, -, *, /, or q.")


print("=" * 40)
print("TRUE's Calculator v2.0")
print("=" * 40)


while True:
    print("\n---New Calculation---")
    operation = get_operation()
    if operation == "q":
       print("Goodbye, True, stay sharp.")
       break


    num1 = get_number("Enter the first number:")
    num2 = get_number("Enter the second number:")


    if operation == "+":
       result = add(num1, num2)
    elif operation == "-":
       result = subtract(num1, num2)
    elif operation == "*":
       result = multiply(num1, num2)
    elif operation == "/":
       result = divide(num1, num2)

    print(f"\n result:{num1} {operation} {num2} = {result}")





















 











