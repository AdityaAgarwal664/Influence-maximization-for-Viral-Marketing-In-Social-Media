from flask import Flask, render_template, request, send_file
from flask import Blueprint
import pandas as pd
import pymongo
import minor_new_new
from io import BytesIO
import base64
import  matplotlib as pl
import os
import glob
import time

app = Flask(__name__)

site = Blueprint('site', __name__, template_folder='templates')
app.register_blueprint(site)

result=[]


@app.route('/')
def index():
    return render_template('free1.html')



@app.route('/process', methods=['POST'])
def process():
    folder_path = "static/video"

    
    image_extensions = ["*.mp4"]


    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(folder_path, ext)))


    for file in image_files:
        os.remove(file) 
    budget = int(request.form['required-influencers'])
    csv_file = request.files['csv-file']
    algo=request.form.get('algorithmSelect')
    

    folder_path = "static/images"


    image_extensions = ["*.png","*.jpg"]


    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(folder_path, ext)))


    for file in image_files:
        os.remove(file)
    
    
    csv_file.save('temp.csv')
    
   
    data = pd.read_csv('temp.csv')
    
    selected_seed_nodes,influenced_nodes = minor_new_new.perform_influence_maximization(data, budget, algo)
    
    
    connection_counts = data['Source'].value_counts().reset_index()
    connection_counts.columns = ['Source Node', 'Count']
    df=pd.DataFrame(connection_counts)
    
    new=df.to_csv('newtemp.csv')
    time.sleep(7)
    ok=pd.read_csv('newtemp.csv')
    video_path = 'static/video/greedy_algorithm_video.mp4'

    table2_html = ok.to_html(classes='table table-bordered', index=False, escape=False)
    image2_url = 'static/images/output1.jpg'
    table_html = data.to_html(classes='table table-bordered', index=False)
    return render_template('free1.html',video=video_path,image2=image2_url,table=table_html,table2=table2_html,selected_seed_nodes=selected_seed_nodes, influenced_nodes=influenced_nodes)

@app.route('/get_video')
def get_video():
    video_path = 'static/video/greedy_algorithm_video.mp4'
    return send_file(video_path, mimetype='video/mp4')
# @app.route('/video')
# def video():
    

#       # Replace with the actual path to your video file
#     return send_file(video_path, mimetype='video/mp4')


# folder_path = "static/video"

    
# image_extensions = ["*.mp4"]


# image_files = []
# for ext in image_extensions:
#     image_files.extend(glob.glob(os.path.join(folder_path, ext)))


# for file in image_files:
#     os.remove(file)

if __name__ == '__main__':
    app.run(debug=True)
    # folder_path = "static/video"

    
    # image_extensions = ["*.mp4"]


    # image_files = []
    # for ext in image_extensions:
    #     image_files.extend(glob.glob(os.path.join(folder_path, ext)))


    # for file in image_files:
    #     os.remove(file)

    

