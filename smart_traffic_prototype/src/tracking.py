import streamlit as st
from ultralyticsplus import YOLO, render_result
import cv2
import numpy as np
import sqlite3
import time
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from collections import defaultdict
import tempfile
import shutil
import plotly.express as px
from moviepy.editor import VideoFileClip
import time

# Importation de scripts
from project.yolo_project.src.data import dateH, semaine, jour, weekEnd, inserer_detections, reinitialiser_donnees , insertion, reset_autoincrement

#_______________________________________________________________________________________________________

            # --------------------------------------------------
            # --------------- FONCTIONS TRACKING ---------------
            # --------------------------------------------------

def process_and_display_video(uploaded_file1, model, i):
    current = time.time()
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmpfile:
        # Write the contents of the uploaded file to the temporary file
        shutil.copyfileobj(uploaded_file1, tmpfile)
        tmpfile_path = tmpfile.name

    # Use the path of the temporary file with cv2.VideoCapture
    cap = cv2.VideoCapture(tmpfile_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(f'media/out/output{i}.avi', fourcc, fps, (width, height))
 
    detection_counts = defaultdict(int)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Perform inference
        results = model.predict(frame)
        render = render_result(model=model, image=frame, result=results[0])
        frame_out = np.array(render)

        # Save frame to video
        out.write(frame_out)

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # transforme la vidéo out format avi en mp4
    clip = VideoFileClip(f'media/out/output{i}.avi')
    clip.write_videofile(f'media/out/output{i}.mp4')

        # Count detections
    for d in results[0].boxes.data:
        class_id = int(d[5])
        class_name = model.model.names[class_id]
        if class_name in detection_counts:
            detection_counts[class_name]+=1
        else: detection_counts[class_name]=1

    trucks = (
    detection_counts.get("big truck", 0) +
    detection_counts.get("mid truck", 0) +
    detection_counts.get("small truck", 0) +
    detection_counts.get("truck-l-", 0) +
    detection_counts.get("truck-m-", 0) +
    detection_counts.get("truck-s-", 0) +
    detection_counts.get("truck-xl-", 0)
    )
    
    buses = (
        detection_counts.get("bus-s-", 0) +
        detection_counts.get("big bus", 0) +
        detection_counts.get("small bus", 0) +
        detection_counts.get("bus-l-", 0)
    )

    cars = detection_counts.get("car", 0)

    #mettre à jour le dictionnaire de détections afin qu'il y ait que les 3 types de véhicules désormais
    detection_counts.clear()
    detection_counts["car"] = cars
    detection_counts["truck"] = trucks
    detection_counts["bus"] = buses

    duration = time.time() - current
    duration = round(duration, 2)

    return detection_counts, duration

def initialize_database():
    # Using context manager for handling database connection
    with sqlite3.connect('db-copy.sqlite3') as conn:
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = OFF;")

        tables = ['app_detectionvehicule', 'app_detection', 'app_vehicule', 'app_feu', 'app_etatfeu', 'app_rue', 'app_typevehicule', 'app_temps']
        for table in tables:
            c.execute(f"DELETE FROM {table};")

        c.execute("PRAGMA foreign_keys = ON;")
        # Insert static data into tables (omitted for brevity)

        conn.commit()

def process_video(uploaded_file1, model, i):
    with st.spinner('Traitement de la vidéo...'):
        detection_counts = process_and_display_video(uploaded_file1, model, i)

    if detection_counts:
        st.success('Vidéo bien analysée !')
        display_results(detection_counts)
    else:
        st.warning("Aucune détection n'a été trouvée !")
  
def display_loading():
    with st.spinner('Chargement en cours...'):
        time.sleep(2)  # Temps de chargement simulé

def display_results(detection_counts, col):
    display_loading()
    cars = detection_counts.get("car", 0)
    trucks = detection_counts.get("truck", 0)
    buses = detection_counts.get("bus", 0)

    points_car = cars * 1
    points_truck = trucks * 2
    points_bus = buses * 3
    points = points_car + points_truck + points_bus



    # Graphique 1 : Véhicules par feu
    fig1 = px.bar(x=['Voitures', 'Camions', 'Bus'], y=[cars, trucks, buses], labels={'x': 'Type de véhicule', 'y': 'Nombre de véhicules'})
    fig1.update_layout(title_text='Véhicules détectés par type', width=300, height=400)
    col.plotly_chart(fig1)    

def extract_vehicle_counts(detection_counts):
    cars = detection_counts.get("car", 0)
    trucks = detection_counts.get("truck", 0)
    buses = detection_counts.get("bus", 0)

    return cars, trucks, buses

def extract_points(detection_counts):
    cars = detection_counts.get("car", 0)
    trucks = detection_counts.get("truck", 0)
    buses = detection_counts.get("bus", 0)

    points_car = cars * 1
    points_truck = trucks * 2
    points_bus = buses * 3
    points = points_car + points_truck + points_bus

    return points

def analyze_data(detection_counts, id_rue, id_feu, col):
    # reinitialiser_donnees()
    insertion(id_rue, id_feu, *extract_vehicle_counts(detection_counts))
    col.success("Données insérées avec succès !")

def image_feux():
    if(analyze_data):
        st.image('media/feux.jpg', width=700)

