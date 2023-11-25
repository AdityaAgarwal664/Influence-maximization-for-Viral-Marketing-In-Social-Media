from flask import Flask, render_template, request
from flask import Blueprint
import pandas as pd
import  matplotlib as pl
import os
import glob
import time
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import base64
import cv2
import os
import time
import glob
import csv



app = Flask(__name__)

site = Blueprint('site', __name__, template_folder='templates')
app.register_blueprint(site)

result=[]


@app.route('/')
def index():
    return render_template('free1.html')



@app.route('/process', methods=['POST'])
def process():
    

        
    budget = int(request.form['required-influencers'])
    csv_file = request.files['csv-file']

    
       

    csv_file.save('temp.csv')

   
    data = pd.read_csv('temp.csv')
    
    selected_seed_nodes,influenced_nodes = perform_influence_maximization(data, budget)


    connection_counts = data['Source'].value_counts().reset_index()
    connection_counts.columns = ['Source Node', 'Count']

    df=pd.DataFrame(connection_counts)
    new=df.to_csv('newtemp.csv')
    ok=pd.read_csv('newtemp.csv')
  
    table2_html = ok.to_html(classes='table table-bordered', index=False, escape=False)
    image_url = 'static/video/greedy_algorithm_video.mp4' 
    image2_url = 'static/images/output1.jpg'
    table_html = data.to_html(classes='table table-bordered', index=False)
    return render_template('free1.html', image=image_url,image2=image2_url,table=table_html,table2=table2_html,selected_seed_nodes=selected_seed_nodes, influenced_nodes=influenced_nodes)






if __name__ == '__main__':
    app.run(debug=True)
    


def perform_influence_maximization(data, budget):
    
    folder_path = "static/images"


    image_extensions = ["*.png"]


    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(folder_path, ext)))


    for file in image_files:
        os.remove(file)
        
    
    image_dir = 'static/images'
    output_video_path = 'static/video/greedy_algorithm_video.mp4'
    os.makedirs(image_dir, exist_ok=True)

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
        image_counter = 0
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
            influenced_nodes = independent_cascade_model(graph,seed_nodes)
        
            node_colors = ['red' if node in seed_nodes else 'blue' if node in influenced_nodes else 'yellow' for node in G.nodes()]

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
            image_path = os.path.join(image_dir, f'iteration_{image_counter:03d}.png')
            plt.savefig(image_path,format='png')
            plt.axis('off')    
            image_counter += 1
            

       
        images = [img for img in os.listdir(image_dir) if img.endswith(".png")]
        images.sort()


        if images:
           image_path = os.path.join(image_dir, images[0])
           frame = cv2.imread(image_path)
           height, width, layers = frame.shape
        else:
           print("No images found in the directory.")
           exit()


        fourcc = cv2.VideoWriter_fourcc(*'H264')
        out = cv2.VideoWriter(output_video_path, fourcc, 1.5, (width, height))


        for image in images:
           image_path = os.path.join(image_dir, image)
           frame = cv2.imread(image_path)
           out.write(frame)


        out.release()

        
        

        dd=pd.read_csv('newtemp.csv')
        source_nodes = dd['Source Node']
        counts = dd['Count']
        dicto=dict(zip(source_nodes,counts))
        s=[]
        c=[]
        for key,val in dicto.items():
            if key in seed_nodes:
                s.append(key)
                c.append(val)
        
        print(s)
        print(c)
        plt.figure(figsize=(8, 8))
        plt.pie(c, labels=s, autopct='%1.1f%%',startangle=140,colors=plt.cm.Paired(range(len(s))))
        plt.title('Pie Chart on Connections')
        plt.axis('equal')  
        plt.savefig("static\images\output1.jpg")

        

        
        return seed_nodes
        

    selected_seed_nodes = greedy_algorithm(G, budget)
    influenced_nodes= independent_cascade_model(G, selected_seed_nodes)
    
    data = list(zip(selected_seed_nodes,influenced_nodes))
    
    
    
        
    return selected_seed_nodes,influenced_nodes