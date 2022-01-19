file_name = "b_basic"
with open(file_name+".in.txt",'r',encoding='utf-8') as f:
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

def sort(data):
    if(data[1][1] == 0):
        return (data[1][0] + data[1][2])
    return (data[1][0]+data[1][2])/(data[1][1] + data[1][2])

ingredient_likes_dislikes = dict()

for i in range(ingredient_count):
    ingredient_likes_dislikes[i] = [0,0,0]

# print(customer_choice)
for customer in customer_choice:
    for i in range(ingredient_count):
        if customer_choice[customer][i] == 1:
            ingredient_likes_dislikes[i][0] += 1
        elif customer_choice[customer][i] == 0:
            ingredient_likes_dislikes[i][1] += 1
        else:
            ingredient_likes_dislikes[i][2] += 1

# print(ingredient_likes_dislikes)
sorted_likes_dislikes = dict()
for x,y in sorted(ingredient_likes_dislikes.items(),key=sort,reverse=True):
    sorted_likes_dislikes[x] = y
# print(sorted_likes_dislikes)

score = 0
dual_possibilities = []
dual_possibilities_rejected = []
ingredient_order = []
for i in sorted_likes_dislikes:
    ingredient_order.append(i)

def get_result(dual_possibility,flag = False):
    invert = False
    rejected_customers = []
    start = 0
    choices = dict()
    # print(ingredient_order)
    if flag:
        rejected_customers = dual_possibility[1]
        start = dual_possibility[2]
        invert = dual_possibility[6]
    for i in range(start,len(ingredient_order)):
        if invert:
            x = len(ingredient_order) - int(i/2)-1
        else:
            x = int(i/2)
        rejected = len(rejected_customers)
        global score
        global dual_possibilities
        score = total_customers - rejected
        likes = dislikes = neutral = 0
        # print(rejected_customers)
        for customer in customer_choice:
            # print(customer)
            if customer in rejected_customers:
                continue
            if(customer_choice[customer][ingredient_order[x]] == 1):
                likes += 1
            elif customer_choice[customer][ingredient_order[x]] == 0:
                dislikes += 1
            else:
                neutral += 1
        
        decision = 0
        if likes >= dislikes and not flag: #forming a decision on whether or not to have that ingredient
            decision = 1
            if likes == dislikes:
                dual_possibilities.append([ingredient_order[x],list(rejected_customers),i,likes,dislikes,neutral,invert])  
                # print(dual_possibilities)
        elif ingredient_order[x] == dual_possibility[0] and  flag:
            pass
        elif likes >= dislikes and flag:
            decision = 1

        for customer in customer_choice:
            if customer_choice[customer][ ingredient_order[x]] == decision or customer_choice[customer][ ingredient_order[x]] == -1:
                pass
            elif not customer in rejected_customers:
                rejected_customers.append(customer)
        # print(decision, end = "")
        invert = not invert
        choices[ingredient_order[x]] = decision
    return choices

first_choice = get_result([0],False)


max_score = 0
final_choice = dict()
if score > max_score:
    max_score = score
for i in dual_possibilities:
    choices = get_result(dual_possibility=i,flag=True)
    if(score > max_score):
        max_score = score
        final_choice = choices

total_ingredients = 0

for i in first_choice:
    if i in final_choice:
        pass
    else:
        final_choice[i] = first_choice[i]
    if final_choice[i] == 1:
        total_ingredients += 1
ingredients = dict(map(reversed,ingredients.items()))
# print(ingredients)

with open(file_name+"_output.txt",'w',encoding='utf-8') as f:
    f.write(str(total_ingredients))
    for i in final_choice:
        if final_choice[i] == 1:
            f.write(" "+ingredients[i])

print(max_score)