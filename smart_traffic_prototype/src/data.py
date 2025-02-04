import sqlite3
import datetime
import locale
# Etablir la langue des caractères
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

# Récupération des données temporelles
dateH = datetime.datetime.now()
semaine = dateH.isocalendar()[1]
jour = dateH.strftime("%A").capitalize()
weekEnd = jour in ["Samedi", "Dimanche"]

#_______________________________________________________________________________________________________

            # --------------------------------------------------
            # ----------------- FONCTIONS DATA -----------------
            # --------------------------------------------------

# Fonctions auxiliaires (comme défini précédemment)
def reinitialiser_donnees():
    # Connect to the SQLite database
    conn = sqlite3.connect('db-copy.sqlite3')
    c = conn.cursor()

    # Temporarily disable foreign key constraints
    c.execute("PRAGMA foreign_keys = OFF;")

    # Delete all data from the tables in the correct order
    tables = ['app_detectionvehicule', 'app_detection', 'app_vehicule', 'app_feu', 'app_etatfeu', 'app_rue', 'app_typevehicule', 'app_temps']
    for table in tables:
        c.execute(f"DELETE FROM {table};")

    # Re-enable foreign key constraints
    c.execute("PRAGMA foreign_keys = ON;")

    # Insert data into the tables
    c.execute("INSERT INTO app_rue (idRue ,nomRue) VALUES (1, 'Route d''Orléans'), (2, 'Route de Massy');")
    c.execute("INSERT INTO app_typevehicule (idTypeVehicule, nomTypeVehicule) VALUES (1, 'Voiture'), (2, 'Camion'), (3, 'Bus');")
    c.execute("INSERT INTO app_etatfeu (idEtatFeu, nomEtatFeu) VALUES (1, 'Vert'), (2, 'Rouge'), (3, 'Orange'), (4, 'Eteint');")
    c.execute("INSERT INTO app_feu (idFeu, nomFeu, rue_id, etatFeu_id) VALUES (1, 'Feu1', 1, 1), (2, 'Feu2', 2, 1), (3, 'Feu3', 1, 2), (4, 'Feu4', 2, 2);")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Fonction pour insérer les détections
def inserer_detections(id_type_vehicule, nombre_detections, id_rue, id_feu, curseur, dateH, semaine, jour, weekEnd):
    for i in range(nombre_detections):
        curseur.execute("INSERT INTO app_temps (dateHeure, semaine, jourSemaine, isWeekEnd) VALUES (?, ?, ?, ?)", (dateH, semaine, jour, weekEnd))    
        idTemps = curseur.lastrowid

        curseur.execute("INSERT INTO app_detection (temps_id, rue_id, feu_id) VALUES (?, ?, ?)", (idTemps, id_rue, id_feu))
        idDetection = curseur.lastrowid

        curseur.execute("INSERT INTO app_vehicule (nomVehicule, typevehicule_id) VALUES (?, ?)", ("Véhicule", id_type_vehicule))
        idVehicule = curseur.lastrowid

        curseur.execute("INSERT INTO app_detectionvehicule (vehicule_id, detection_id) VALUES (?, ?)", (idVehicule, idDetection))

# Fonction pour réinitialiser le compteur d'auto-incrémentation des ids
def reset_autoincrement(cursor, table_name):
    cursor.execute(f"UPDATE sqlite_sequence SET seq = 0 WHERE name = '{table_name}'")

# Fonction principale pour insérer les détections
def insertion(id_rue, id_feu, cars, trucks, buses):
    # Connexion à la base de données avec un gestionnaire de contexte
    try:
        with sqlite3.connect("db-copy.sqlite3") as connexion:
            curseur = connexion.cursor()
            isDetection = False
            reset_autoincrement(curseur, 'app_temps')
            reset_autoincrement(curseur, 'app_detection')
            reset_autoincrement(curseur, 'app_vehicule')
            reset_autoincrement(curseur, 'app_detectionvehicule')

            if buses > 0:
                isDetection = True
                inserer_detections("3", buses, id_rue, id_feu, curseur, dateH, semaine, jour, weekEnd)
            else:
                print("Pas de bus détecté !")

            if cars > 0:
                isDetection = True
                inserer_detections("1", cars, id_rue, id_feu, curseur, dateH, semaine, jour, weekEnd)
            else:
                print("Pas de voiture détectée !")

            if trucks > 0:
                isDetection = True
                inserer_detections("2", trucks, id_rue, id_feu, curseur, dateH, semaine, jour, weekEnd)
            else:
                print("Pas de camion détecté !")

            if not isDetection:
                print("Pas de véhicule détecté !")


            # La transaction est automatiquement validée (commit) en sortant du bloc with
    except sqlite3.Error as e:
        print("Une erreur est survenue lors de la connexion à la base de données:", e)
