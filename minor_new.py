import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import cv2
import os

from flask import Flask, render_template, request

app = Flask(__name__)
#data = pd.read_csv('new.csv')

def perform_influence_maximization(data, budget):
    G = nx.Graph()
    for _, row in data.iterrows():
        G.add_edge(row['Source'], row['Target'])


    def independent_cascade_model(graph, seed_nodes, p=0.2, max_iterations=1):
        influenced_nodes = set(seed_nodes)
        newly_influenced_nodes = set(seed_nodes)
       
        for _ in range(max_iterations):
            if not newly_influenced_nodes:
                break
            new_nodes = set()
            for node in newly_influenced_nodes:
                neighbors = list(graph.neighbors(node))
                for neighbor in neighbors:
                    if neighbor not in influenced_nodes:
                        if np.random.rand() < p:
                            new_nodes.add(neighbor)
            newly_influenced_nodes = new_nodes.copy()
            influenced_nodes.update(new_nodes)

        return influenced_nodes

    def greedy_algorithm(graph, k, p=0.1, max_iterations=1000):
        seed_nodes = []
        for _ in range(k):
            max_node = None
            max_influence = -1
            for node in graph.nodes():
                if node not in seed_nodes:
                    temp_seed_nodes = seed_nodes.copy()
                    temp_seed_nodes.append(node)
                    influence = len(independent_cascade_model(graph, temp_seed_nodes, p, max_iterations))
                    if influence > max_influence:
                        max_influence = influence
                        max_node = node
            seed_nodes.append(max_node)
        return seed_nodes


#budget = 10
#product_info = "Product XYZ"


    selected_seed_nodes = greedy_algorithm(G, budget)


    influenced_nodes = independent_cascade_model(G, selected_seed_nodes)
    

    node_colors = ['red' if node in selected_seed_nodes else 'blue' if node in influenced_nodes else 'yellow' for node in G.nodes()]

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42, k=0.15, iterations=100) 

    nx.draw(
        G, pos, labels={node: '' for node in G.nodes()}, node_color=node_colors, node_size=150, font_size=8, font_color='black',
        alpha=0.8, linewidths=0.5, edge_color='gray', with_labels=False
    )

    node_labels_pos = {k: (v[0] - 0.05, v[1]) for k, v in pos.items()}


    nx.draw_networkx_labels(G, node_labels_pos, font_size=6, font_color='black')


    plt.title("Your Influencers", fontsize=16)


    legend_labels = {'Seed Nodes': 'red', 'Influenced Nodes': 'blue', 'Non-Active Nodes': 'yellow'}
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=label)
                   for label, color in legend_labels.items()]
    legend = plt.legend(handles=legend_handles, loc='best', title="Legend", fontsize=10)
    legend.get_title().set_fontsize(12)
    plt.savefig("static\images\output.png")
    plt.axis('off')

    print(f"Selected Seed Nodes: {selected_seed_nodes}")
    print(f"Name of Influenced Nodes: {(influenced_nodes)}")
    print(f"Number of Influenced Nodes: {len(influenced_nodes)}")
    
    

    
    #plt.show()
    return influenced_nodes