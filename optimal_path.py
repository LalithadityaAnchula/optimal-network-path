"""
NetworkX is a Python package for 
the creation, manipulation, and study of the structure, dynamics, and functions of complex networks.

"""
import networkx as nx
import matplotlib.pyplot as plt
import random
from queue import PriorityQueue

# Adjacency list and Costs dictionary for obtaining neighbours and cost between u and v in O(1) time
adList = dict()
costs = dict()

# Taking input for number of network nodes
n = int(input("Enter the number of nodes in the network : "))

# Taking input for probability to get Erdos Reyni graph
p = float(input("Enter the probability of reliability on each link between nodes in network : "))

# An Erdos Reyni grapg is returned based on given n and p
# Here p is the probability to have an edge between nodes u and v in network
g = nx.erdos_renyi_graph(n,p)


# Generating random coordinates for nodes in our network 
for (u,v) in g.nodes(data=True):
    v['pos'] = (random.randint(0,100), random.randint(0,100))   
pos=nx.get_node_attributes(g,'pos')

# Assigning random weights with constraints (i.e >= 200 and <=1000)
for (u,v,w) in g.edges(data=True):
    w['weight'] = random.randint(200,1000) 
    if u not in adList:
        adList[u] = [v]
    else:
        adList[u].append(v)
    if v not in adList:
        adList[v] = [u]
    else:
        adList[v].append(u)
    costs[tuple([u,v])] = w['weight']
        
# Getting the weights between the edges
labels = nx.get_edge_attributes(g,'weight')

# Plotting the generated grapgh model of our network
nx.draw(g,pos,with_labels=True)
nx.draw_networkx_edge_labels(g,pos,edge_labels=labels)
plt.axis('off')
plt.title('Generated network of computers')
plt.show()

# heuristic function definition
def heuristicFunction(a,b):
    """
    Our heuristic function of choice is Manhattan's distance here.
    i.e d = |x1-x2| + |y1-y2|
    
    """
    return abs(a[0]-b[0])+abs(a[1]-b[1])


def get_cost(a,b):

    """
    This is function returns the cost to reach fromone network 
    node to its neighbour network node

    """
    target_tuple = tuple([a,b])
    if target_tuple in costs:
        return costs[target_tuple]
    else:
        return costs[target_tuple[-1::-1]]


def find_optimal(start ,goal,explored):

    """

    This function uses A* algorithm for finding the optimal network path between
    given start node and goal node.
    
    Uses PriorityQueues to always obtain the node with least f(n) value from open frountier,
    where f(n) = g(n)+h(n)

    Here :  g(n) - > cost due to travel from start to node n 
            h(n) - > Heuristic estimate value from n to goal node

    """
    openFrontier = PriorityQueue()
    openFrontier.put(
        (
            heuristicFunction(pos[start],pos[goal]),
            0,
            start,
            [start]
        )
    )
    while not openFrontier.empty():

        # Popping the node from frountier
        _,g_fun,current_node,path = openFrontier.get()

        #Adding to explored set
        explored.add(current_node)

        # Optimal path to goal found
        if current_node == goal:
            print(f'Sequence of nodes in path : {path}')
            print(f'Total optimal cost : {g_fun}')
            return (path,g_fun)

        # Current_node don't have any neighbours ,So we cant expand it and have it in optimal path
        if current_node not in adList:
            continue
        
        # Expanding current node and getting neighbours
        neighbours = adList[current_node]

        #Adding neighbours to frountier for further expansion and exploring
        for node in neighbours:
            if node not in explored:
                openFrontier.put(
                    (
                        heuristicFunction(pos[node],pos[goal])+g_fun+get_cost(path[-1],node),
                        g_fun+get_cost(path[-1],node),
                        node,
                        path+[node]
                    )
                )

    # If frountier is empty and nmo path is returned means no path found
    print("Path not found")
    return None

def show_optimal_path(answer,optimal_path_cost):

    """
    Takes optimal path sequence as list of network nodes and optimal path cost as inputs 
    and plots the network with highlighted optimal path.
    
    """
    options = {"edgecolors": "tab:gray", "node_size": 800, "alpha": 0.9}
    nx.draw_networkx_nodes(g, pos,nodelist=answer, node_color="tab:red", **options)
    nx.draw_networkx_nodes(g, pos)
    nx.draw(g,pos,with_labels=True)
    path_edges = []
    for i in range(len(answer)-1):
        path_edges.append((answer[i],answer[i+1]))
    nx.draw_networkx_edges(g, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_edges(
        g,
        pos,
        edgelist=path_edges,
        width=9,
        alpha=0.6,
        edge_color="tab:red",
    )
    nx.draw_networkx_edge_labels(g,pos,edge_labels=labels)

    plt.axis('off')
    plt.title(f'Optimal network path cost : {optimal_path_cost}')
    plt.show()


# Taking input for starting network node
start = int(input("Enter the currrent network node : "))

#Taking input for destination / goal network node
goal = int(input("Enter the destination network node  : "))\

# Sequence of network nodes in path are returned as list if  there exists path
answer,optimal_path_cost = find_optimal(start,goal,set())

#If optimal path exists shows optimal path
if answer:
    show_optimal_path(answer,optimal_path_cost)
