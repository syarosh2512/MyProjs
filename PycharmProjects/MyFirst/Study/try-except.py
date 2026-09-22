num = None
while num is None:
    try:
        num = int(input("Enter a number: "))
        num += 23
        print(num)
    except ValueError:
        print("неправильний  тип, введіть число")