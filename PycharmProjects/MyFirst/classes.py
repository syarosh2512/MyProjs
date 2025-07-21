from pkgutil import get_data


class Dog:
    """A simple Dog class with name and age attributes."""
    def __init__(self, name, age):
        # Initialize dog with name and age
        self.name = name
        self.age = age
        
    def set_data(self, name, age):
        # Update dog's name and age
        self.name = name
        self.age = age
        
    def get_data(self):
        # Return dog's data as dictionary
        return {'name': self.name, 'age': self.age}
        
    def __str__(self):
        # String representation of dog
        return f"{self.name}, {self.age} years old"


if __name__ == "__main__":
    # Create dog instances properly
    dog1 = Dog('Armin', 7)
    dog2 = Dog('Buldozer', 10)
    dog3 = Dog('Mia', 15)
    
    # Print using the string representation
    #print(dog1)
    #print(dog2)
    
    # Demonstrate set_data and get_data methods
    dog1.set_data('Rex', 5)
    print(f"Updated dog1: {dog1}")
    print(f"Dog1 data: {dog1.get_data()}")
    print(f"Dog2 data: {dog2.get_data()}")
    dog2.set_data('Rex', 5)
    print(f"Updated dog3: {dog3}")
    print(f"Dog3 data: {dog3.get_data()}")
