def parse_file(file):
    '''
    file: a file object
    '''
    num_clients = int(file.readline())
    likes = []
    dislikes = []

    for i in range(num_clients):
        ith_likes = file.readline().split()
        ith_likes = int(ith_likes[0]), set(ith_likes[1:])
        ith_dislikes =  file.readline().split()
        ith_dislikes = int(ith_dislikes[0]), set(ith_dislikes[1:])
        likes.append(ith_likes)
        dislikes.append(ith_dislikes)
    return num_clients, likes, dislikes

def evaluate(ingredients, likes, dislikes):
    '''
    ingredients - Set of strs, set of all chosen ingredients
    likes - list of tuples. Each tuple is of the form (n, liked_ings) 
        n is the number of liked ings. liked_ings is the set of ingredients
        liked by the ith client
    dislikes - list of tuples. Each tuple is of the form (n, disliked_ings) 
        n is the number of disliked ings. disliked_ings is the set of ingredients
        disliked by the ith client
    '''
    score = 0
    for i in range(len(likes)):
        if likes[i][1].issubset(ingredients) and len(dislikes[i][1].intersection(ingredients)) == 0:
            score += 1
    return score

def fast_evaluate(chosen, likes, dislikes):
    score = 0
    for like, dislike in zip(likes, dislikes):
        if like == like & chosen and chosen & dislike == 0:
            score += 1
    return score