import random

letters = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
]
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
symbols = ["!", "#", "$", "%", "&", "(", ")", "*", "+"]
characters = letters + numbers + symbols

print("Welcome to the PyPassword Generator!")
password_length = int(input("Specify the desired length of the password: "))


def generate_password(length, char_set):
    """
    Generates a random password based on the specified length and character set.

    Args:
        length (int): The desired length of the password.
        char_set (list): The list of characters to choose from.

    Returns:
        str: The generated password.
    """
    # Selects k characters from the lists
    characters_selected = random.choices(population=char_set, k=length)

    # Shuffling the password
    random.shuffle(characters_selected)

    # Joining the characters to form the password
    generated_password = ''.join(characters_selected)

    return generated_password


generated_password = generate_password(password_length, characters)
print("Generated password:", generated_password)