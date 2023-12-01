from flask import Flask,render_template,request,send_file
from flask import Blueprint
import pandas as pd
import os
import glob
import networkx as nx
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
import cv2
import time



def perform_im(data,budget,algo):
    image_dir='static\images'
    output_vid_path=r'static\video\greedy_algo_video.mp4'
    G=nx.Graph()
    for _,row in data.iterrows():
        G.add_edge(row['Source'],row['Target'])

    def icm(graph,seed_nodes,p=0.2,max_iterations=1):
        influenced_nodes=set(seed_nodes)
        newly_influenced_nodes=set(seed_nodes)
        for _ in range(max_iterations):
            if not newly_influenced_nodes:
                break
            new_nodes=set()
            for node in newly_influenced_nodes:
                neighbors=list(graph.neighbors(node))
                for neighbor in neighbors:
                    if neighbor not in influenced_nodes:
                        if np.random.rand() < p:
                            new_nodes.add(neighbor)
            newly_influenced_nodes=new_nodes.copy()
            influenced_nodes.update(new_nodes)

        return influenced_nodes
    def greedy_algo(graph,k,p=0.1,max_iterations=1000):
        seed_nodes=[]
        image_counter=0
        for _ in range(k):
            max_node=None
            max_influence=-1
            for node in graph.nodes():
                
                if node not in seed_nodes:
                    temp_seed=seed_nodes.copy()
                    temp_seed.append(node)
                    influence=len(icm(graph,temp_seed,p,max_iterations))
                    if influence>max_influence:
                        max_influence=influence
                        max_node=node
            seed_nodes.append(max_node)
            influence_nodes=icm(graph,seed_nodes)
            node_colors=['red' if node in seed_nodes else 'green' if node in influence_nodes else 'blue' for node in G.nodes()]
            plt.figure(figsize=(12,8))
            pos=nx.spring_layout(G,seed=40,k=0.15,iterations=100)
            nx.draw(
                G, pos, labels={node: '' for node in G.nodes()}, node_color=node_colors, node_size=150, font_size=8, font_color='black',
                alpha=0.8,linewidths=0.5, edge_color='gray', with_labels=False
                )
            
            node_labels_pos={k:(v[0]-0.05,v[1]) for k,v in pos.items()}
            nx.draw_networkx_labels(G,node_labels_pos,font_size=7,font_color='black')
            plt.title('Your infuencers through Greedy')
            legend_labels={'Seed Nodes':'Red',"Influencers Nodes":'green','Non-Active Nodes':'blue'}
            legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=label)
                   for label, color in legend_labels.items()]
            legend=plt.legend(handles=legend_handles,loc='best',title='Legend',fontsize=10)
            legend.get_title().set_fontsize(12)
            image_path=os.path.join(image_dir,f"pic_{image_counter:03d}.png")
            plt.savefig(image_path,format='png')
            plt.axis('off')
            image_counter+=1
            plt.close()
        return seed_nodes
    
    def visualize_g(graph,seed_nodes,influenced_nodes,image_counter):
        node_colors=['red' if node in seed_nodes else 'green' if node in influenced_nodes else 'blue' for node in G.nodes()]
        plt.figure(figsize=(12,8))
        pos=nx.spring_layout(G,seed=40,k=0.15,iterations=100)
        nx.draw(graph,pos,labels={node:'' for node in G.nodes()},node_color=node_colors,node_size=140,font_size=9,font_color='black',alpha=0.8,linewidths=0.5,edge_color='gray',with_labels=False)
        node_labels_pos={k:(v[0]-0.05,v[1]) for k,v in pos.items()}
        nx.draw_networkx_labels(G,node_labels_pos,font_size=7,font_color='black')
        plt.title('Your infuencers')
        legend_labels={'Seed Nodes':'Red',"Influencers Nodes":'green','Non-Active Nodes':'blue'}
        legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=label)
                for label, color in legend_labels.items()]
        legend=plt.legend(handles=legend_handles,loc='best',title='Legend',fontsize=10)
        legend.get_title().set_fontsize(12)
        image_path=os.path.join(image_dir,f"pic_{image_counter:03d}.png")
        plt.savefig(image_path,format='png')
        plt.axis('off')
        plt.close()

    def deg_cen(graph,k):
        influence_nodes=set()
        seed_nodes=[]
        image_counter=0
        for _ in range(k):
            max_node=None
            max_degree=-1
            for node,degree in nx.degree_centrality(graph).items():
                if node not in seed_nodes and degree>max_degree:
                    max_degree=degree
                    max_node=node
            seed_nodes.append(max_node)
            neighbors=set(graph.neighbors(max_node))
            influence_nodes.update(neighbors)

            visualize_g(graph,seed_nodes,influence_nodes,image_counter)
            image_counter+=1
        return seed_nodes,influence_nodes
    
    def pag_rank(graph,k):
        influence_nodes=set()
        seed_nodes=[]
        image_counter=0
        for _ in range(k):
            max_node=None
            max_degree=-1
            for node,degree in nx.pagerank(graph).items():
                if node not in seed_nodes and degree>max_degree:
                    max_degree=degree
                    max_node=node
            seed_nodes.append(max_node)
            neighbors=set(graph.neighbors(max_node))
            influence_nodes.update(neighbors)

            pag_rank(graph,seed_nodes,influence_nodes,image_counter)
            image_counter+=1
        return seed_nodes,influence_nodes
    
    if(algo=='Greedy'):
        selected_seed_nodes=greedy_algo(G,budget)
        influenced_nodes=icm(G,selected_seed_nodes)
        data=list(zip(selected_seed_nodes,influenced_nodes))
    
    elif(algo=='Pagerank'):
        selected_seed_nodes,influenced_nodes=pag_rank(G,budget)
        data=list(zip(selected_seed_nodes,influenced_nodes))
    
    elif(algo=='degreeCentrality'):
        selected_seed_nodes,influenced_nodes=deg_cen(G,budget)
        data=list(zip(selected_seed_nodes,influenced_nodes))
    else:
        print("no")
    
    images=[img for img in os.listdir(image_dir) if img.endswith('.png')]
    images.sort()

    if images:
        image_path=os.path.join(image_dir,images[0])
        frame=cv2.imread(image_path)
        height,width,layers=frame.shape
    else:
        exit()
    
    fourcc=cv2.VideoWriter_fourcc(*'H264')
    out=cv2.VideoWriter(output_vid_path,fourcc,1.5,(width,height))

    for image in images:
        image_path=os.path.join(image_dir,image)
        frame=cv2.imread(image_path)
        out.write(frame)

    out.release()

    dd=pd.read_csv('newtemp.csv')
    source_nodes=dd['Source node']
    counts=dd['Count']
    plt.figure(figsize=(8,8))
    plt.pie(counts,labels=source_nodes,autopct='%1.1f%%',startangle=140,colors=plt.cm.Paired(range(len(source_nodes))))
    plt.title("Pie Chart on connections")
    plt.axis('equal')
    plt.savefig("static\images\pie.jpg")
    
    plt.figure(figsize=(10,6))
    plt.plot(dd['Source node'],dd['Count'],marker='o',linestyle='-',color='b')
    plt.title("Line Chart on connections")
    plt.xlabel('Source')
    plt.ylabel('Connections')
    plt.grid(True)
    plt.axis('equal')
    plt.savefig("static\images\line.jpg")

    plt.figure(figsize=(10,6))
    plt.bar(dd['Source node'],dd['Count'],color='c')
    plt.title("Bar Chart on connections")
    plt.xlabel('Source')
    plt.ylabel('Connections')
    plt.grid(axis='y')
    plt.axis('equal')
    plt.savefig(r"static\images\bar.jpg")

    plt.figure(figsize=(10,6))
    plt.scatter(dd['Source node'],dd['Count'],marker='o',color='r')
    plt.title("Scatter Chart on connections")
    plt.xlabel('Source')
    plt.ylabel('Connections')
    plt.grid()
    plt.axis('equal')
    plt.savefig("static\images\Scatter.jpg")

    import seaborn as sns

    df=pd.read_csv('newtemp.csv')
    heatmap_data=df.pivot(index='Source node',columns='Count',values='Count')
    plt.figure(figsize=(10,6))
    sns.heatmap(heatmap_data,cmap='YlGnBu',annot=True,fmt='g',linewidths=0.5)
    plt.title('Heat Map of source nodes and counts')
    plt.savefig("static\images\heatmap.jpg")

    return selected_seed_nodes,influenced_nodes

app=Flask(__name__)
site=Blueprint('site',__name__,template_folder='template')
app.register_blueprint(site)
result=[]

@app.route('/')
def index():
    return render_template('free1.html')

@app.route('/process',methods=['POST'])
def process():
    folder_path='static\video'
    image_extensions=['*.mp4']

    image_files=[]
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(folder_path,ext)))

    for file in image_files:
        os.remove(file)

    budget=int(request.form['required-influencers'])
    csv_file=request.files['csv-file']
    algo=request.form.get('algorithmSelect')

    
    folder_path='static\iamges'
    image_extensions=['*.png','*jpg']

    image_files=[]
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(folder_path,ext)))

    for file in image_files:
        os.remove(file)
    
    csv_file.save('temp.csv')
    data=pd.read_csv('temp.csv')
    connection_counts=data['Source'].value_counts().reset_index()
    connection_counts.columns=['Source node','Count']
    df=pd.DataFrame(connection_counts)
    new=df.to_csv('newtemp.csv')
    selected_seed_nodes,influenced_nodes=perform_im(data,budget,algo)
    
    
    #df=pd.DataFrame('newtemp.csv')

    
    ok=pd.read_csv('newtemp.csv')
    
    video_path='static\video\greedy_algo_video.mp4'
    table2_html=ok.to_html(classes='table table-bordered',index=False,escape=False)
    image2_url='static\images\pie.jpg'
    image3_url='static\images\bar.jpg'
    image4_url='static\images\Scatter.jpg'
    image5_url='static\images\line.jpg'
    image6_url='static\images\heatmap.jpg'
    table_html = data.to_html(classes='table table-bordered', index=False)
    return render_template('free1.html',video=video_path,image2=image2_url,image3=image3_url,image4=image4_url,image5=image5_url,image6=image6_url,table=table_html,table2=table2_html,selected_seed_nodes=selected_seed_nodes, influenced_nodes=influenced_nodes)
 
@app.route('/get_video')
def get_video():
    video_path='static\video\greedy_algo_video.mp4'
    return send_file(video_path,mimetype='video/mp4')

if __name__ == '__main__':
    app.run(debug=True)


    