with open("a.txt", "r", encoding="utf-8") as f:
    data = f.read()

input = data.split("\n")
# print(input)

map_deets = input[0].split(" ")

duration = map_deets[0] #contains the time limit of the simulation
intersections = map_deets[1] 
streets = map_deets[2]
cars = map_deets[3]
points = map_deets[4]

line_count = len(input)
street_des = [] #contains only the deets of the streets including time and intersection deets from the original file

street_des_dict = dict() #contains the deets of the streets in a dictionary form to be able to access it by entering the street name...
intersection_out = dict() #contains all the outgoing street from an intersection in the format : (intersection_no : [street_name(s)])
intersection_in = dict() #contains all the entering street in an intersection( ones with the traffic lights) in the format : (street_name : intersection_no)
travel_time = dict()   #contains the total time taken by each car

active_intersections = dict() #contains all the active intersections or intersections through which cars are passing/should pass at a given instant

traffic_state = dict() # contains the states of the traffic lights at each intersection in a dictionary form of type : (intersection_name:[traffic_states])

car_paths = [] #contains the deets of each car in a list, this is later sorted in the descending order of total time taken by each car in an ideal case...

path_flag = 0 #no idea what this does

for i in range(1, line_count):
    data = input[i].split(" ")
    if not data[1].isdigit():
        path_flag = i
        break
    street_des.append(data)


for street in street_des:
    street_des_dict[street[2]] = street

for i in range(path_flag, line_count - 1):
    data = input[i].split(" ")
    car_paths.append(data)


def key(elem):
    return elem[0]


for i in range(int(intersections)):
    out_streets = []
    in_streets = []
    for street in street_des:
        if int(street[0]) == i:
            out_streets.append(street[2])
        if int(street[1]) == i:
            in_streets.append(street[2])
    for street in in_streets:
        intersection_in[street] = i
    intersection_out[i] = out_streets


for i, car in enumerate(car_paths):
    time = 0
    for x in range(2, len(car)):
        time += int(street_des_dict[car[x]][3])
    travel_time[i] = time

car_paths = [paths for _, paths in sorted(zip(travel_time, car_paths))]

for i, car in enumerate(car_paths):
    active_intersections[car[1]] = i

for i in range(len(intersection_out)):
    traffic_state[i] = [0] * len(intersection_out[i])

print(traffic_state)
print(intersection_in)
