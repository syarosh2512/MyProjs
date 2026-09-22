myset = {1,2,3,4,5, 7,5,6}
print(myset, type(myset))
myset.add(10)
# myset.clear()
print (myset, type(myset))
myset.add(100)
myset.remove(10)

print(myset)
myset.discard(100)
print(myset)
word = "hello"
set2= set(word)
print(set2)
set2.pop()
print(set2)