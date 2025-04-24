# student= {
#     "name":"<Jack>",
#     "age":20,
#     "is_new":True,
#
# }
#
# print("Jon's book")
# print('Jon\'s book')
#
# #math
from queue import PriorityQueue

# num = [2,3,4,5]
# num.append (9)
# num=num*2
# print(type(num),"list is new",num)
# num1 = [21,31,41,51]
# boll = True
# print(boll, num1+num)
#
# world = "circumstances"
# print(world)
#
# a = int(input("Enter a number 1:"))
# b = int(input("Enter a number 2:"))
# c = float(input("Enter a number 3:"))
#
# k = a+b+c
# print("result is = ", type(k))
# print("result is = ", a+b+c)

# age = int(input("Enter your age "))
#
# status = "Adult" if age > 18 else "Junior"
# print(status)

# for i in range(1,10,2):
#     print(i)

# for i in range(1,5):
#     print("\n","i=", i, "\n")
#     for j in range(i,5):
#         print("j=",j)

# from datetime import datetime
# now = datetime.now()
# print(now.strftime("%Y-%m-%d %H:%M:%S")) # Outputs

# import os, sys
# print(os.getcwd())
# print(sys.path)
# print(os.listdir())
#
# print('__file__', __file__)
# print(os.path.abspath(__file__))

# work =True
# while work:
#     user_input = input("Enter 'q' to quit, or any other key to continue: ")
#     if user_input == 'q':
#         work = False
#     else:
#         print("You entered:", user_input)
# print("Goodbye!")

# for i in range(1,12):
#     # if i%2 == 0:
#     #     continue
#     if i==8:
#         break
#     print("El= ",i)

# for i in "Mystery impossible":
#     if i == "ow":
#         print("Found it!")
#         break
# else:
#     print("Not found")
#
# # print("\nGoodbye!")

# fruits= ["Apple", "Banana", "Orange", "Mango", "Grapes"]
# print(fruits.index("Orange"))
# for fruit in fruits:
#     print(fruit)
#
# fruits.sort()
# print(fruits.index("Orange"))
# for fruit in fruits:
#     print(fruit)

# list1 = [1, 2, 3, 4, 5, 22]
# list2 = [12, 14, 6, 7, 8, 9, 10]
# # list3 = list1 + list2
# list1.extend(list2)
# print(list1)
# print(list1.count(2))
# # list3.sort()
# # print(list3)
# list1.reverse()
# print(list1)
# list1.append(101)
# print(list1)
#
# list3 = [x**2 for x in range(12)]
# print(list3)
# list3.sort()
# list3.pop()
# print(list3[::-1])
# print(len(list3))

# text = "Python best ever"
# # print(type(text))
# # print(len(text))
# list1 = list(text)
# # print(len(list1))
# # print(text.count("e"))
# # print(text[0])
# # print(text[-1])
# # print(text[::-1])
# # new_text = "J" + text[1:]
# # print(new_text)
# result = "\\".join(text)
# print(result.capitalize())
# list1.append("!")
# print(text)
# print(list1[::-1])
# text = 'football,basketball,cricket,drive'
# # hobbies = 'dancing, playing, reading'
# hobbies = text.split(',')
# # print(text1)
# # print(hobbies)
# # print(myhobbies)
# # print(type(myhobbies))
#
# for i in range(0, len(hobbies)):
#     hobbies[i] = hobbies[i].capitalize()
#
# print(hobbies, type(hobbies))
#
# result = ",".join(hobbies)
# print(result, type(result))

lis = [5, 2, 7, 4, 9, [4,99,11]]
print(lis[2])
print(lis[2:4])
print(lis[2:])
print(lis[::-1])
print(lis[:-3:-1])

