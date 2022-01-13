import math

input_file = "a.txt"

with open(input_file, "r", encoding="utf-8") as f:
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
intersection_time = dict()
cars_through_intersection = dict()

cars_through_street = dict() #contains the number of cars that goes through a street into the corresponding intersection
street_last_car_time = dict() #contains the time of the last car that passes through this in an ideal case

traffic_states = dict() #dict ( intersection : [street,traffic time]))
car_freq = dict()
has_schedule = dict() #contains number of streets if an intersection has a schedule

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
    has_schedule[i] = 0
    in_streets = []
    intersection_time[i] = 0
    cars_through_intersection[i] = 0
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


for car in car_paths:
    if intersection_time[intersection_in[car[1]]] == 0:
        intersection_time[intersection_in[car[1]]] = 1 
    curr_time = 0
    cars_through_intersection[intersection_in[car[1]]] += 1
    for i in range(2,len(car)):
        curr_time += int(street_des_dict[car[i]][3])
        if curr_time > intersection_time[intersection_in[car[i]]]:
            intersection_time[intersection_in[car[i]]] = curr_time
        if i < len(car) -1:
            cars_through_intersection[intersection_in[car[i]]] += 1

for street in street_des:
    cars_through_street[street[2]] =0
    street_last_car_time[street[2]] = 1

for car in car_paths:
    time = 1
    for street in range(1,len(car)-1):
        if street != 1:
            time += int(street_des_dict[car[street]][3])
        cars_through_street[car[street]] += 1
        if street_last_car_time[car[street]] < time:
            street_last_car_time[car[street]] = time 
            
for street in street_des:
    car_freq[street[2]] = math.ceil(cars_through_street[street[2]]/street_last_car_time[street[2]])

for freq in car_freq:
    if(car_freq[freq] > 0):
        has_schedule[intersection_in[freq]] += 1

intersection_with_schedule = []

with open("output.txt",'w',encoding='utf-8') as f:
    counter = 0
    for i in range(int(intersections)):
        if has_schedule[i] > 0:
            counter+=1
            intersection_with_schedule.append(i)
    f.write(str(counter)+"\n")
    for i in intersection_with_schedule:
        f.write(str(i)+"\n")
        f.write(str(has_schedule[i])+"\n")
        for freq in car_freq:
            if intersection_in[freq] == i:
                f.write(freq+ " "+str(car_freq[freq])+"\n")

# print(street_des)
# print(intersection_in)
# print(cars_through_street)
# print(street_last_car_time)
# print(car_freq)
# print(has_schedule)
