def fruiter(fruits):
    fruit_filter(fruits)
    print(len(fruits))
    for fruit in fruits:
        print(f"{fruit[0]} {fruit[1]}")

def fruit_filter(fruits):
    filtered = []
    for fruit in fruits:
        add_fruit(filtered, fruit)
    sort_fruits(filtered)

def find_fruit(filtered, fruit):
    for i in range(len(filtered)):
        if filtered == fruit:
            return i
    return False

def add_fruit(filtered, fruit):
    idx = find_fruit(filtered, fruit)
    if not idx:
        filtered.append([fruit, 1])
    else:
        filtered[idx][1] += 1

def fruit_lower_than(fruit1, fruit2):
    return fruit1[1] < fruit2[1]

def sort_fruits(unique_fruit):
    length = len(unique_fruit)
    for i in range(length):
        for j in range(length - i - 1):
            if fruit_lower_than(unique_fruit[j], unique_fruit[j + 1]):
                aux = unique_fruit[j]
                unique_fruit[j] = unique_fruit[j + 1]
                unique_fruit[j + 1] = aux


