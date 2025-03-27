from datetime import datetime, timedelta
from functools import reduce
from random import shuffle
import random 
from algo import A_star
from stops_enum import StopsEnum

def tabu_search(start, L, start_time):
    LIMIT = 3
    results = []
    prev_cost = timedelta(days=1000)
    tabu = []
    best_results = list(L)
    best_cost = timedelta(days=1000)
    for _ in range(LIMIT):
        results.append(A_star(start, L[0], start_time))
        for i in range(1, len(L)):
            results.append(A_star(L[i-1], L[i], results[-1][-1]))
        results.append(A_star(L[-1], start, results[-1][-1]))
        for r in results:
            print(r[-1])
        cost = results[-1][-1] - start_time
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