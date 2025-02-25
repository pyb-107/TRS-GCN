import networkx as nx
import matplotlib.pyplot as plt
import random
# 这份代码的作用是画一张随机分布的二部图

# Generate a bipartite graph
B = nx.Graph()

# Number of nodes in each partition
num_nodes_1 = 10
num_nodes_2 = 16

# Create two sets of nodes for the bipartite graph
nodes_1 = [f'x{i}' for i in range(num_nodes_1)]
nodes_2 = [f'b{i}' for i in range(num_nodes_2)]

# Add the nodes with the bipartite attribute
B.add_nodes_from(nodes_1, bipartite=0)
B.add_nodes_from(nodes_2, bipartite=1)

# Create edges with varying probabilities
for u in nodes_1:
    for v in nodes_2:
        # Some nodes have a higher probability of being connected
        if random.random() < 0.3:  # Higher connection probability
            B.add_edge(u, v)
        elif random.random() < 0.05:  # Lower connection probability
            B.add_edge(u, v)

# Plot the bipartite graph
pos = nx.bipartite_layout(B, nodes_1)
plt.figure(figsize=(10, 6))
nx.draw(B, pos, with_labels=True, node_color=['skyblue' if n in nodes_1 else 'lightgreen' for n in B.nodes()])
plt.title("Randomly Generated Bipartite Graph with Variable Connection Probability")
plt.show()
