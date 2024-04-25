import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load data from CSV file (flights.csv)
file_path = 'D:/dev/FlightRoute-/flights.csv'
flights_data = pd.read_csv(file_path)

# Create a directed graph
flights_graph = nx.DiGraph()

# Add nodes and edges from the DataFrame
for idx, row in flights_data.iterrows():
    flights_graph.add_edge(row['Origin_airport'], row['Destination_airport'], weight=row['Distance'])

# Assuming your flights_graph is already created
pos = nx.spring_layout(flights_graph)  # positions for all nodes
nx.draw(flights_graph, pos, with_labels=True)
edge_labels = nx.get_edge_attributes(flights_graph, 'weight')
nx.draw_networkx_edge_labels(flights_graph, pos, edge_labels=edge_labels)

# Used to print options
destination_airports = [
    "AMW", "RDM", "EKO", "WDG", "END", "ERI", "GYY", "HYS", "ITO", "AOH", "APC", "GUS", "RNO", "RMG", 
    "TSM", "ACT", "CNW", "THV", "YUM", "CAK", "LTS", "BTM", "CIC", "DOV", "FAR", "FNT", "HVR", "HOB", 
    "HUM", "HON", "LGU", "MCN", "WRB", "MIA", "TNT", "OPF", "MPB", "TMB", "MIO", "MOT", "MIB", "OCF", 
    "OGD", "HIF", "OMA", "MIQ", "OFF", "PHT", "PUC", "PVU", "SLE", "SEM", "TPA", "MCF", "TUL", "RVS", 
    "TYR", "UKI", "UCA", "ABY", "ALB", "CVO", "APN", "AHN", "MMI", "AUO", "IN1", "AUS", "BSM", "TX6", 
    "BGR", "BIH", "BOS", "BYI", "CPR", "CVN", "CVS", "DFW", "DAL", "FTW", "FWH", "AFW", "ADS", "DNE", 
    "DNN", "DAY", "MGY", "FFO", "DHN", "DLH", "ESN", "ELM", "EUG", "ACV", "EKA", "NFL", "FAT", "FCH", 
    "GUP", "HLN", "1B1", "ITH", "JLN", "JNU", "JSE", "ADQ", "KDK", "OKK", "LRD", "LUL", "LAW", "LOZ", 
    "MAE", "MWA", "MZZ", "MNN", "MCE", "MOB", "BFM", "MLU", "MIE", "APF", "EWR", "OXR", "PIA", "PIR", 
    "PUB", "UIN", "RAC", "RSN", "SLN", "SRC", "NC3", "SSC", "SUM", "TCM", "GRF", "TIW", "TOL", "TDZ", 
    "FOE", "TUS", "DMA", "TUP", "UVA", "VEL", "CWA", "STE", "YKM", "ABI", "DYS", "AOO", "AWX", "ADM", 
    "AST", "ATL", "PDK", "FTY", "AGS", "AUG", "WVL", "BKW", "BFR", "BJI", "VWL", "BZN", "BKG", "BUF", 
    "ORD", "MDW", "CGX", "PWK", "DPA", "II2", "CHI", "CWI", "DCU", "DEC", "DRT", "DLF", "DTW", "DET", 
    "YIP", "DBQ", "DRO", "AMK", "ELP", "BIF", "EKI", "FDY", "FET", "GAD", "MS1", "VWD", "HKY", "HLM", 
    "MI2", "HOU", "IAH", "EFD"
]

# Function to find the shortest path using Dijkstra's algorithm
def dijkstra(graph, start):
    # Shortest paths is a dict of nodes whose value is a tuple of (previous node, weight)
    shortest_paths = {vertex: (None, float('infinity')) for vertex in graph}
    shortest_paths[start] = (None, 0)
    current_node = start
    visited = set()
    
    while current_node is not None:
        visited.add(current_node)
        # Get all neighboring nodes and their respective weights
        destinations = graph[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph[current_node][next_node]['weight'] + weight_to_current_node
            if shortest_paths[next_node][1] > weight:
                shortest_paths[next_node] = (current_node, weight)
        
        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        current_node = None
        if next_destinations:
            # Next vertex is the destination with the lowest weight
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
    
    return shortest_paths

# Extracts the shortest path to target using the shortest paths dict
def extract_path(shortest_paths, target):
    path = []
    while target is not None:
        path.insert(0, target)
        next_node = shortest_paths[target][0]
        target = next_node
    return path

# Function to identify hubs (airports with the most flights). Retrieves the top 5
def identify_hubs(graph, top_n=5):
    in_degrees = graph.in_degree()
    out_degrees = graph.out_degree()
    
    # Sort nodes based on the degree values and slice to get the top N
    top_incoming_hubs = sorted(in_degrees, key=lambda x: x[1], reverse=True)[:top_n]
    top_outgoing_hubs = sorted(out_degrees, key=lambda x: x[1], reverse=True)[:top_n]
    
    return top_outgoing_hubs, top_incoming_hubs

# Function to determine unreachable airports
def unreachable_airports(graph, source):
    reachable = nx.descendants(graph, source)
    all_nodes = set(graph.nodes)
    unreachable = all_nodes - reachable
    return unreachable

def view_graph():
    plt.show()

view = input("Do you want to view a visual of the flight graph? yes/no\n").upper()
if view == "YES":
    plt.show()
# Execute Dijkstra's algorithm to find shortest paths from user input
print("1. Find the shortest flight from two airports.")

view_airports = input("Do you need a printed list of available airports? yes/no\n").upper()
if view_airports == "YES":
    print("Airport Choices:\n")
    print(destination_airports)
    print("\n")

while True:
    outgoing_choice = input("Enter the outgoing airport (Three letter airport code.)\n").upper()
    if outgoing_choice in flights_graph:
        break
    else:
        print("Airport not found. Please try again.")

shortest_paths = dijkstra(flights_graph, outgoing_choice)

while True:
    destination_choice = input("Enter the destination airport (Three letter airport code.)\n").upper()
    if destination_choice in flights_graph:
        break
    else:
        print("Airport not found. Please try again.")
        
# Extract specific path and distance
path = extract_path(shortest_paths, destination_choice)
path_distance = shortest_paths[destination_choice][1] if path else None

if outgoing_choice in flights_graph.nodes() and destination_choice in flights_graph.nodes():
    shortest_paths = dijkstra(flights_graph, outgoing_choice)
    path = extract_path(shortest_paths, destination_choice)
    if path and shortest_paths[destination_choice][1] < float('infinity'):
        path_distance = shortest_paths[destination_choice][1]
        print(f"Shortest path from {outgoing_choice} to {destination_choice}: A distance of {path_distance} miles.")
    else:
        print(f"No path exists from {outgoing_choice} to {destination_choice}")
else:
    print("One or both of the airport codes entered are not in the graph.")

# Check unreachable airports from user selected airport
unreachable_choice = input("2. Enter an airport code to find unreachable airports (Three letter airport code. Example: Kansas City Airport = MCI)\n").upper()
unreachable = unreachable_airports(flights_graph, unreachable_choice)
print(f"Unreachable airports from {unreachable_choice}:\n", unreachable)
print("\n")

# Identify top 5 hubs
top_outgoing_hubs, top_incoming_hubs = identify_hubs(flights_graph)

print("Top 5 airport hubs with the most outgoing flights:")
for airport, count in top_outgoing_hubs:
    print(f"{airport} with {count} outgoing flights")
