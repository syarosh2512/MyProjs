class Dog:
    def __init__(self, name=None, age=None, isHappy=None):
        # self.name = name
        # self.age = age
        # self.isHappy = isHappy
        self.set_data(name, age, isHappy)
        self.get_data()

    def set_data(self, dog_name, dog_age, isHappy):
        self.name = dog_name
        self.age = dog_age
        self.isHappy = isHappy

    def get_data(self):
        #return self.name, self.age, self.isHappy
        print(self.name, "age:", self.age, "Happy:",  self.isHappy)

dog1 = Dog('Rex', 5, True)
dog2 = Dog('Snippy', 10, False)
dog3 = Dog('Mia', 15)

# dog1.get_data()
# dog2.get_data()