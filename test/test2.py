def handle(s):
    if any(char.isupper() for char in s):
        s = s.lower()
    s = s.replace(" ", "")
    i = 0
    while i < len(s):
        if not s[i].isalnum():
            s = s.replace(s[i], "")
        else:
            i += 1
    print(s)
    return s

def judge(string):
    mid = len(string) // 2
    if len(string) % 2 == 0 and string[:mid] == string[-1: mid - 1: -1]:
        return True
    elif len(string) % 2 == 1 and string[:mid] == string[-1: mid: -1]:
        return True
    return False

    print(string[mid])
    print(mid)
# abba
# 0123
s = "A man, a plan, a canal: Panama"
judge(s)
