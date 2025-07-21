try:
    a = 10
    b = int(input("Введіть число: "))
    print("Тип коректний")
    print(a / b)
except ValueError:
    print("Ви не ввели число")
except ZeroDivisionError:
    print("Ділити на нуль не можна")
else:
    print("ви молодець")
finally:
    print("FINITA")