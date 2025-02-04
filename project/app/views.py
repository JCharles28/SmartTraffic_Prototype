
import datetime
from django.utils import timezone
from django.shortcuts import render
from django.core.serializers import serialize
from app.models import *
import json
from django.db.models import Count
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

# --- Affichage des templates ---

def index(request):
    # Récupération des données Chart (1)
    nbDetection = list(Detection.objects.values('rue__nomRue').annotate(nbDetection=Count('rue_id')).order_by())
    nomRue = [sublist['rue__nomRue'] for sublist in nbDetection]
    nbDetection = [sublist['nbDetection'] for sublist in nbDetection]

    # Récupération des données Chart (2)
    nbDetection2 = list(
        DetectionVehicule.objects
        .values('vehicule__typeVehicule__nomTypeVehicule')
        .annotate(nbDetection=Count('detection_id'))
        .order_by()
    )
    typeVehicule = [sublist['vehicule__typeVehicule__nomTypeVehicule'] for sublist in nbDetection2]
    nbDetection2 = [sublist['nbDetection'] for sublist in nbDetection2]
    
    # Récupération des données Chart (3)

    current_hour = timezone.now().hour

    # nbDetectionJournaliere = Detection.objects.filter(temps__dateHeure__hour=current_hour).count()
    temps = datetime.datetime.now()
    heures = []
    for i in range(24):
        heures.append(temps.replace(hour=i, minute=0, second=0, microsecond=0))
    tabDetectionsJournaliere = [random.randint(0, 85) for _ in range(24)]
    
    # Récupération des données Chart (5)
    nbDetection5 = list(Detection.objects.values('feu__nomFeu').annotate(nbDetection5=Count('feu_id')).order_by())
    nomFeu = [sublist['feu__nomFeu'] for sublist in nbDetection5]
    nbDetection5 = [sublist['nbDetection5'] for sublist in nbDetection5]
    
    # Récupération des données Chart (6)
    def rejetC02():
        rejetC02, rejetC02Voiture, rejetC02Camion, rejetC02Bus = 0, 0, 0, 0
        for i in range(len(nbDetection2)):
            # si le type de véhicule est "Voiture"
            if typeVehicule[i] == "Voiture":
                # on récupère le nombre de détection de ce type de véhicule
                rejetC02Voiture = nbDetection2[i] * 8.7
            # si le type de véhicule est "Camion"
            elif typeVehicule[i] == "Camion":
                # on récupère le nombre de détection de ce type de véhicule
                rejetC02Camion = nbDetection2[i] * 18
            # si le type de véhicule est "Bus"
            elif typeVehicule[i] == "Bus":
                # on récupère le nombre de détection de ce type de véhicule
                rejetC02Bus = nbDetection2[i] * 10.5
            else:
                print("Type de véhicule non pris en compte")

            rejetC02 = rejetC02Voiture + rejetC02Camion + rejetC02Bus
        
        if rejetC02 > 0:
            return rejetC02
        else:
            return 0

    def rejetC02partype():
        tabrejetC02partype = []
        rejetC02Voiture, rejetC02Camion, rejetC02Bus = 0, 0, 0
        for i in range(len(nbDetection2)):
            # si le type de véhicule est "Voiture"
            if typeVehicule[i] == "Voiture":
                # on récupère le nombre de détection de ce type de véhicule
                rejetC02Voiture = nbDetection2[i] * 8.7
                if rejetC02Voiture > 0:
                    tabrejetC02partype.append(rejetC02Voiture)
                else: 
                    tabrejetC02partype.append(0)
            # si le type de véhicule est "Camion"
            elif typeVehicule[i] == "Camion":
                # on récupère le nombre de détection de ce type de véhicule
                rejetC02Camion = nbDetection2[i] * 18
                if rejetC02Camion > 0:
                    tabrejetC02partype.append(rejetC02Camion)
                else: tabrejetC02partype.append(0)
            # si le type de véhicule est "Bus"
            elif typeVehicule[i] == "Bus":
                # on récupère le nombre de détection de ce type de véhicule
                rejetC02Bus = nbDetection2[i] * 10.5
                if rejetC02Bus > 0:
                    tabrejetC02partype.append(rejetC02Bus)
                else: tabrejetC02partype.append(0)
            else:
                print("Type de véhicule non pris en compte")
        
        return tabrejetC02partype

    # Affichage console
    print("--------------------")
    print("Chart 1:")
    print(nomRue)
    print(nbDetection)
    print("--------------------")
    print("Chart 2:")
    print(typeVehicule)
    print(nbDetection2)
    print("--------------------")
    print("Chart 3:")
    print("Nombre de détection : ", tabDetectionsJournaliere)
    tabHeures = []
    for i in range(24):
        tabHeures.append(heures[i].hour)
    print("Les heures de la journée : ", tabHeures)
    print("--------------------")
    print("Chart 5:")
    print(nomFeu)
    print(nbDetection5)
    print("--------------------")
    print("Chart 6:")
    print("rejet de CO2 : ", rejetC02())
    print("--------------------")
    print("Chart 7:")
    print("rejet de CO2 par type de véhicule : ", rejetC02partype())

    # JSON
    rues_json = json.dumps(nomRue, ensure_ascii=False)
    nbDetection_json = json.dumps(nbDetection, ensure_ascii=False)
    typeVehicule_json = json.dumps(typeVehicule, ensure_ascii=False)
    nbDetection2_json = json.dumps(nbDetection2, ensure_ascii=False)
    tabDetectionsJournaliere_json = json.dumps(tabDetectionsJournaliere, ensure_ascii=False)
    tabHeures_json = json.dumps(tabHeures, ensure_ascii=False)
    nomFeu_json = json.dumps(nomFeu, ensure_ascii=False)
    nbDetection5_json = json.dumps(nbDetection5, ensure_ascii=False)
    rejetC02_json = json.dumps(rejetC02(), ensure_ascii=False)
    rejetC02partype_json = json.dumps(rejetC02partype(), ensure_ascii=False)

 
    return render(
        request, 'index.html',
        {
        'rue': rues_json, 
        'nbDetection': nbDetection_json,
        'typeVehicule': typeVehicule_json, 
        'nbDetection2': nbDetection2_json,
        'nbDetection3': tabDetectionsJournaliere_json,
        'tabHeures': tabHeures_json,
        'feu': nomFeu_json,
        'nbDetection5': nbDetection5_json,
        'rejetC02': rejetC02_json,
        'rejetC02partype': rejetC02partype_json,
        }
    )

def carte(request):
    # Récupération des données Chart (1)
    nbDetection = list(Detection.objects.values('feu__nomFeu').annotate(nbDetection=Count('feu_id')).order_by())
    nomFeu = [sublist['feu__nomFeu'] for sublist in nbDetection]
    nbDetection = [sublist['nbDetection'] for sublist in nbDetection]
    
    print("--------------------")
    print("Detections on map:")
    print(nomFeu)
    print(nbDetection)
    print("--------------------")

    # JSON
    nomFeu_json = json.dumps(nomFeu, ensure_ascii=False)
    nbDetection_json = json.dumps(nbDetection, ensure_ascii=False)
    
    return render(request, 'carte.html', {
      'feu': nomFeu_json, 
      'nbDetection': nbDetection_json,
    })

def accueil(request):
    return render(request, 'accueil.html')

@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        value = data.get('value')

        if value > 50:
            send_mail(
                'Attention',
                'Une valeur est supérieure à 50',
                'charlesmcmpro@gmail.com',
                ['charifmcm@gmail.com'],
                fail_silently=False,
            )

        return JsonResponse({'status': 'ok'})