import random
import string

def generate_password():
    while True:
        password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(8))
        is_valid = (any(c.islower() for c in password)
                    and any(c.isupper() for c in password)
                    and any(c.isdigit() for c in password)
                    and any(c in string.punctuation for c in password))
        if is_valid:
            return password

def generate_mixed_passwords(n):
    passwords = []
    for _ in range(n):
        if random.choice([True, False]):
            password = generate_password()
            passwords.append(password)
        else:
            password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(8))
            passwords.append(password)
    return passwords


if __name__ == '__main__':
    print(generate_mixed_passwords(10))