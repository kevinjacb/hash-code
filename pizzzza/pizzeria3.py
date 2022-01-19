import math

with open("c_coarse.in.txt",'r',encoding='utf-8') as f:
    file_data = f.read()

file_data = file_data.split('\n')

# print(file_data)

total_customers = int(file_data[0]) #total customers
customer_choice = dict() # preference dipicted in trinary form XD for eg : (cheese, eggs, chicken, mayo, mustard sauce): 1,0,1,1,-1,0 where -1 represents dont care and 0 represents dislike
ingredients = dict()

ingredient_count = 0

for file in file_data:
    file = file.split(" ")
    for ingredient in file:
        if not ingredient.isdigit() and not ingredient in ingredients.keys():
            ingredients[ingredient] = ingredient_count
            ingredient_count += 1

# print(ingredient_count)
for i,file in enumerate(file_data):
    file = file.split(" ")
    if(i % 2 == 1 or  i == 0):
        preference = [-1]*ingredient_count
    for ingredient in file:
        if not ingredient.isdigit():
            if(i % 2 == 0 and i != 0):
                preference[ingredients[ingredient]] = 0
            elif i != 0: 
                preference[ingredients[ingredient]] = 1
    customer_choice[int((i-1)/2)] = preference 

# print(customer_choice)
# print(ingredients)
# print(liked_ingredients)
# print(disliked_ingredients)
def sort(preference):
    likes = 0
    dislikes = 0
    for i in range(len(preference)):
        if preference[i] == 1:
            likes += 1
        elif preference[i] == 0:
            dislikes += 1
    if dislikes == 0:
        return likes
    return likes/dislikes

# print(customer_choice)
sorted_customer_choice = dict()
for x, y in sorted(customer_choice.items(), key=sort):
    sorted_customer_choice[x] = y
# print(sorted_customer_choice)


rejected_customers = []
score = 0
for i in range(ingredient_count):
    rejected = len(rejected_customers)
    # print(rejected)
    score = total_customers - rejected
    likes = 0
    dislikes = 0
    neutral = 0
    for customer in sorted_customer_choice:
        if customer in rejected_customers:
            continue
        if(sorted_customer_choice[customer][i] == 1):
            likes += 1
        elif sorted_customer_choice[customer][i] == 0:
            dislikes += 1
        else:
            neutral += 1
    
    decision = 0
    if likes >= dislikes: #forming a decision on whether or not to have that ingredient
        decision = 1

    for customer in sorted_customer_choice:
        if sorted_customer_choice[customer][i] == decision or sorted_customer_choice[customer][i] == -1:
            pass
        elif not customer in rejected_customers:
            rejected_customers.append(customer)
    # print(likes)
    # print(dislikes)

    
print(score)