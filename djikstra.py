import networkx as nx
import matplotlib.pyplot as plt
import math


# no a efficient implementation but rather a textbook like configuration


def init_adjaceny_matrix(number_of_nodes: int):
    adjacency_matrix = []
    for i in range(0, number_of_nodes):
        adjacency_matrix.append([])
        for j in range(0, number_of_nodes):
            adjacency_matrix[i] += [math.inf]

    return adjacency_matrix


def connect_vertices(matrix, first_vertex: int, second_vertex: int, value):
    matrix[first_vertex][second_vertex] = value


def remove_connection(matrix, first_vertex: int, second_vertex: int):
    matrix[first_vertex][second_vertex] = math.inf


def visualize_adjaceny_matrix(matrix, colour_nodes=None):
    if colour_nodes is None:
        colour_nodes = []
    G = nx.DiGraph()
    labeldict = {}
    for i in range(1, len(matrix)):
        if i in colour_nodes:
            print(i)
            G.add_node(i, node_color="tab:red")
        else:
            G.add_node(i)
        labeldict[i] = i

    for i in range(1, len(matrix)):
        for j in range(1, len(matrix)):
            vertex = matrix[i][j]
            if vertex != math.inf:
                G.add_edge(i, j, weight=vertex)

    colour_map = ["red" if i in colour_nodes else "blue" for i in range(1, len(matrix))]
    pos = nx.circular_layout(G)
    nx.draw(G, pos, labels=labeldict, with_labels=True, node_color=colour_map)
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()


def get_outgoing_edges(matrix, vertex):
    points = matrix[vertex]
    return_list = []
    for point in range(1, len(points)):
        point_value = matrix[vertex][point]
        if point_value != math.inf:
            return_list.append(point)

    return return_list


class PriorityQueue:
    # very inefficient implementation to showcase the algorithm
    # in utmost simplicity - a binary heap or rather a fibonacci
    # heap would be needed for more efficiency at scale
    priority_dict = []

    def add(self, item, priority):
        self.priority_dict.append([priority, item])

    def update_priority(self, item, priority):
        candidate = None
        for element in self.priority_dict:
            if element[1] == item:
                candidate = element
                break

        if candidate is not None:
            self.priority_dict.remove(candidate)

        self.priority_dict.append([priority, item])

    def empty(self):
        return len(self.priority_dict) == 0

    def pop(self):
        search = sorted(self.priority_dict, key=lambda x: x[0])
        element = search[0]
        self.priority_dict.remove(element)
        return element[1]


def djikstra(matrix, start_node):
    list_of_other_nodes = list(range(len(matrix)))
    list_of_other_nodes.remove(0)
    list_of_other_nodes.remove(start_node)

    distances = {}
    distances[start_node] = 0

    queue = PriorityQueue()
    visited_nodes = [start_node]

    while list_of_other_nodes:
        vertex = list_of_other_nodes.pop()
        distances[vertex] = math.inf

        queue.add(vertex, math.inf)

    for node in get_outgoing_edges(matrix, start_node):
        distances[node] = matrix[start_node][node]
        queue.update_priority(node, matrix[start_node][node])

    while not queue.empty():
        vertex = queue.pop()
        visited_nodes += [vertex]
        for node in get_outgoing_edges(matrix, vertex):
            # check if new route is shorter than known route
            if distances[vertex] + matrix[vertex][node] < distances[node]:
                distances[node] = distances[vertex] + matrix[vertex][node]
                queue.update_priority(node, distances[node])

        print(distances)
        visualize_adjaceny_matrix(matrix, colour_nodes=visited_nodes)

    return distances
# sample djikstra set
matrix = init_adjaceny_matrix(7)

connect_vertices(matrix, 1, 2, 1)
connect_vertices(matrix, 1, 6, 3)
connect_vertices(matrix, 2, 6, 3)
connect_vertices(matrix, 2, 3, 2)
connect_vertices(matrix, 3, 6, 1)
connect_vertices(matrix, 3, 4, 1)
connect_vertices(matrix, 4, 5, 1)
connect_vertices(matrix, 4, 6, 1)
connect_vertices(matrix, 5, 6, 6)
connect_vertices(matrix, 5, 1, 1)
connect_vertices(matrix, 6, 1, 1)

print(djikstra(matrix, 5))
