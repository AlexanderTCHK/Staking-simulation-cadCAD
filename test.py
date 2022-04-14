import random
dic = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five"
}

dic_lst = list(dic)
print(dic_lst)
print(type(dic_lst))
shuffle = random.shuffle(dic_lst)
print(shuffle)

mylist = ["apple", "banana", "cherry"]
random.shuffle(mylist)

print(mylist)