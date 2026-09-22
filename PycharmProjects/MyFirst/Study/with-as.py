

with open('3130.txt', 'r',encoding="utf-8") as file:
    content = file.read()
print(content)


try:
    with open('3130.txt', 'a', encoding="utf-8") as file:
        file.write("привіт \n")
        file.write("STEm IS Good \n")

except FileNotFoundError:
    print("File not found")
finally:
    print("File closed")

with open('3130.txt', 'a', encoding="utf-8") as file:
    file.write("привіт \n")
    file.write("STEm IS Good \n")

# Перевірка зчитування з файлу
with open('3130.txt', 'r', encoding="utf-8") as file:
    content = file.read()
    print(content)