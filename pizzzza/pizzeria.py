with open("c_coarse.in.txt",'r',encoding='utf-8') as f:
    file_data = f.read()

file_data = file_data.split('\n')

print(file_data)

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

x = pow(2,ingredient_count)

for i,file in enumerate(file_data):
    file = file.split(" ")
    if(i % 2 == 1 or  i == 0):
        preference = [-1]*ingredient_count
    for ingredient in file:
        if not ingredient.isdigit():
            if(i % 2 == 0 and not i is 0):
                preference[ingredients[ingredient]] = 0
            elif not i is 0:
                preference[ingredients[ingredient]] = 1
    customer_choice[int((i-1)/2)] = preference 

max_score = 0
flag = True
for i in range(x):
    score = 0
    binary = list(format(i,'b'))
    for customer in customer_choice:
        for i,bit in enumerate(binary):
            if customer_choice[customer][i] is int(bit):
                pass
            elif customer_choice[customer][i] == -1:
                pass
            else:
                flag = False
        if flag:
            score += 1
        flag = True
    if score > max_score:
        max_score = score

print(ingredients) 
print(max_score)