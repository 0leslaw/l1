from datetime import datetime, timedelta
from functools import reduce
from random import shuffle
import random 
from algo import A_star
from A_star_stops_minimizer import A_star_stops
from stops_enum import StopsEnum

def tabu_search(start, L, start_time, minimize="t"):
    LIMIT = 3
    results = []
    prev_cost = datetime(year=2000, month=1, day=1) if minimize == "t" else float("inf")
    tabu = []
    best_results = list(L)
    best_cost = datetime(year=2000, month=1, day=1) if minimize == "t" else float("inf")
    travel_function = A_star if minimize == "t" else A_star_stops
    for _ in range(LIMIT):
        results.append(travel_function(start, L[0], start_time))
        for i in range(1, len(L)):
            results.append(travel_function(L[i-1], L[i], results[-1][-1]))
        results.append(travel_function(L[-1], start, results[-1][-1]))
        for r in results:
            print(r[-1])
        cost = results[-1][-1]
        print(cost)
        results = []
        if cost < prev_cost:
            prev_cost = cost
            if len(tabu) > 0:
                tabu.pop(-1)
                
        if cost < best_cost:
            best_cost = cost
            best_results = list(L)
        
        switched = (0, 1)
        while switched in tabu:
            switched = (random.randint(0, len(L)-1), random.randint(0, len(L)-1))
            while switched[0] == switched[1]:
                switched = (random.randint(0, len(L)-1), random.randint(0, len(L)-1))
        
        tabu.append(switched)
        L[switched[0]], L[switched[1]] = L[switched[1]], L[switched[0]]
        if len(tabu) > len(L):
            tabu.pop(0)
                
        # print(L, cost)
                
    print(best_results, best_cost)
    
if __name__ == "__main__":
    tabu_search(StopsEnum.PL_GRUNWALDZKI.value, [StopsEnum.WOJNOW.value, StopsEnum.RYNEK.value, StopsEnum.EPI.value, StopsEnum.KAMIENSKIEGO.value], datetime.strptime("14:30:00", "%H:%M:%S"))