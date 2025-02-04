import time, sqlite3
import tkinter as tk

db_path = r"C:\Users\chari\OneDrive\Desktop\KESKIA\MontoringSmartTraffic\project\yolo_project\src\db-copy.sqlite3"

# Chemin vers la base de donnees SQLite (ajuste pour Windows)
# print(f"Le chemin vers la base de données :  {db_path}\n")


# Définissez canvas comme une variable globale
canvas = None

voitureTime = 2
busTime = 2.5
camionTime = 2.5

class Voie:
    def __init__(self, feu, voitures, bus, camions):
        self.feu = feu
        self.vehicules = voitures + bus + camions
        self.voitures = voitures
        self.bus = bus
        self.camions = camions
        self.temps_vert = voitureTime*self.voitures + busTime*self.bus + camionTime*self.camions
        self.temps_rouge = 80
        self.temps_orange = 5
        self.points = voitures + 2*bus + camions

    def get_feu_vert_voie(self):
        if self.temps_vert > 30:
            return 30
        return self.temps_vert

class Avenue:
    # composer de 2 voies face à face
    def __init__(self, voie1, voie2):
        self.Voie1 = voie1
        self.Voie2 =  voie2
        self.vehicules = voie1.vehicules + voie2.vehicules
        self.voitures = voie1.voitures + voie2.voitures
        self.bus = voie1.bus + voie2.bus
        self.camions = voie1.camions + voie2.camions
        self.points = voie1.camions + voie2.voitures + 2*voie1.bus
        self.temps_vert = voie1.get_feu_vert_voie() if voie1.get_feu_vert_voie() > voie2.get_feu_vert_voie() else voie2.get_feu_vert_voie()
        self.temps_rouge = voie1.temps_rouge | voie2.temps_rouge
        self.temps_orange = voie1.temps_orange | voie2.temps_orange

    def get_points_avenue(self):
        return self.Voie1.points + self.Voie2.points

    def get_feu_vert_avenue(self):
        return self.temps_vert       

class Carrefour4Rues:
    def __init__(self, avenue1, avenue2):
        self.Avenue1 = avenue1
        self.Avenue2 = avenue2
        self.vehicules = avenue1.vehicules + avenue2.vehicules
        self.voitures = avenue1.voitures + avenue2.voitures
        self.bus = avenue1.bus + avenue2.bus
        self.camions = avenue1.camions + avenue2.camions

    def check_priorite(self):
        if self.Avenue1.points > self.Avenue2.points:
            return self.Avenue1
        else:
            return self.Avenue2
        
    def check_secondaire(self):
        if self.Avenue1.points < self.Avenue2.points:
            return self.Avenue1
        else:
            return self.Avenue2
    
# - - - - - - - - - - - - - - - - - - - - - -

def get_voie(connexion, feu_id):
    requete = """
    SELECT tv.nomTypeVehicule, count(dv.id) AS nombreVehicules 
    FROM app_detectionvehicule dv 
    INNER JOIN app_vehicule v ON dv.vehicule_id = v.idVehicule 
    INNER JOIN app_typevehicule tv ON v.typeVehicule_id = tv.idTypeVehicule 
    WHERE dv.detection_id IN (SELECT d.idDetection FROM app_detection d WHERE d.feu_id = ?) 
    GROUP BY tv.idTypeVehicule;
    """
    curseur = connexion.cursor()
    curseur.execute(requete, (feu_id,))
    resultats = curseur.fetchall()

    vehicules, voitures, bus, camions = 0, 0, 0, 0

    for type_vehicule, nombre in resultats:
        if type_vehicule.lower() == "voiture":
            voitures += nombre
        elif type_vehicule.lower() == "bus":
            bus += nombre
        elif type_vehicule.lower() == "camion":
            camions += nombre
        vehicules += nombre

    return Voie(feu_id, voitures, bus, camions)

def get_avenue(connexion, voie1_id, voie2_id):
    voie1 = get_voie(connexion, voie1_id)
    voie2 = get_voie(connexion, voie2_id)
    return Avenue(voie1, voie2)
    
def get_carrefour(connexion, avenue1_ids, avenue2_ids):
    avenue1 = get_avenue(connexion, *avenue1_ids)
    avenue2 = get_avenue(connexion, *avenue2_ids)
    return Carrefour4Rues(avenue1, avenue2)

# - - - - - - - - - - - - - - - - -

def temps():
    with sqlite3.connect(db_path) as connexion:

        print("\n")

        # Recuperation des voies et des avenues
        avenue1 = get_avenue(connexion, 1, 3)
        avenue2 = get_avenue(connexion, 2, 4)

        print(f"Avenue 1 : {avenue1.vehicules} vehicules, {avenue1.voitures} voitures, {avenue1.bus} bus, {avenue1.camions} camion, {avenue1.get_points_avenue()} points")
        print(f"Avenue 2 : {avenue2.vehicules} vehicules, {avenue2.voitures} voitures, {avenue2.bus} bus, {avenue2.camions} camion, {avenue2.get_points_avenue()} points")

        print("\n")

        # Recuperation du carrefour
        carrefour = get_carrefour(connexion, (1, 3), (2, 4))
        print(f"Carrefour : {carrefour.vehicules} vehicules")

        print("\n") 

        # Recuperation de la voie prioritaire
        avenue_prioritaire = carrefour.check_priorite()
        if avenue_prioritaire:
            print(f"Voie prioritaire : {avenue_prioritaire.vehicules} vehicules, {avenue_prioritaire.voitures} voitures, {avenue_prioritaire.bus} bus, {avenue_prioritaire.camions} camion, {avenue_prioritaire.get_points_avenue()} points")
            print(f"Temps du feu vert : {avenue_prioritaire.temps_vert} secondes")
            print(f"Temps du feu orange : {avenue_prioritaire.temps_orange} secondes")
            print(f"Temps du feu rouge : {avenue_prioritaire.temps_rouge} secondes")
            print("\n")
        else:
            print("Pas de voie prioritaire")

        print("\n")

        avenue_secondaire = carrefour.check_secondaire()

        if avenue_secondaire:
            print(f"Voie secondaire : {avenue_secondaire.vehicules} vehicules, {avenue_secondaire.voitures} voitures, {avenue_secondaire.bus} bus, {avenue_secondaire.camions} camion, {avenue_secondaire.get_points_avenue()} points")
            print(f"Temps du feu vert : {avenue_secondaire.temps_vert} secondes")
            print(f"Temps du feu orange : {avenue_secondaire.temps_orange} secondes")
            print(f"Temps du feu rouge : {avenue_secondaire.temps_rouge} secondes")
            print("\n")
        else:
            print("Pas de voie secondaires")

    return avenue_prioritaire, avenue_secondaire


class TrafficLightApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Feux Tricolores")
        self.geometry("400x600")

        self.canvas = tk.Canvas(self, width=400, height=600)
        self.canvas.pack()

        self.lights = []  # Stocke les références aux cercles des feux pour les animer
        self.current_light = 0  # Suivre l'état actuel des feux (0: rouge, 1: orange, 2: vert)

        self.prio_text = self.canvas.create_text(200, 270, text="", font=("Helvetica", 11), fill="black")
        self.second_text = self.canvas.create_text(200, 290, text="", font=("Helvetica", 11), fill="black")

        self.connexion = sqlite3.connect(db_path)

        # objet Carrefour4Rues
        self.carrefour = get_carrefour(self.connexion, (1, 3), (2, 4))

        # Dessiner les feux tricolores
        self.draw_traffic_lights()
        # Démarrer l'animation
        self.animate_lights()
        # Mise à jour de l'affichage du temps
        # self.update_countdown()

    def draw_traffic_light(self, i, x, y):
        """Dessine un seul feu tricolore à la position x, y."""
        light_ids = []
        # Créer la surface ovale en fond
        ca = self.canvas.create_rectangle(x, y, x + 100, y + 200, fill='gray', outline='black', width=4)

        # Créer le cercle pour le feu vert
        vert = self.canvas.create_oval(x + 15, y + 25, x + 85, y + 65, fill='green', outline='black', width=2)
        light_ids.append(vert)

        # Créer le cercle pour le feu orange
        orange = self.canvas.create_oval(x + 15, y + 85, x + 85, y + 125, fill='orange', outline='black', width=2)
        light_ids.append(orange)

        # Créer le cercle pour le feu rouge
        rouge = self.canvas.create_oval(x + 15, y + 145, x + 85, y + 185, fill='red', outline='black', width=2)
        light_ids.append(rouge)

        # Ajouter l'étiquette du feu
        libelle = self.canvas.create_text(x + 50, y + 10, font=("Helvetica", 11), fill="black")
        # libelle = self.canvas.create_text(x + 50, y + 10, text=f"Feu {i}", font=("Helvetica", 11), fill="black")
        return light_ids

    def draw_traffic_lights(self):
        """Dessine quatre feux tricolores."""
        positions = [(7, 50), (107, 50), (207, 50), (307, 50)]
        for i, pos in enumerate(positions):
            self.lights.append(self.draw_traffic_light(i+1, *pos))

    def update_countdown(self, temps1, temps2):
        # Cancel the previous schedule
        if hasattr(self, 'after_id'):
            self.after_cancel(self.after_id)

        # Decrement temps1 by 1
        if temps1 > 0:
            temps1 -= 1000
            self.canvas.itemconfig(self.prio_text, text=f"Durée de passage des feux prioritaires : {round(temps1/1000)} secondes")
            self.after_id = self.after(1000, self.update_countdown, temps1, temps2)  # Update every second
        else:
            # Decrement temps2 by 1
            if temps2 > 0:
                temps2 -= 1000
                self.canvas.itemconfig(self.second_text, text=f"Durée de passage des feux secondaires : {round(temps2/1000)} secondes")
                self.after_id = self.after(1000, self.update_countdown, temps1, temps2)  # Update every second
    
    def animate_lights(self):
        # Mise à jour des couleurs des feux
        for light_set in self.lights:
            # Réinitialiser toutes les lumières à gris
            for light in light_set:
                self.canvas.itemconfig(light, fill="black")
        
        if self.current_light == 0 or self.current_light == 2:  # Feux 1 et 3 sont verts
            self.canvas.itemconfig(self.lights[0][2], fill="green")  # Feu 1
            self.canvas.itemconfig(self.lights[2][2], fill="green")  # Feu 3
            self.canvas.itemconfig(self.lights[1][0], fill="red")  # Feu 2
            self.canvas.itemconfig(self.lights[3][0], fill="red")  # Feu 4
        else:  # Feux 2 et 4 sont verts
            self.canvas.itemconfig(self.lights[0][0], fill="red")  # Feu 1
            self.canvas.itemconfig(self.lights[2][0], fill="red")  # Feu 3
            self.canvas.itemconfig(self.lights[1][2], fill="green")  # Feu 2
            self.canvas.itemconfig(self.lights[3][2], fill="green")  # Feu 4


        avenue_prioritaire = self.carrefour.check_priorite()
        avenue_secondaire = self.carrefour.check_secondaire()

        temps_vert_prio = avenue_prioritaire.temps_vert * 1000
        temps_rouge_prio = avenue_prioritaire.temps_rouge * 1000
        temps_orange_prio = avenue_prioritaire.temps_orange * 1000
        
        temps_vert_second = avenue_secondaire.temps_vert * 1000
        temps_rouge_second = avenue_secondaire.temps_rouge * 1000
        temps_orange_second = avenue_secondaire.temps_orange * 1000

        # Passer à la lumière suivante
        self.current_light = (self.current_light + 1) % 4

        # Appeler cette fonction à nouveau après un premier délai
        self.after(temps_vert_prio, self.animate_lights)

        self.update_countdown(temps_vert_prio, temps_vert_second)

def main_algo():
    connexion = sqlite3.connect(db_path)
    with connexion:
        app = TrafficLightApp()
        app.mainloop()

# RUN

if __name__ == "__main__":
    main_algo()

