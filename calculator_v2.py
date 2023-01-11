from collections import deque
import re


class InvalidCharacterError(Exception):
    def __str__(self):
        return "Invalid character(s) used!"


class UnknownCommandError(Exception):
    def __str__(self):
        return "Unknown command"


class InvalidIdentifierError(Exception):
    def __str__(self):
        return "Invalid identifier"


class UnknownVariableError(Exception):
    def __str__(self):
        return "Unknown variable"


class InvalidAssignmentError(Exception):
    def __str__(self):
        return "Invalid Assignment"


class Calculator:
    operators = {'+', '-', '*', '/', '^', '(', ')'}  # collection of operators
    incorrect_operators = {"**", "//", "^^", "/*", "*/"}  # collection of incorrect operators
    priority = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}  # priorities of operators
    variable_dictionary = {}
    '''
    The init initializes the expression, stacks, and outputs when converting from infix -> postfix -> output
    '''
    def __init__(self, expression):
        self.expression = expression
        self.postfix_stack = deque()
        # postfix_expression is where popped elements will be appended to
        self.postfix_expression = []
        self.output_stack = deque()
        self.output = []

        # check for invalid operators
        if any(operator in self.expression for operator in self.incorrect_operators):
            raise InvalidCharacterError

        if self.expression.count("(") != self.expression.count(")"):
            raise InvalidCharacterError

        # clean initial_expression to get rid of unnecessary + and convert -
        while True:
            if "++" in self.expression or "--" in self.expression or "+-" in self.expression:
                self.expression = self.expression.replace("++", "+")
                self.expression = self.expression.replace("--", "+")
                self.expression = self.expression.replace("+-", "-")
                # self.expression = self.expression.replace(" ", "")
            else:
                break
    '''Checks for invalid commands'''
    def command(self):
        if "/" == self.expression[0] and self.expression[1:] not in ("help", "exit"):
            raise UnknownCommandError
        elif self.expression == "/help":
            print("The program does ...")
            return True
        elif self.expression == "/exit":
            print("Bye!")
            quit()
            return
    '''Checks for invalid variables and assigns if no errors found'''
    def variable(self):
        self.strip_expression = self.expression.strip()
        if self.strip_expression.isalpha():
            if self.strip_expression in self.variable_dictionary.keys():
                # this will change the expression to the value and print the value
                # this occurs if the input is just the variable
                self.strip_expression = self.variable_dictionary[self.strip_expression]
                print(self.strip_expression)
                return True
            else:
                raise UnknownVariableError

        if "=" in self.expression:
            if self.expression.count("=") > 1:
                raise InvalidCharacterError
            '''split_assignment is splitting the assignment of a variable into the variable and value'''
            self.split_assignment = self.expression.split("=")
            self.split_assignment = [item.strip() for item in self.split_assignment]
            variable, value = self.split_assignment[0], self.split_assignment[1]
            if not variable.isalpha():
                raise InvalidIdentifierError
            elif value.isalpha() and value not in self.variable_dictionary.keys():
                raise UnknownVariableError
            elif value.isnumeric():
                self.variable_dictionary[variable] = value
                return True
            elif value.isalpha() and value in self.variable_dictionary.keys():
                self.variable_dictionary[variable] = self.variable_dictionary[value]
                return True
            elif not value.isalpha() and not value.isnumeric():
                split_variable = re.split('(\d+)', value)
                if split_variable[2] not in self.variable_dictionary.keys():
                    raise InvalidAssignmentError
                elif split_variable[1].isalpha():
                    # this error is raised if the variable is before the number being multiplied to it
                    raise InvalidIdentifierError
                else:
                    evaluation = int(split_variable[1]) * int(self.variable_dictionary[split_variable[2]])
                    self.variable_dictionary[variable] = str(evaluation)
                    return True

    '''Converts to postfix'''
    def to_postfix(self):
        # self.expression_l is used for iteration. append to self.expression_list
        # this separates elements into their own entry in the list to deal with multi-digit numbers
        self.expression_l = self.expression.split()
        self.expression_list = []
        for char in self.expression_l:
            index = self.expression_l.index(char)
            if "(" in char:
                p_index = char.index("(")
                num_or_var = char[p_index + 1:]
                self.expression_list.append("(")
                self.expression_list.append(num_or_var)
            elif ")" in char and index != len(self.expression_list) - 1:
                p_index = char.index(")")
                num_or_var = char[:p_index]
                self.expression_list.append(num_or_var)
                self.expression_list.append(")")
            elif ")" in char and index == len(self.expression_list) - 1:
                p_index = char.index(")")
                num_or_var = char[:p_index]
                self.expression_list.append(num_or_var)
                self.expression_list.append(")")
            else:
                self.expression_list.append(char)

        for char in self.expression_list:
            if char.isalnum():
                '''add to result if number or variable'''
                self.postfix_expression.append(char)
            elif char in self.operators:
                # If the stack is empty or the top of the stack is a left parenthesis
                if len(self.postfix_stack) == 0 or self.postfix_stack[-1] == "(":
                    self.postfix_stack.append(char)
                elif char == "(":
                    self.postfix_stack.append(char)
                elif char == ")":
                    while self.postfix_stack[-1] != "(":
                        self.postfix_expression.append(self.postfix_stack.pop())
                    # this will pop the left parenthesis to discard it
                    self.postfix_stack.pop()
                # If the priority of the incoming char is greater than the top of stack
                elif self.priority[char] > self.priority[self.postfix_stack[-1]]:
                    self.postfix_stack.append(char)
                elif self.priority[char] <= self.priority[self.postfix_stack[-1]]:
                    while len(self.postfix_stack) != 0 and self.postfix_stack[-1] != "(":
                        if self.priority[char] <= self.priority[self.postfix_stack[-1]]:
                            self.postfix_expression.append(self.postfix_stack.pop())
                        else:
                            break
                    self.postfix_stack.append(char)
        while len(self.postfix_stack) != 0:
            self.postfix_expression.append(self.postfix_stack.pop())
        return
    '''Converts postfix to an output number'''
    def to_output(self):
        for char in self.postfix_expression:
            if char.isnumeric():
                self.output_stack.append(char)
            elif char.isalpha():
                self.output_stack.append(self.variable_dictionary[char])
            elif char in self.operators and char != "^":
                num1 = self.output_stack.pop()
                num2 = self.output_stack.pop()
                eval_string = f'{num2}{char}{num1}'
                self.output_stack.append(eval(eval_string))
            elif char == "^":
                num1 = self.output_stack.pop()
                num2 = self.output_stack.pop()
                eval_string = f'{num2}**{num1}'
                self.output_stack.append(eval(eval_string))
        final_result = self.output_stack.pop()
        print(int(final_result))

'''Main script'''
if __name__ == "__main__":
    while True:
        try:
            expression = input()
            if not expression:
                continue
            expression_object = Calculator(expression)
            if "/" in expression:
                help_checker = expression_object.command()
                if help_checker:
                    continue
            if any(char.isalpha() for char in expression):
                # checks if it needs to assign a variable. If the variable is just in an expression, nothing happens
                var_checker = expression_object.variable()
                if var_checker:
                    continue
            expression_object.to_postfix()
            expression_object.to_output()

        except InvalidCharacterError as err:
            print(err)
            continue
        except UnknownCommandError as err:
            print(err)
            continue
        except InvalidIdentifierError as err:
            print(err)
            continue
        except UnknownVariableError as err:
            print(err)
            continue
        except InvalidAssignmentError as err:
            print(err)
            continue
