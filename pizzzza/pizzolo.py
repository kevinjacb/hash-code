import time #tmp
import utils
import random

in_files = ['a_an_example', 'b_basic', 'c_coarse', 'd_difficult', 'e_elaborate']

in_fname = in_files[3]
in_file = open(in_fname + '.in.txt')

start = time.time()
num_clients, likes, dislikes = utils.parse_file(in_file)
# Get the set of all ingredients
ingredients = set()
for like in likes:
    ingredients.update(like[1])
for dislike in dislikes:
    ingredients.update(dislike[1])
num_ingredients = len(ingredients)
end = time.time()
print(f"Parsed input in {end - start}s")

ing_dict = {}
ctr = 0
for like, dislike in zip(likes, dislikes):
    for ing in like[1]:
        if ing in ing_dict:
            ing_dict[ing]['like'][0] += 1
            ing_dict[ing]['like'][1].append(ctr)
            ing_dict[ing]['score'] += 1 / like[0]
        else:
            ing_dict[ing] = {'like': [1, [ctr]], 'dislike': [0, []], 'score': 1}
    for ing in dislike[1]:
        if ing in ing_dict:
            ing_dict[ing]['dislike'][0] += 1
            ing_dict[ing]['dislike'][1].append(ctr)
            ing_dict[ing]['score'] -= 1 / dislike[0]
        else:
            ing_dict[ing] = {'like': [0, []], 'dislike': [1, [ctr]], 'score': -1}
    ctr += 1



def random_ings(num_ings):
    chosen_ings = set()
    for i, ing in enumerate(ingredients):
        if i < num_ings:
            chosen_ings.add(ing)
        else:
            break
    return chosen_ings

def best_weighted_ings():
    ingredient_list = list(ingredients)
    ingredient_list.sort(key=lambda x: ing_dict[x]['score'],reverse=True)
    best_chosen_ings = set()

    client_states = {i: likes[i][0] for i in range(num_clients)}
    best_score = -1
    chosen_ings = set()
    score = 1
    for i in range(num_ingredients):
        chosen_ings.add(ingredient_list[i])
        # Update score after adding current ingredient
        for liker in ing_dict[ingredient_list[i]]['like'][1]:
            if client_states[liker] > 0:
                client_states[liker] -= 1
                if client_states[liker] == 0:
                    score += 1
        for disliker in ing_dict[ingredient_list[i]]['dislike'][1]:
            if client_states[disliker] == 0:
                score -= 1
            client_states[disliker] = -1

        if score > best_score:
            best_score = score
            best_chosen_ings.update(chosen_ings)
    return best_chosen_ings

def brute_n_weight():
    ingredient_list = list(ingredients)
    ingredient_list.sort(key=lambda x: ing_dict[x]['score'],reverse=True)
    client_states = {i: likes[i][0] for i in range(num_clients)}
    best_score = -1
    chosen_ings = set()
    best_chosen_ings = set()
    score = 1
    best_index = 0
    for i in range(num_ingredients):
        chosen_ings.add(ingredient_list[i])
        # Update score after adding current ingredient
        for liker in ing_dict[ingredient_list[i]]['like'][1]:
            if client_states[liker] > 0:
                client_states[liker] -= 1
                if client_states[liker] == 0:
                    score += 1
        for disliker in ing_dict[ingredient_list[i]]['dislike'][1]:
            if client_states[disliker] == 0:
                score -= 1
            client_states[disliker] = -1

        if score > best_score:
            best_score = score
            best_index = i
            best_chosen_ings.update(chosen_ings)
    return best_index, best_score
        

def gray_brute(num_iter):
    ingredient_list = list(ingredients)
    ingredient_list.sort(key=lambda x: ing_dict[x]['score'],reverse=True)

    log_2_lookup = {2**i: i for i in range(num_ingredients)}
    gray_i = 0
    client_state = [[like[0], 0] for like in likes]
    bindex, score = brute_n_weight()
    for i in range(bindex + 1):
        for liker in ing_dict[ingredient_list[i]]['like'][1]:
            client_state[liker][0] -= 1
        for disliker in ing_dict[ingredient_list[i]]['dislike'][1]:
            client_state[liker][1] += 1

    best_score = score
    for i in range(1, min(num_iter, 2**num_ingredients)):
        gray_i = i ^ (i >> 1)
        prev_gray_i = (i - 1) ^ ((i - 1) >> 1)
        change = log_2_lookup[gray_i ^ prev_gray_i]
        if change > bindex:
            print("broken")
        if gray_i >> change & 1:
            # Add
            new_ing = ingredient_list[num_ingredients - 1 - change] 
            for liker in ing_dict[new_ing]['like'][1]:
                client_state[liker][0] -= 1
                if client_state[liker] == [0, 0]:
                    score += 1
            for disliker in ing_dict[new_ing]['dislike'][1]:
                if client_state[disliker] == [0, 0]:
                    score -= 1
                client_state[disliker][1] += 1
        else:
            # Remove
            removed_ing = ingredient_list[num_ingredients - 1 - change] 
            for liker in ing_dict[removed_ing]['like'][1]:
                if client_state[liker] == [0, 0]:
                    score -= 1
                client_state[liker][0] += 1
            for disliker in ing_dict[removed_ing]['dislike'][1]:
                client_state[disliker][1] -= 1
                if client_state[disliker] == [0, 0]:
                    score += 1
        if score > best_score:
            best_score = score
            print(f"New best score: {best_score}")



def genetic_recipe(num_gens, pop_size):
    pass

start = time.time()
chosen_ings = gray_brute(10**9)
end = time.time()
print(f"Processed in {end - start}s")
# start = time.time()
# score = utils.evaluate(chosen_ings, likes, dislikes)
# end = time.time()
# print(f"Score: {score}\nEvaluated in {end - start}s")