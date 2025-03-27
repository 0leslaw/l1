from datetime import datetime, timedelta
import pandas as pd
import re
from constants import lon_deg, lat_deg
from utils import lon_lat_to_d
from graph_creation import load_into_G

def main():
    df = pd.read_csv("data.csv")
    print(df.columns)
    for col in df.columns:
        print(col, df[col].unique())

def make_enum_file():
    df = pd.read_csv("data.csv")
    stops = set(df["start_stop"]) | set(df["end_stop"])
    name2sripped = {}
    for stop in stops:
        name2sripped[stop] = stop.replace(" ", "_").replace("ą", "a").replace("ę", "e").replace("ł", "l").replace("ó", "o").replace("ś", "s").replace("ż", "z").replace("ź", "z").replace("ć", "c").replace("ń", "n").replace(".","_").replace(",","_").replace("-","_").replace("(","_").replace(")","_").replace("/","_").replace("ł", "l").replace("Ł", "L").replace("ń", "n").replace("Ń", "N").replace("ś", "s").replace("Ś", "S").replace("ź", "z").replace("Ź", "Z").replace("ż", "z").replace("Ż", "Z").replace("ć", "c").replace("Ć", "C").replace("ą", "a").replace("Ą", "A").replace("ę", "e").replace("Ę", "E").replace("ó", "o").replace("Ó", "O")
        name2sripped[stop] = reduce_repeated_char(name2sripped[stop], "_")
        name2sripped[stop] = name2sripped[stop].upper()
        
    if len(name2sripped.values()) != len(set(name2sripped.values())):
        print("Error: not all stops are unique")
    else:
        print(name2sripped.values())
    
    # create the file:
    with open("stops_enum.py", "w", encoding="utf-8") as f:
        f.write("from enum import Enum\nclass StopsEnum(Enum):\n")
        for stop, stripped in name2sripped.items():
            f.write(f"    {stripped}= \"{stop}\"\n")
        f.write("\n")
        
def reduce_repeated_char(s, char):
    pattern = f"{re.escape(char)}+"
    return re.sub(pattern, char, s)
    
    
def test_datetime():
    d1 = datetime.strptime("23:00:00", "%H:%M:%S")
    d1 = d1.replace(day=1)
    d2 = datetime.strptime("1:00:00", "%H:%M:%S")
    d2 = d2.replace(day=d1.day + 1)
    
    print(d2 < d1 + timedelta(hours=2))
    
def find_biggest_vel():
    
    G = load_into_G("h", "g", "came_by_edge", "came_from_node")
    max_vel = float("-inf") # km/h
    mean_vel = 0
    vels= 0
    for node in G.nodes:
        edges = G.out_edges(node, keys=True, data=True)
        for o, t, k, data in edges:
            vels += 1
            d = lon_lat_to_d(G, o, t)
            
            departure_time = data["departure_time"]
            arrival_time = data["arrival_time"] 
            if departure_time == arrival_time:
                print(o, t, k, "SAME!")
                continue
            if arrival_time < departure_time:
                arrival_time.replace(day=arrival_time.day+1)
                
            dt = arrival_time - departure_time
            total_hours = dt.total_seconds() / 3600
            vel = d/total_hours
            mean_vel += vel
            max_vel = max(vel, max_vel)
    mean_vel /= vels
    with open("max_vel.txt", "w") as f:
        f.write(f"max velocity = {max_vel}\nmean vel = {mean_vel}")
        

def checkout_edge(o, t, id):
    G = load_into_G()
    e = G.get_edge_data(o, t, id)
    print(e)
    
if __name__ == "__main__":
    # make_enum_file()
    
    # main()
    # test_datetime()
    find_biggest_vel()
    # checkout_edge("Poprzeczna", "Redycka", 559839)
    