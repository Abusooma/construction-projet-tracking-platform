import random
import string


def generate_random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


if __name__ == '__main__':
    password_generate = generate_random_password()

