variable_dict = {}


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


def variable_setter(string_of_nums):
    global variable_dict
    if string_of_nums.count("=") > 1:
        raise InvalidCharacterError

    while " " in string_of_nums:
        string_of_nums = string_of_nums.replace(" ", "")

    list_of_nums = string_of_nums.split("=")
    variable = list_of_nums[0]
    value = list_of_nums[1]
    if not variable.isalpha():
        raise InvalidIdentifierError
    elif value.isalpha() and value not in variable_dict.keys():
        raise UnknownVariableError
    elif value.isalpha() and value in variable_dict.keys():
        variable_dict[variable] = variable_dict[value]
        return
    elif not value.isalpha() and not value.isnumeric():
        key_checker = 0
        for key in variable_dict.keys():
            if key in value:
                key_checker += 1
                key_length = len(key)
                index = value.index(key)
                value = str(int(value[:index]) * int(variable_dict[value[index:key_length + 1]]))
                variable_dict[variable] = value
                return
        if key_checker == 0:
            raise InvalidAssignmentError
    elif value.isnumeric():
        variable_dict[variable] = value
        return

def expression_checker(string_of_nums, index_list=[]):
    for count, char in enumerate(string_of_nums):
        if char not in ("+", "-", " ") and not char.isnumeric():
            raise InvalidCharacterError
        elif char in ("+", "-") and (string_of_nums[count - 1] != " " or string_of_nums[count + 1] != " "):
            if count == 0 and char == "-":
                pass
            elif char == "+" and count != len(string_of_nums) - 1 and string_of_nums[count + 1].isnumeric():
                index_list.append(count)
            else:
                raise InvalidCharacterError

    if len(index_list) != 0:
        for index in index_list:
            string_of_nums = string_of_nums[:index] + string_of_nums[index + 1:]
        return string_of_nums
    else:
        return string_of_nums


def evaluate_function(filtered_list):
    while len(filtered_list) != 1:
        if filtered_list[1] == "+":
            x = int(filtered_list.pop(0)) + int(filtered_list.pop(1))
            filtered_list[0] = x
        elif filtered_list[1] == "-":
            x = int(filtered_list.pop(0)) - int(filtered_list.pop(1))
            filtered_list[0] = x
    return filtered_list[0]


while True:
    input_nums = input()
    if input_nums == "/exit":
        print("Bye!")
        quit()
    elif input_nums == "/help":
        print("This program calculates the sum and/or difference of numbers.")
        continue
    elif not input_nums:
        continue
    else:
        while True:
            if "++" in input_nums or "--" in input_nums or "+-" in input_nums:
                input_nums = input_nums.replace("++", "+")
                input_nums = input_nums.replace("--", "+")
                input_nums = input_nums.replace("+-", "-")
            else:
                break
    try:
        # check for commands
        if "/" in input_nums:
            raise UnknownCommandError
        # check for variable
        if "=" in input_nums:
            variable_setter(input_nums)
            continue
        if input_nums.isalpha():
            key_checker = 0
            for key in variable_dict.keys():
                if key == input_nums:
                    key_checker += 1
            if key_checker == 0:
                raise UnknownVariableError

        if not any(char.isalpha() for char in input_nums):
            input_nums = expression_checker(input_nums)
        # need to check if there is an alphabetical, and if so, check if it is a valid variable in dict
        if any(char.isalpha() for char in input_nums):
            key_checker_2 = 0
            for key in variable_dict.keys():
                if key in input_nums:
                    key_checker_2 += 1
                    input_nums = input_nums.replace(key, variable_dict[key])
            if key_checker_2 == 0:
                raise InvalidIdentifierError

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

    input_nums = input_nums.split()

    input_nums = evaluate_function(input_nums)
    print(input_nums)
