
from datetime import timedelta
from datetime import datetime
from graph_creation import load_into_G, load_into_G_lines
import networkx as nx
from pq import PriorityQueue
from utils import lon_lat_to_d, best_edge_and_cost, time_of_arrival_at_stop_in_current_best_path, get_edges, get_result_edges, best_edge_and_cost_stops, get_result_edges_stops
from constants import lon_deg, lat_deg
from stops_enum import StopsEnum

def A_star_stops(start, end, filler) :
    G = load_into_G_lines()
    G.nodes[start]["h"] = 0
    G.nodes[start]["g"] = 0
    opened_ids = {start}
    closed_ids = set()
    while opened_ids:
        id_best_node = None
        node_cost = float("inf")
        for id_node_tested in opened_ids:
            a_s_cost = A_s_cost(G.nodes[id_node_tested])
            if a_s_cost < node_cost:
                node_cost = a_s_cost
                id_best_node = id_node_tested
                
        if id_best_node == end:
            return get_result_edges_stops(G, start, end)
        
        opened_ids.remove(id_best_node)
        closed_ids.add(id_best_node)
        
        successors = G.successors(id_best_node)
 
        for succ in successors:
            if succ not in opened_ids and succ not in closed_ids:
                
                opened_ids.add(succ)
                # calc the costs
                # the h is easy, since it only depends on the position
                G.nodes[succ]["h"] = calc_heuristic_cost(G, succ, end)
                
                # for the g however we need to consider the time for each edge
                # edges = G.out_edges(id_best_node, succ, keys=True, data=True)
                is_transfer, lines = is_transfer__list_of_available_lines(G, id_best_node, succ)
                G.nodes[succ]["g"] = G.nodes[id_best_node]["g"] + (0 if is_transfer else 1)
                G.nodes[succ]["current_available_stops"] = lines
                # TAKE THE STOPS INTO ACCOUNT
                
                
                # its visited for the first time, so we assign the best found edge to the route

                G.nodes[succ]["came_from_node"] = id_best_node
                
            else: 
                is_transfer, lines = is_transfer__list_of_available_lines(G, id_best_node, succ)
                if G.nodes[succ]["g"] > G.nodes[id_best_node]["g"] + (0 if is_transfer else 1):
                    G.nodes[succ]["g"] = G.nodes[id_best_node]["g"] + (0 if is_transfer else 1)
                    G.nodes[succ]["current_available_stops"] = lines

                    G.nodes[succ]["came_from_node"] = id_best_node
                    
                    if succ in closed_ids:
                        opened_ids.add(succ)
                        closed_ids.add(succ)
                



def calc_heuristic_cost(G, node1_id, node2_id):
    d = lon_lat_to_d(G, node1_id, node2_id)
    # we need to use the same metric as the g cost functio (alternatively we could use some abstract metric to speedup the algo)
    hh = d / 50 #km/h
    return hh / 100 # make an arbitrary heuristic cost for decision making
        
def is_transfer__list_of_available_lines(G, start, end):
    edge = G.get_edge_data(start, end)
    
    if "current_available_stops" in G.nodes[start]:
        curr_av_stops = G.nodes[start]["current_available_stops"]
    else:
        curr_av_stops = G.nodes[start]["all_available_lines"]
    
    av_transfers = curr_av_stops.intersection(edge["lines"])
    return bool(av_transfers), av_transfers if av_transfers else edge["lines"]
    
def A_s_cost(node):
    return node["h"] + node["g"]



 
if __name__ == "__main__":
    A_star_stops(StopsEnum.GALERIA_DOMINIKANSKA.value, StopsEnum.POPRZECZNA.value, datetime.strptime("16:30:00", "%H:%M:%S"))