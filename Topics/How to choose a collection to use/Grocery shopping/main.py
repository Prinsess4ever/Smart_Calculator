from collections import defaultdict

food = defaultdict(list)
shopping_list = input().split()

for grocery_food in shopping_list:
    food[grocery_food].append(grocery_food)

for the_food, how_many in food.items():
    print(f'{len(how_many)} {the_food}')
