class User:
    def __init__(self, username, password, age=None):
        self.name = username
        self.__age = age
        self.__password = password
    def check_password(self, password):
        return self.__password == password
    def get_age(self):
        return self.__age


u1 =  User('Armin', '1234')

print(u1.name)
print(u1.get_age())
print(u1.check_password('1234'))  # Use the check_password method instead

class Animal:
    def __init__(self, name=None):
        self.name = name
    def speak(self):
        print(f"{self.name} makes a sound")
class Dog(Animal):
    def speak(self):
        print(f"{self.name} barks")
class Cat(Animal):
    def speak(self):
        print(f"{self.name} meows")
dog = Dog("Armin")
cat = Cat("Mia")
dog.speak()  # Output: Buddy barks
cat.speak()  # Output: Whiskers meows