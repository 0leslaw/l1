import networkx as nx
import pandas as pd
from datetime import datetime
import pickle
import os


"""Index(['Unnamed: 0', 'company', 'line', 'departure_time', 'arrival_time',
       'start_stop', 'end_stop', 'start_stop_lat', 'start_stop_lon',
       'end_stop_lat', 'end_stop_lon'],
      dtype='object')"""

def load_into_G(*fields_added_to_nodes):
    if os.path.exists("A_star_graph.pkl"):
        with open("A_star_graph.pkl", 'rb') as file:
            G = pickle.load(file)
        return G
    
    df = pd.read_csv("data.csv")   
    df.rename(inplace=True, columns={"Unnamed: 0": "key"})
    G = nx.MultiDiGraph()
    
    stops = set(df["start_stop"]) | set(df["end_stop"])
    # pick some stop location
    stops2locations = {}
    for stop in stops:
        df1 = df.loc[df["start_stop"] == stop]
        if df1.empty:
            df1 = df.loc[df["end_stop"] == stop]
            G.add_node(stop, **{field: 0 for field in fields_added_to_nodes},lat=df1.iloc[0]["end_stop_lat"], lon=df1.iloc[0]["end_stop_lon"])
        else:
            G.add_node(stop, **{field: 0 for field in fields_added_to_nodes}, lat=float(df1.iloc[0]["start_stop_lat"]), lon=float(df1.iloc[0]["start_stop_lon"]))
    
    for id, row in df.iterrows():
        G.add_edge(
            row["start_stop"],
            row["end_stop"], 
            **{
                k: conditional_to_datetime(k, v)
                for k, v in row.items() if k not in ["start_stop", "end_stop"]
            },
        )
    print(G.edges("Sołtysowicka", keys=True, data=True), G.nodes["Sołtysowicka"] )
    with open("A_star_graph.pkl", 'wb') as file:
        pickle.dump(G, file)
        
    return G

def conditional_to_datetime(name, value):
    if name not in ["departure_time", "arrival_time"]:
        return value
    
    fst_two = int(value[:2])
    modded = fst_two % 24
    return datetime.strptime(str(modded) + value[2:], "%H:%M:%S")

if __name__ == "__main__":
    load_into_G()