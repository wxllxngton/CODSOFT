power_status = True
next_calculation = {}

logo = """
 _____________________
|  _________________  |
| | Pythonista   0. | |  .----------------.  .----------------.  .----------------.  .----------------.
| |_________________| | | .--------------. || .--------------. || .--------------. || .--------------. |
|  ___ ___ ___   ___  | | |     ______   | || |      __      | || |   _____      | || |     ______   | |
| | 7 | 8 | 9 | | + | | | |   .' ___  |  | || |     /  \     | || |  |_   _|     | || |   .' ___  |  | |
| |___|___|___| |___| | | |  / .'   \_|  | || |    / /\ \    | || |    | |       | || |  / .'   \_|  | |
| | 4 | 5 | 6 | | - | | | |  | |         | || |   / ____ \   | || |    | |   _   | || |  | |         | |
| |___|___|___| |___| | | |  \ `.___.'\  | || | _/ /    \ \_ | || |   _| |__/ |  | || |  \ `.___.'\  | |
| | 1 | 2 | 3 | | x | | | |   `._____.'  | || ||____|  |____|| || |  |________|  | || |   `._____.'  | |
| |___|___|___| |___| | | |              | || |              | || |              | || |              | |
| | . | 0 | = | | / | | | '--------------' || '--------------' || '--------------' || '--------------' |
| |___|___|___| |___| |  '----------------'  '----------------'  '----------------'  '----------------'
|_____________________|
"""
print(logo)


def add(n1, n2):
    """
    Adds two numbers.

    Args:
        n1 (float): The first number.
        n2 (float): The second number.

    Returns:
        float: The sum of n1 and n2.
    """
    return n1 + n2


def subtract(n1, n2):
    """
    Subtracts the second number from the first.

    Args:
        n1 (float): The first number.
        n2 (float): The second number.

    Returns:
        float: The result of n1 - n2.
    """
    return n1 - n2


def multiply(n1, n2):
    """
    Multiplies two numbers.

    Args:
        n1 (float): The first number.
        n2 (float): The second number.

    Returns:
        float: The product of n1 and n2.
    """
    return n1 * n2


def divide(n1, n2):
    """
    Divides the first number by the second number.

    Args:
        n1 (float): The numerator.
        n2 (float): The denominator.

    Returns:
        float: The result of n1 / n2.
    """
    if n2 != 0:
        return n1 / n2
    else:
        return "Error: Division by zero."


def calculator(first_number, last_number, operator):
    """
    Performs calculations based on the provided operator.

    Args:
        first_number (float): The first number.
        last_number (float): The second number.
        operator (str): The operator (+, -, *, /).

    Returns:
        float or str: The result of the calculation or an error message.
    """
    if operator == "+":
        result = add(first_number, last_number)
    elif operator == "-":
        result = subtract(first_number, last_number)
    elif operator == "*":
        result = multiply(first_number, last_number)
    elif operator == "/":
        result = divide(first_number, last_number)
    else:
        return "Invalid operation! Try again."

    next_calculation["result"] = result
    return result


while power_status:
    continue_msg = None

    try:
        f_number = float(input("What is the first number? "))
        print("+\n-\n*\n/")
        operation = input("Pick an operation: ")
        l_number = float(input("What is the next number? "))
        result_carried = calculator(
            first_number=f_number, last_number=l_number, operator=operation
        )
        print(f"{f_number} {operation} {l_number} = {result_carried}")

        while True:
            continue_msg = input(
                f"Type 'y' to continue with {result_carried}, 'n' to start a new calculation, or 'q' to quit: "
            )

            if continue_msg == "n":
                break
            elif continue_msg == "q":
                power_status = False
                break

            f_number = next_calculation.get("result", 0)
            print("+\n-\n*\n/")
            operation = input("Pick an operation: ")
            l_number = float(input("What is the next number? "))
            result_carried = calculator(
                first_number=f_number, last_number=l_number, operator=operation
            )
            print(f"{f_number} {operation} {l_number} = {result_carried}")

    except ValueError:
        print("Input a number!")
    except Exception as err:
        print(f"Error: {str(err).capitalize()}")

else:
    print("\nPower Off!")
