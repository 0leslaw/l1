
from datetime import timedelta
from datetime import datetime
from graph_creation import load_into_G
import networkx as nx
from pq import PriorityQueue
from utils import lon_lat_to_d, best_edge_and_cost, time_of_arrival_at_stop_in_current_best_path, get_edges, get_result_edges
from constants import lon_deg, lat_deg
from stops_enum import StopsEnum

def A_star(start, end, t, max_wait_time_hours=1) :
    G = load_into_G("h", "g", "came_by_edge", "came_from_node", "best_arrival_time")
    G.nodes[start]["h"] = timedelta(0)
    G.nodes[start]["g"] = timedelta(0)
    opened_ids = {start}
    closed_ids = set()
    current_time = t
    while opened_ids:
        id_best_node = None
        node_cost = timedelta(days=1000)
        for id_node_tested in opened_ids:
            a_s_cost = A_s_cost(G.nodes[id_node_tested])
            if a_s_cost < node_cost:
                node_cost = a_s_cost
                id_best_node = id_node_tested
                
        if id_best_node == end:
            return get_result_edges(G, start, end)
        
        opened_ids.remove(id_best_node)
        closed_ids.add(id_best_node)
        
        successors = G.successors(id_best_node)
        
        if id_best_node != start:
            current_time = time_of_arrival_at_stop_in_current_best_path(G, id_best_node) # important we uptade the current_time
        
        for succ in successors:
            if succ not in opened_ids and succ not in closed_ids:
                
                opened_ids.add(succ)
                # calc the costs
                # the h is easy, since it only depends on the position
                G.nodes[succ]["h"] = calc_heuristic_cost(G, succ, end)
                
                # for the g however we need to consider the time for each edge
                # edges = G.out_edges(id_best_node, succ, keys=True, data=True)
                edges = get_edges(G, id_best_node, succ)
                
                best_edge, best_cost = best_edge_and_cost(edges, max_wait_time_hours, current_time)
                G.nodes[succ]["g"] = G.nodes[id_best_node]["g"] + best_cost
                
                # its visited for the first time, so we assign the best found edge to the route
                G.nodes[succ]["came_by_edge"] = best_edge
                G.nodes[succ]["came_from_node"] = id_best_node
                
            else: 
                best_edge, best_cost = best_edge_and_cost(
                    # G.out_edges(id_best_node, succ, keys=True, data=True), 
                    get_edges(G, id_best_node, succ),
                    max_wait_time_hours, current_time)
                if G.nodes[succ]["g"] > G.nodes[id_best_node]["g"] + best_cost:
                    G.nodes[succ]["g"] = G.nodes[id_best_node]["g"] + best_cost
                    
                    G.nodes[succ]["came_by_edge"] = best_edge
                    G.nodes[succ]["came_from_node"] = id_best_node
                    
                    if succ in closed_ids:
                        opened_ids.add(succ)
                        closed_ids.add(succ)
                



def calc_heuristic_cost(G, node1_id, node2_id):
    d = lon_lat_to_d(G, node1_id, node2_id)
    # we need to use the same metric as the g cost functio (alternatively we could use some abstract metric to speedup the algo)
    hh = d / 50 #km/h
    return timedelta(hours=hh)
        
def A_s_cost(node):
    return node["h"] + node["g"]



 
if __name__ == "__main__":
    A_star(StopsEnum.POPRZECZNA.value, StopsEnum.PL_GRUNWALDZKI.value, datetime.strptime("12:00:00", "%H:%M:%S"))