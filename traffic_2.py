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

print(intersections)