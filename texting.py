def disemvowel(string):
    vowels = ["a", "e", "i", "o", "u"]
    string_list = []
    for i in string:
        if i.lower() not in vowels:
            string_list.append(i)
    string = ''.join(string_list)
    return string


# lolla = disemvowel("This website is for losers LOL!")
# print(lolla)

# puka = disemvowel("N ffns bt,\nYr wrtng s mng th wrst I'v vr rd")
# print(puka)


def high_and_low(numbers):
    pass


numbers = "4 5 29 54 4 0 -214 542 -64 1 -3 6 -6"


def find_short(s):
    l = [len(word) for word in s.split()]
    return min(l)


print(find_short("lolla loll"))