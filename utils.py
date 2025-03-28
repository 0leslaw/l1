from datetime import timedelta
from constants import lat_deg, lon_deg

def lon_lat_to_d(G, node1_id, node2_id):
    lat_delta = (G.nodes[node1_id]["lat"] - G.nodes[node2_id]["lat"]) * lat_deg
    lon_delta = (G.nodes[node1_id]["lon"] - G.nodes[node2_id]["lon"]) * lon_deg
    d = (lat_delta**2 + lon_delta**2)**0.5
    return d

def best_edge_and_cost(edges, max_wait_time_hours, start_time):
    nodes_best_edge = None
    nodes_best_edge_cost = timedelta(days=1000)
    for u, v, k, data in edges:
        # if the departure already took place we still want to look for it in the next day 
        departure_time = data["departure_time"]
        if departure_time < start_time:
            departure_time = departure_time.replace(day=departure_time.day+1)

        if departure_time - start_time <= timedelta(hours=max_wait_time_hours):
            # if the departure is after the arrival it clearly means the arrival is in the next day
            arrival_time = data["arrival_time"]
            if arrival_time < departure_time:
                arrival_time.replace(day=arrival_time.day+1)
                
            cost = arrival_time - start_time
            if cost < nodes_best_edge_cost:
                nodes_best_edge_cost = cost
                nodes_best_edge = k
            
    return nodes_best_edge, nodes_best_edge_cost

def best_edge_and_cost_stops(G, edges, max_wait_time_hours, start_time):
    nodes_best_edge = None
    nodes_best_dest = None
    nodes_best_line = None
    nodes_best_edge_cost = timedelta(days=1000)
    for u, v, k, data in edges:
        # if the departure already took place we still want to look for it in the next day 
        departure_time = data["departure_time"]
        if departure_time < start_time:
            departure_time = departure_time.replace(day=departure_time.day+1)

        if departure_time - start_time <= timedelta(hours=max_wait_time_hours):
            if "current_best_line" not in G.nodes[u]:
                G.nodes[v]["current_best_line"] = data["line"]
                return k, timedelta(0), None, None
            else:                
                cost = timedelta(0) if G.nodes[u]["current_best_line"] == data["line"] else timedelta(hours=10)
                if cost < nodes_best_edge_cost:
                    nodes_best_edge_cost = cost
                    nodes_best_edge = k
                    nodes_best_dest = v
                    nodes_best_line = data["line"]
    

    return nodes_best_edge, nodes_best_edge_cost, nodes_best_dest, nodes_best_line


def time_of_arrival_at_stop_in_current_best_path(G, stop_id):
    """when on the stop in each check we want to check what would be the time, we do it by taking the 
    current best edge coming to the node"""
    stop = G.nodes[stop_id]
    prev_id = stop["came_from_node"]
    edge_id = stop["came_by_edge"]
    # print(G.nodes[prev_id])
    edge = G[prev_id][stop_id][edge_id]
    return edge["arrival_time"]

def get_edges(G, origin, target):
    edge_data = G[origin][target]
    for k, data in edge_data.items():  
        yield origin, target, k, data  
        
def get_result_costs(G, start, end):
    cost = G.nodes[end]["g"]
    curr_node = end
    while curr_node != start:
        edge_data = G.get_edge_data(G.nodes[curr_node]["came_from_node"], curr_node, key=G.nodes[curr_node]["came_by_edge"])
        # print(G.nodes[curr_node]["came_from_node"], edge_data["departure_time"], edge_data["line"])
        curr_node = G.nodes[curr_node]["came_from_node"]
        cost += G.nodes[curr_node]["g"]
    # print(f"BEST EDGES: {best_edges}\n\nBEST STOPS: {stops}")
    return cost

def get_result_edges_stops(G, start, end):
    stops = [end]
    curr_node = end
    switches = G.nodes[end]["g"]
    lines = []
    # print(end)
    while curr_node != start:
        lines.append(G.nodes[curr_node]["current_available_stops"])

        curr_node = G.nodes[curr_node]["came_from_node"]
        stops.append(curr_node)
    stops = stops
    print()
    lines = get_min_lines(lines)
    for i in range(len(lines)):
        print(stops[i], lines[i])
    # print(f"BEST EDGES: {best_edges}\n\nBEST STOPS: {stops}")
    return stops, lines, switches


def get_min_lines(lines: list[set]):
    lines = lines[::-1]
    breakd = 0
    c_inters = lines[0]
    for i in range(1, len(lines)):
        if not lines[i].intersection(lines[i-1]) :
            for j in range(breakd, i):
                lines[j] = c_inters
            breakd = i
            c_inters = lines[i]
            
        else:
            c_inters = c_inters.intersection(lines[i])
    
    for j in range(breakd, len(lines)):
        lines[j] = c_inters
            
    return lines[::-1]
            
    
def get_result_edges(G, start, end):
    best_edges = []
    stops = [end]
    curr_node = end
    # print(end)
    while curr_node != start:
        edge_data = G.get_edge_data(G.nodes[curr_node]["came_from_node"], curr_node, key=G.nodes[curr_node]["came_by_edge"])
        print(G.nodes[curr_node]["came_from_node"], edge_data["departure_time"], edge_data["line"])
        best_edges.append(edge_data)
        curr_node = G.nodes[curr_node]["came_from_node"]
        stops.append(curr_node)
    best_edges = best_edges
    stops = stops
    print()
    # print(f"BEST EDGES: {best_edges}\n\nBEST STOPS: {stops}")
    return best_edges, stops, time_of_arrival_at_stop_in_current_best_path(G, end)