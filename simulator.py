from typing import Any
import traffic as rd


input = ""

time_elapsed = 0 #contains the total time elapsed for each car during each iteration

queue = dict() #contains the number of cars(if any) with the time at which it is queued

with open("output.txt",'r',encoding='utf-8') as f:
    input = f.read()


input = input.split("\n")

for street in rd.street_des:
    queue[street[2]] = [0]*int(rd.duration )#contains no of cars at every second of the duration

car_freq_elapsed = dict() #contains the traffic state timings of a street at its respective intersection

for i in range(int(rd.intersections)):
    elapsed = 0
    for freq in rd.car_freq:
        if rd.intersection_in[freq] == i:
            car_freq_elapsed[freq] = [0,0]
            car_freq_elapsed[freq][0] = elapsed
            elapsed += rd.car_freq[freq]
            car_freq_elapsed[freq][1] = elapsed

print(car_freq_elapsed)


# print(street_des)
# print(intersection_in)
# print(cars_through_street)
# print(street_last_car_time)
# print(car_freq)
# print(has_schedule)

intersection_cycle_time = dict()
for i in range(int(rd.intersections)):
    intersection_cycle_time[i] = 0

for i in rd.car_freq:
    intersection_cycle_time[rd.intersection_in[i]] += rd.car_freq[i]

print(intersection_cycle_time)
print(rd.car_paths)


def waiting_time_intersection(current_street,elapsed_time, queued_cars, time_period, cycle ):
    time_within_bounds = elapsed_time % cycle # maps the elapsed time to within the range of cycle
    total_time = 0 
    time_on = time_period[1] - time_period[0] #time for which the light is green
    time_off = cycle - time_on #time for which the light is red
    time_left = time_period[1] - time_within_bounds #time left for which light is green
    if time_within_bounds >= time_period[0] and time_within_bounds < time_period[1]:
        if queued_cars is 0:
            return total_time
        else:
            queue[current_street][elapsed_time] += 1
            if queued_cars <= time_left:
                for i in range(queued_cars):
                    queue[current_street][elapsed_time+i + 1] = queue[current_street][elapsed_time] - i - 1
                total_time += queued_cars
                return total_time
            else:
                elapsed_time_dup = elapsed_time
                cars_left = queued_cars - time_left
                total_time += time_left + time_off
                while(cars_left > time_on):
                    total_time += cycle
                    car_when_red = 0
                    for i in range(1,cycle+1):
                        if(i <= time_on):
                            queue[current_street][elapsed_time_dup+i] = cars_when_red= queue[current_street][elapsed_time_dup] - i
                        else:
                            queue[current_street][elapsed_time_dup+i] = cars_when_red
                    cars_left -= time_on
                    elapsed_time_dup += cycle
                total_time += cars_left
                return total_time
    else:
        elapsed_time_dup = elapsed_time
        queue[current_street][elapsed_time]+=1
        total_time += cycle - time_within_bounds
        cars_left = queued_cars
        while(cars_left > time_on):
            total_time += cycle
            car_when_red = 0
            for i in range(1,cycle+1):
                if(i <= time_on):
                    queue[elapsed_time_dup+i] = cars_when_red= queue[elapsed_time_dup] - i
                else:
                    queue[elapsed_time_dup+i] = cars_when_red
            cars_left -= time_on
            elapsed_time_dup += cycle
        total_time += cars_left
        return total_time

total_points = 0
for car in rd.car_paths:
    time_elapsed = 0 
    time_elapsed += waiting_time_intersection(car[1],time_elapsed,queue[car[1]][time_elapsed],car_freq_elapsed[car[1]],intersection_cycle_time[rd.intersection_in[car[1]]]) 
    for i in range(2,len(car)):
        time_elapsed += int(rd.street_des_dict[car[i]][3]) 
        if time_elapsed > int(rd.duration):
            break
        if i is len(car) - 1:
            break
        time_elapsed += waiting_time_intersection(car[i],time_elapsed,queue[car[i]][time_elapsed],car_freq_elapsed[car[i]],intersection_cycle_time[rd.intersection_in[car[i]]])

    print(time_elapsed)
    if time_elapsed <= int(rd.duration):
        total_points += int(rd.points)
        total_points += int(rd.duration) - time_elapsed

print(total_points)