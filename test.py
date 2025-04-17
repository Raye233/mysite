s = "a good   example   "
lst = list(s)
while lst and lst[-1] == " ":
    lst.pop()
while lst and lst[0] == " ":
    lst.pop(0)
print(lst)
new_lst = ''.join(lst).split(" ")
print(new_lst)
final_lst = [each for each in new_lst if each != ""]
print(final_lst)
final_lst.reverse()
print(' '.join(final_lst))