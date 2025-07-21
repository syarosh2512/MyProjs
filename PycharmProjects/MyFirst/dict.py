person = {"user1": {
    'name': 'Jason',
    'age': 20,
    'address': ('Rivne', 'Myra street', 35314),
    'car' : 'Honda CV'
    },
"user2": {
    'name': 'Mason',
    'age': 24,
    'city': 'Dubno',
    'car' : 'Lanos'
}
}

# print(person.get('age'))
# person['phone'] = "+380734567890"
#
# print(person.get('phone'))
# print(person.keys())
# print(person.values())
# print(person.items())

# for key, value in person.items():
#     print(key, ":", value)

for value, key in person.items():
    print(value, key)

# person.clear()
# person.pop('car')
# print(person)
# person.popitem()
# print(person)

print(person["user1"]['address'][1])