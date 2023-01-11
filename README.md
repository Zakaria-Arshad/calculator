# calculator OOP Python script by Zakaria Arshad

This calculator can store variables and output the result of mathematical calculations using proper PEMDAS

Calculator v1: Can only handle addition and subtraction

Calculator v2: Full addition of all operators. Can now use PEMDAS. Switched script to use OOP/Classes to make functionality easier and code cleaner. Can pass
most random test cases in case of errors with custom errors including "Unknown Variable", "Invalid Assignment", etc.

Two known test case failures for v2 - Cannot handle parenthesis inside parenthesis. Also cannot perform calculation when assigning a variable (i.e a = 1+1)
  Second test case can most likely be fixed by making string past the "=" an object of Calculator class and performing the calculation to return a value
