import random
import string


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


print(random_string_generator())
print(''.join(random.choice("sdfsdfsdfsd") for x in range(10)))

print(string.ascii_lowercase)
print(string.digits)

print(list(random.choice(string.ascii_lowercase) for x in range(10)))
