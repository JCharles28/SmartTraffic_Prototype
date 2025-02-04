import streamlit as st
from ultralyticsplus import YOLO, render_result
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import locale
from collections import defaultdict
import plotly.express as px
from moviepy.editor import VideoFileClip
import time

# Importation du  script algorithm.py
# from algorithm import affichage_algo
from project.yolo_project.src.tracking import *
from project.yolo_project.src.model import load_model
from project.yolo_project.src.algorithme import main_algo

# Etablir la langue des caractères
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')  

st.markdown('<h1 style="font-family: Segoe UI; text-align: center; color: #fff">Smart Traffic</h1>', unsafe_allow_html=True)
st.markdown('<h3 style="font-family: Segoe UI; text-align: center; color: red">Powered by Evolukid & Orange </h3>', unsafe_allow_html=True)

# Chargement du modèle
model = load_model()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'password' not in st.session_state:
    st.session_state.password = ''

# Group multiple widgets:
with st.form(key='my_form'):
    username = st.text_input("Nom d'utilisateur (login)")
    password = st.text_input('Mot de passe', type='password')
    btn_connexion = st.form_submit_button('Connexion')

st.session_state.username = username
st.session_state.password = password

# Stocker les users et les mots de passe dans un dictionnaire
users = {
    "admin": "admin",
    "user": "user",
    "morad": "attik",
    "rabah": "attik",
    "admin": "admin",
    "walid": "atik",
    "najlae": "chilouet",
    "jean-charles": "mchangama"
}

# Initialisation des variables depoints
points_1 = points_2 = points_3 = points_4 = 0

if btn_connexion:
    if st.session_state.username in users and users[st.session_state.username] == password:
        st.session_state.logged_in = True

        st.success("Connexion réussie")
    else:
        st.session_state.logged_in = False
        st.error("Login ou mot de passe incorrect...")

if st.session_state.logged_in:
        st.markdown('<hr>', unsafe_allow_html=True)
        st.markdown('<h4 style="font-family: Segoe UI; text-align: center; color: #fff; text-shadow: 0 0 1px #fff; margin: 0 0 5% 0">Bienvenue à la session de démo du système, Smart Traffic !</h3>', unsafe_allow_html=True)
        
        a, b, c = st.columns([1,3,1])
        b.image("media/out/carrefour_rouge.png", width=400, caption="Carrefour de Champart, Chily-Mazarin (91)")   

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        # colonne 1
        if 'uploaded_file1' not in st.session_state:
            st.session_state.uploaded_file1 = None
        if 'points_1' not in st.session_state: 
            st.session_state.points_1 = 0

        col1.markdown('<h5 style="font-family: Segoe UI; text-align: center; color: #fff; margin: 3% 0 0 0;">Axe Nord-Sud</h5>', unsafe_allow_html=True)
        col2.markdown('<h5 style="font-family: Segoe UI; text-align: center; color: #fff; margin: 3% 0 0 0;">Axe Est-Ouest</h5>', unsafe_allow_html=True)
        

        col1.markdown('<h6 style="margin: 1.5% 0 1.5% 0">Voie 1</h6>', unsafe_allow_html=True)
        uploaded_file1 = col1.file_uploader("Choisir une vidéo de traffic routier", type=["mov", "hevc", "heic", "avi", "mp4"], key="video1")

        if uploaded_file1 is not None and uploaded_file1 != st.session_state.uploaded_file1:
            st.session_state.uploaded_file1 = uploaded_file1
            col1.video(uploaded_file1)
            col1.write('Vidéo en analyse...')
            detection_counts1, duration1 = process_and_display_video(uploaded_file1, model, 1)
            print("detection_counts1:",detection_counts1)
            if detection_counts1:
                col1.write('Résultats :')
                # col1.warning(f"Temps du process : {duration1} secondes")
                display_results(detection_counts1, col1)
                with st.spinner('Analyse en cours...'):          
                    col1.video('media/out/output1.mp4')
                    analyze_data(detection_counts1, 1, 1, col1)
                    points_1 += extract_points(detection_counts1)
                    st.session_state.points_1 += points_1
                    print("Points:",points_1)
                    col1.success(f"Points : {points_1}")
        
        # colonne 2
        if 'uploaded_file2' not in st.session_state:
            st.session_state.uploaded_file2 = None
        if 'points_2' not in st.session_state:
            st.session_state.points_2 = 0

        col2.markdown('<h6 style="margin: 1.5% 0 1.5% 0">Voie 2</h6>', unsafe_allow_html=True)
        uploaded_file2 = col2.file_uploader("Choisir une vidéo de traffic routier", type=["mov", "hevc", "heic", "avi", "mp4"], key="video2")

        if uploaded_file2 is not None and uploaded_file2 != st.session_state.uploaded_file2:
            st.session_state.uploaded_file2 = uploaded_file2
            col2.video(uploaded_file2)
            col2.write('Vidéo en analyse...')
            detection_counts2, duration2 = process_and_display_video(uploaded_file2, model, 2)
            print("detection_counts2:",detection_counts2)
            if detection_counts2:
                col2.write('Résultats :')
                # col2.warning(f"Temps du process : {duration2} secondes")
                display_results(detection_counts2, col2)
                with st.spinner('Analyse en cours...'):          
                    col2.video('media/out/output2.mp4')
                    analyze_data(detection_counts2, 2, 2, col2)
                    points_2 += extract_points(detection_counts2)
                    st.session_state.points_2 += points_2
                    print("Points:",points_2)
                    col2.success(f"Points : {points_2}")         
        
        
        # colonne 3
        if 'uploaded_file3' not in st.session_state:
            st.session_state.uploaded_file3 = None
        if 'points_3' not in st.session_state:
            st.session_state.points_3 = 0

        col3.markdown('<h6 style="margin: 1.5% 0 1.5% 0">Voie 3</h6>', unsafe_allow_html=True)
        uploaded_file3 = col3.file_uploader("Choisir une vidéo de traffic routier", type=["mov", "hevc", "heic", "avi", "mp4"], key="video3")

        if uploaded_file3 is not None and uploaded_file3 != st.session_state.uploaded_file3:
            st.session_state.uploaded_file3 = uploaded_file3
            col3.video(uploaded_file3)
            col3.write('Vidéo en analyse...')
            detection_counts3, duration3 = process_and_display_video(uploaded_file3, model, 3)
            print("detection_counts3:",detection_counts3)
            if detection_counts3:
                col3.write('Résultats :')
                # col3.warning(f"Temps du process : {duration3} secondes")
                display_results(detection_counts3, col3)
                with st.spinner('Analyse en cours...'):          
                    col3.video('media/out/output3.mp4')
                    analyze_data(detection_counts3, 1, 3, col3)
                    points_3 += extract_points(detection_counts3)
                    st.session_state.points_3 += points_3
                    print("Points:",points_3)
                    col3.success(f"Points : {points_3}")         
        
        # colonne 4
        if 'uploaded_file4' not in st.session_state:
            st.session_state.uploaded_file4 = None
        if 'points_4' not in st.session_state:
            st.session_state.points_4 = 0

        col4.markdown('<h6 style="margin: 1.5% 0 1.5% 0">Voie 4</h6>', unsafe_allow_html=True)
        uploaded_file4 = col4.file_uploader("Choisir une vidéo de traffic routier", type=["mov", "hevc", "heic", "avi", "mp4"], key="video4")

        if uploaded_file4 is not None and uploaded_file4 != st.session_state.uploaded_file4:
            st.session_state.uploaded_file4 = uploaded_file4
            col4.video(uploaded_file4)
            col4.write('Vidéo en analyse...')
            detection_counts4, duration4 = process_and_display_video(uploaded_file4, model, 4)
            print("detection_counts4:",detection_counts4)
            if detection_counts4:
                col4.write('Résultats :')
                # col4.warning(f"Temps du process : {duration4} secondes")
                display_results(detection_counts4, col4)
                with st.spinner('Analyse en cours...'):          
                    col4.video('media/out/output4.mp4')
                    analyze_data(detection_counts4, 2, 4, col4)
                    points_4 += extract_points(detection_counts4)
                    st.session_state.points_4 += points_4
                    print("Points:",points_4)
                    col3.success(f"Points : {points_4}")   

        points_voie2 = st.session_state.points_1 + st.session_state.points_3
        points_voie1 = st.session_state.points_2 + st.session_state.points_4
        print("Points:",points_voie1, points_voie2)

        if uploaded_file1 and uploaded_file2 and uploaded_file3 and uploaded_file4: 
            st.markdown('<hr>', unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color: white;'>Résultats</h2>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center; color: white;'>L'axe Nord-Sud : {points_voie1} points</h3>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center; color: white;'>L'axe Est-Ouest : {points_voie2} points</h3>", unsafe_allow_html=True)  

            if points_voie1 > points_voie2:
                st.markdown("<h3 style='text-align: center; color: white;'>L'axe Nord-Sud est prioritaire sur L'axe Est-Ouest</h3>", unsafe_allow_html=True)
                st.image("media/out/feu_1_3.png", width=725)

            else:
                st.markdown(f"<h3 style='text-align: center; color: white;'>L'axe Est-Ouest est prioritaire sur l'axe Nord-Sud</h3>" , unsafe_allow_html=True)
                st.image("media/out/feu_2_4.png", width=725)

            # RUN ALGORITHME
            d, e, f = st.columns([2,2,2])
            e.markdown('', unsafe_allow_html=True)
            e.button("Lancer la simulation des feux", on_click=main_algo)   


