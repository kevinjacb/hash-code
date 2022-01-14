with open("a_an_example.in.txt",'r',encoding='utf-8') as f:
    file_data = f.read()

file_data = file_data.split('\n')
print(file_data)

total_customers = int(file_data[0]) #total customers
liked_ingredients = dict() #liked_ingredients corresponding to the customer
disliked_ingredients = dict() #disliked ingredients corresponding to the customer
all_ingredients = dict() #ingredients with their corresponding likes, dislikes and dont care counts

liked_common = dict() #count of customers who share common liked ingredients (unused)
disliked_common = dict() #count of customers who share common disliked ingredients (unused)

for i in range(0,int(file_data[0])):
    liked_ingredients[i] = file_data[i*2+1].split(" ")  
    disliked_ingredients[i] = file_data[i*2+2].split(" ")

for i in liked_ingredients:
    for ingredient in liked_ingredients[i]:
        if not ingredient.isdigit() and not ingredient in all_ingredients.keys():
            all_ingredients[ingredient] = [0]*3
        if ingredient in liked_common.keys() and not ingredient.isdigit():
            liked_common[ingredient] += 1
            all_ingredients[ingredient][0] += 1
        elif not ingredient.isdigit():
            liked_common[ingredient] = 1
            all_ingredients[ingredient][0] = 1

for i in disliked_ingredients:
    for ingredient in disliked_ingredients[i]:
        if not ingredient.isdigit() and not ingredient in all_ingredients.keys():
            all_ingredients[ingredient] = [0]*3
        if ingredient in disliked_common.keys() and not ingredient.isdigit():
            disliked_common[ingredient] += 1
            all_ingredients[ingredient][1] += 1
        elif not ingredient.isdigit():
            disliked_common[ingredient] = 1
            all_ingredients[ingredient][1] = 1

print(all_ingredients)
print(liked_ingredients)
print(disliked_ingredients)
print(liked_common)
print(disliked_common)
