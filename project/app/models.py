from django.db import models

class Temps(models.Model):
    idTemps = models.AutoField(primary_key=True)
    dateHeure = models.DateTimeField()
    semaine = models.IntegerField()
    jourSemaine = models.CharField(max_length=50)
    isWeekEnd = models.BooleanField()

class Rue(models.Model):
    idRue = models.AutoField(primary_key=True)
    nomRue = models.CharField(max_length=50)

class EtatFeu(models.Model):
    idEtatFeu = models.AutoField(primary_key=True)
    nomEtatFeu = models.CharField(max_length=50)

class Feu(models.Model):
    idFeu = models.AutoField(primary_key=True)
    nomFeu = models.CharField(max_length=50)
    rue = models.ForeignKey(Rue, on_delete=models.CASCADE, related_name='feux')
    etatFeu = models.ForeignKey(EtatFeu, on_delete=models.CASCADE)

class Detection(models.Model):
    idDetection = models.AutoField(primary_key=True)
    rue = models.ForeignKey(Rue, on_delete=models.SET_NULL, null=True)
    temps = models.ForeignKey(Temps, on_delete=models.CASCADE)
    feu = models.ForeignKey(Feu, on_delete=models.SET_NULL, null=True)

class TypeVehicule(models.Model):
    idTypeVehicule = models.AutoField(primary_key=True)
    nomTypeVehicule = models.CharField(max_length=50)

class Vehicule(models.Model):
    idVehicule = models.AutoField(primary_key=True)
    nomVehicule = models.CharField(max_length=50)
    typeVehicule = models.ForeignKey(TypeVehicule, on_delete=models.CASCADE, related_name='vehicules')

class DetectionVehicule(models.Model):
    detection = models.ForeignKey(Detection, on_delete=models.CASCADE)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)