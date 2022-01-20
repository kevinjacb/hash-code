import time #tmp
import utils
from tqdm import tqdm

in_files = ['a_an_example', 'b_basic', 'c_coarse', 'd_difficult', 'e_elaborate']

in_fname = in_files[4]
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

def half_brute(threshold=0, max_iter=num_ingredients):
    best_ings = set()
    ingredient_list = list(ingredients)
    ingredient_list.sort(key=lambda x: ing_dict[x]['score'], reverse=True)
    best_score = 0
    pbar = tqdm(range(min(max_iter, num_ingredients)))
    for t in pbar:
        pbar.set_description(f'Best score: {best_score}')
        score = 0
        likes_cpy = {i: [s[0], s[1].copy()] for i, s in enumerate(likes)}
        dislikes_cpy = {i: [s[0], s[1].copy()] for i, s in enumerate(dislikes)}
        chosen_ings = set()
        var_ing_dict = dict()
        for x in ing_dict:
            var_ing_dict[x] = dict()
            var_ing_dict[x]['score'] = ing_dict[x]['score']
            var_ing_dict[x]['like'] = [ing_dict[x]['like'][0], ing_dict[x]['like'][1].copy()]
            var_ing_dict[x]['dislike'] = [ing_dict[x]['dislike'][0], ing_dict[x]['dislike'][1].copy()]
        client_states = {i: 0 for i in range(num_clients)}

        for i in range(t, num_ingredients + t):
            current_ing = ingredient_list[i % num_ingredients]
            current_weight = 0
            for liker in var_ing_dict[current_ing]['like'][1]:
                current_weight += 1 / likes_cpy[liker][0]
            for disliker in var_ing_dict[current_ing]['dislike'][1]:
                current_weight -= 1 / dislikes_cpy[disliker][0]
            # Add ingredient
            if current_weight > threshold:
                chosen_ings.add(current_ing)
                # For every client that likes the ing, remove the
                # ing from their likes and reduce their count of liked ings
                for liker in var_ing_dict[current_ing]['like'][1]:
                    likes_cpy[liker][0] -= 1
                    likes_cpy[liker][1].remove(current_ing)

                    if likes[liker][0] > client_states[liker] >= 0:
                        client_states[liker] += 1
                        if client_states[liker] == likes[liker][0]:
                            score += 1

                # For every client that dislikes the ing, remove the client
                # from the likers/dislikers list of every other ing they like/dislike.
                # Then remove the client.
                for disliker in var_ing_dict[current_ing]['dislike'][1]:
                    dislikes_cpy[disliker][0] -= 1
                    dislikes_cpy[disliker][1].remove(current_ing)
                    for ing in dislikes_cpy[disliker][1]:
                        var_ing_dict[ing]['dislike'][0] -= 1
                        var_ing_dict[ing]['dislike'][1].remove(disliker)
                    for ing in likes_cpy[disliker][1]:
                        var_ing_dict[ing]['like'][0] -= 1
                        var_ing_dict[ing]['like'][1].remove(disliker)
                    if likes[disliker][0] == client_states[disliker]:
                        score -= 1
                    del dislikes_cpy[disliker]
            # Skip ingredient
            else:
                # For every client that liked the ing, remove the client 
                # from the likers/dislikers list of every other ingredient they like and dislike.
                # Then remove the client
                for liker in var_ing_dict[current_ing]['like'][1]:
                    likes_cpy[liker][0] -= 1
                    likes_cpy[liker][1].remove(current_ing)
                    for ing in likes_cpy[liker][1]:
                        var_ing_dict[ing]['like'][0] -= 1
                        var_ing_dict[ing]['like'][1].remove(liker)
                    for ing in dislikes_cpy[liker][1]:
                        var_ing_dict[ing]['dislike'][0] -= 1
                        var_ing_dict[ing]['dislike'][1].remove(liker)
                    del likes_cpy[liker]
                # For every client that dislikes the ing, reduce their dislike count 
                # by one and remove the ingredient from their disliked set
                for disliker in var_ing_dict[current_ing]['dislike'][1]:
                    dislikes_cpy[disliker][0] -= 1
                    dislikes_cpy[disliker][1].remove(current_ing)
            
            if score > best_score:
                best_score = score
                best_ings = chosen_ings.copy()
    return best_ings

start = time.time()
chosen_ings = half_brute(0.0, 10000)
end = time.time()
print(f"Processed in {end - start}s")
start = time.time()
score = utils.evaluate(chosen_ings, likes, dislikes)
end = time.time()
print(f"Judge's score: {score}\nEvaluated in {end - start}s")