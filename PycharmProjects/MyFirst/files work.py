# with open("3130.txt", "r") as f:
#     print(f.read(), end="")

data = input("Enter your name: ")
file = open("user1.txt", "a+")

file.write("Name is: " + data + "\n")

data = input("Enter your hobby: ")
file.write("Hobby : " + data + " \n")

file.close()

file = open("user1.txt", "r")

print(file.read())

file.close()