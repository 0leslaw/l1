from datetime import datetime, timedelta
import heapq
from graph_creation import load_into_G
from utils import best_edge_and_cost, time_of_arrival_at_stop_in_current_best_path, get_edges, get_result_edges
from stops_enum import StopsEnum

def dijkstra(start, end, t, max_wait_time_hours=1):
    G = load_into_G()
    
    # Use a priority queue to efficiently get the node with the minimum cost
    priority_queue = []
    
    for node in G.nodes():
        G.nodes[node]["min_cost"] = timedelta(days=1000)
        G.nodes[node]["visited"] = False
        G.nodes[node]["came_by_edge"] = None
        G.nodes[node]["came_from_node"] = None

    G.nodes[start]["min_cost"] = timedelta(0)
    heapq.heappush(priority_queue, (timedelta(0), start))

    while priority_queue:
        # Get the node with the smallest cost
        current_cost, min_node = heapq.heappop(priority_queue)
        
        if G.nodes[min_node]["visited"]:
            continue

        # Mark as visited
        G.nodes[min_node]["visited"] = True
        
        if min_node == end:
            break  # Stop early if we reached the destination

        current_time = time_of_arrival_at_stop_in_current_best_path(G, min_node) if min_node != start else t

        successors = G.successors(min_node)
        for succ in successors:
            edges = get_edges(G, min_node, succ)
            best_edge, best_cost = best_edge_and_cost(edges, max_wait_time_hours, current_time)
            
            if best_cost + G.nodes[min_node]["min_cost"] < G.nodes[succ]["min_cost"]:
                G.nodes[succ]["min_cost"] = best_cost
                G.nodes[succ]["came_by_edge"] = best_edge
                G.nodes[succ]["came_from_node"] = min_node
                
                heapq.heappush(priority_queue, (best_cost, succ))
    
    return get_result_edges(G, start, end)

    
    
if __name__ == "__main__":
    dijkstra(StopsEnum.POPRZECZNA.value, StopsEnum.PL_GRUNWALDZKI.value, datetime.strptime("12:00:00", "%H:%M:%S"))