def custom_generator(data):
    
    for index in range(len(data)):
        element = data[index]

        yield index, element

enum = custom_generator(['a', 'b', 'c'])

print(next(enum))
print(next(enum))
print(next(enum))


