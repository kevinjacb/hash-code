import math

with open("d_difficult.in.txt",'r',encoding='utf-8') as f:
    file_data = f.read()

file_data = file_data.split('\n')

# print(file_data)

total_customers = int(file_data[0]) #total customers
customer_choice = dict() # preference dipicted in trinary form XD for eg : (cheese, eggs, chicken, mayo, mustard sauce): 1,0,1,1,-1,0 where -1 represents dont care and 0 represents dislike
ingredients = dict()

ingredient_count = 0

liked_ingredients = dict()
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


max_score = 0
for i in range(ingredient_count):
    rejected_customers = []
    score = 0
    for j in range(i,ingredient_count):
        rejected = len(rejected_customers)
        # print(rejected)
        score = total_customers - rejected
        likes = 0
        dislikes = 0
        neutral = 0
        for customer in customer_choice:
            if customer in rejected_customers:
                continue
            if(customer_choice[customer][j] == 1):
                likes += 1
            elif customer_choice[customer][j] == 0:
                dislikes += 1
            else:
                neutral += 1
        
        decision = 0
        if likes >= dislikes: #forming a decision on whether or not to have that ingredient
            decision = 1

        for customer in customer_choice:
            if customer_choice[customer][j] == decision or customer_choice[customer][j] == -1:
                pass
            elif not customer in rejected_customers:
                rejected_customers.append(customer)
        # print(likes)
        # print(dislikes)
    for j in range(0,i):
        rejected = len(rejected_customers)
        # print(rejected)
        score = total_customers - rejected
        likes = 0
        dislikes = 0
        neutral = 0
        for customer in customer_choice:
            if customer in rejected_customers:
                continue
            if(customer_choice[customer][(i-1)-j] == 1):
                likes += 1
            elif customer_choice[customer][(i-1)-j] == 0:
                dislikes += 1
            else:
                neutral += 1
        
        decision = 0
        if likes >= dislikes:
            decision = 1

        for customer in customer_choice:
            if customer_choice[customer][(i-1)-j] == decision or customer_choice[customer][j] == -1:
                pass
            else:
                rejected_customers.append(customer)
    if score > max_score:
        max_score = score
    
    


print(max_score)