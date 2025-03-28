from datetime import datetime
from stops_enum import StopsEnum


def get_option():
    while True:
        option = input("Enter option (1 - for path optimizing or 2 - for commivoy): ")
        if option in {"1", "2"}:
            return option
        print("Invalid option. Please enter 1 or 2.")

def get_argument():
    while True:
        arg = input("Enter argument (t or p): ")
        if arg in {"t", "p"}:
            return arg
        print("Invalid argument. Please enter t or p.")

def get_args(option):
    arg1 = input("Enter start argument: ")
    if option == "1":
        arg2 = input("Enter end argument: ")  # Single value
    else:
        arg2 = input("Enter L argument (comma-separated list): ").split(',')  # List
    arg3 = input("Enter start time argument: ")
    return arg1, arg2, arg3

def main():
    option = get_option()
    arg = get_argument()
    args = get_args(option)
    
    if option == "2":
        from tabu_search import tabu_search
        start = StopsEnum(args[0]).value
        L = [StopsEnum(stop).value for stop in args[1]]
        start_time = datetime.strptime(args[2], "%H:%M:%S")
        tabu_search(start, L, start_time, minimize=arg)
    else:
        start = StopsEnum(args[0]).value
        end = StopsEnum(args[1]).value
        start_time = datetime.strptime(args[2], "%H:%M:%S")
        if arg == "p":
            from A_star_stops_minimizer import A_star_stops
            A_star_stops(start, end, start_time)
        else:
            from algo import A_star
            A_star(start, end, start_time)

if __name__ == "__main__":
    main()