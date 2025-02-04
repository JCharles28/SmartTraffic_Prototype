-- Inserting into Temps
INSERT INTO app_temps (idTemps, dateHeure, semaine, jourSemaine, isWeekEnd) VALUES (1, '2023-12-10 00:00:00', 49, 'Dimanche', TRUE);
INSERT INTO app_temps (idTemps, dateHeure, semaine, jourSemaine, isWeekEnd) VALUES (2, '2023-12-10 01:00:00', 49, 'Dimanche', TRUE);
INSERT INTO app_temps (idTemps, dateHeure, semaine, jourSemaine, isWeekEnd) VALUES (3, '2023-12-10 02:00:00', 49, 'Dimanche', TRUE);
INSERT INTO app_temps (idTemps, dateHeure, semaine, jourSemaine, isWeekEnd) VALUES (4, '2023-12-10 03:00:00', 49, 'Dimanche', TRUE);
INSERT INTO app_temps (idTemps, dateHeure, semaine, jourSemaine, isWeekEnd) VALUES (5, '2023-12-10 04:00:00', 49, 'Dimanche', TRUE);
INSERT INTO app_temps (idTemps, dateHeure, semaine, jourSemaine, isWeekEnd) VALUES (6, '2023-12-11 05:00:00', 50, 'Lundi', FALSE);
INSERT INTO app_temps (idTemps, dateHeure, semaine, jourSemaine, isWeekEnd) VALUES (7, '2023-12-11 06:00:00', 50, 'Lundi', FALSE);
INSERT INTO app_temps (idTemps, dateHeure, semaine, jourSemaine, isWeekEnd) VALUES (8, '2023-12-11 07:00:00', 50, 'Lundi', FALSE);
INSERT INTO app_temps (idTemps, dateHeure, semaine, jourSemaine, isWeekEnd) VALUES (9, '2023-12-11 08:00:00', 50, 'Lundi', FALSE);
INSERT INTO app_temps (idTemps, dateHeure, semaine, jourSemaine, isWeekEnd) VALUES (10, '2023-12-11 09:00:00', 50, 'Lundi', FALSE);

-- Inserting into Rue
INSERT INTO app_rue (idRue ,nomRue) VALUES (1, "Route d'Orléans");
INSERT INTO app_rue (idRue, nomRue) VALUES (2, "Route de Massy");

-- Inserting into Detection
INSERT INTO app_detection (idDetection, rue_id, temps_id) VALUES (1, 1, 1);
INSERT INTO app_detection (idDetection, rue_id, temps_id) VALUES (2, 1, 2);
INSERT INTO app_detection (idDetection, rue_id, temps_id) VALUES (3, 2, 3);
INSERT INTO app_detection (idDetection, rue_id, temps_id) VALUES (4, 2, 4);
INSERT INTO app_detection (idDetection, rue_id, temps_id) VALUES (5, 1, 5);
INSERT INTO app_detection (idDetection, rue_id, temps_id) VALUES (6, 1, 6);
INSERT INTO app_detection (idDetection, rue_id, temps_id) VALUES (7, 2, 7);
INSERT INTO app_detection (idDetection, rue_id, temps_id) VALUES (8, 2, 8);
INSERT INTO app_detection (idDetection, rue_id, temps_id) VALUES (9, 1, 9);
INSERT INTO app_detection (idDetection, rue_id, temps_id) VALUES (10, 1, 10);


-- Inserting into Vehicule
INSERT INTO app_vehicule (idVehicule, nomVehicule, typevehicule_id) VALUES (1, 'Vehicule1', 1);
INSERT INTO app_vehicule (idVehicule, nomVehicule, typevehicule_id) VALUES (2, 'Vehicule2', 2);
INSERT INTO app_vehicule (idVehicule, nomVehicule, typevehicule_id) VALUES (3, 'Vehicule3', 3);
INSERT INTO app_vehicule (idVehicule, nomVehicule, typevehicule_id) VALUES (4, 'Vehicule4', 4);
INSERT INTO app_vehicule (idVehicule, nomVehicule, typevehicule_id) VALUES (5, 'Vehicule5', 1);
INSERT INTO app_vehicule (idVehicule, nomVehicule, typevehicule_id) VALUES (6, 'Vehicule6', 2);
INSERT INTO app_vehicule (idVehicule, nomVehicule, typevehicule_id) VALUES (7, 'Vehicule7', 3);
INSERT INTO app_vehicule (idVehicule, nomVehicule, typevehicule_id) VALUES (8, 'Vehicule8', 4);
INSERT INTO app_vehicule (idVehicule, nomVehicule, typevehicule_id) VALUES (9, 'Vehicule9', 1);
INSERT INTO app_vehicule (idVehicule, nomVehicule, typevehicule_id) VALUES (10, 'Vehicule10', 2);

-- Inserting into TypeVehicule 
INSERT INTO app_typevehicule (idTypeVehicule, nomTypeVehicule) VALUES (1, 'Voiture');
INSERT INTO app_typevehicule (idTypeVehicule, nomTypeVehicule) VALUES (2, 'Camion');
INSERT INTO app_typevehicule (idTypeVehicule, nomTypeVehicule) VALUES (3, 'Bus');
INSERT INTO app_typevehicule (idTypeVehicule, nomTypeVehicule) VALUES (4, 'Moto');

-- Inserting into etatFeu 
INSERT INTO app_etatfeu (idEtatFeu, nomEtatFeu) VALUES (1, 'Vert');
INSERT INTO app_etatfeu (idEtatFeu, nomEtatFeu) VALUES (2, 'Rouge');
INSERT INTO app_etatfeu (idEtatFeu, nomEtatFeu) VALUES (3, 'Orange');
INSERT INTO app_etatfeu (idEtatFeu, nomEtatFeu) VALUES (4, 'Eteint');


-- Inserting into Feu
INSERT INTO app_feu (idFeu, nomFeu, rue_id, etatFeu_id) VALUES (1, 'Feu1', 1, 1);
INSERT INTO app_feu (idFeu, nomFeu, rue_id, etatFeu_id) VALUES (2, 'Feu2', 1, 1);
INSERT INTO app_feu (idFeu, nomFeu, rue_id, etatFeu_id) VALUES (3, 'Feu3', 2, 2);
INSERT INTO app_feu (idFeu, nomFeu, rue_id, etatFeu_id) VALUES (4, 'Feu4', 2, 2);


-- Inserting into DetectionVehicule
INSERT INTO app_detectionvehicule (id, detection_id, vehicule_id) VALUES (1, 1, 1);
INSERT INTO app_detectionvehicule (id, detection_id, vehicule_id) VALUES (2, 2, 2);
INSERT INTO app_detectionvehicule (id, detection_id, vehicule_id) VALUES (3, 3, 3);
INSERT INTO app_detectionvehicule (id, detection_id, vehicule_id) VALUES (4, 4, 4);
INSERT INTO app_detectionvehicule (id, detection_id, vehicule_id) VALUES (5, 5, 5);
INSERT INTO app_detectionvehicule (id, detection_id, vehicule_id) VALUES (6, 6, 6);
INSERT INTO app_detectionvehicule (id, detection_id, vehicule_id) VALUES (7, 7, 7);
INSERT INTO app_detectionvehicule (id, detection_id, vehicule_id) VALUES (8, 8, 8);
INSERT INTO app_detectionvehicule (id, detection_id, vehicule_id) VALUES (9, 9, 9);
INSERT INTO app_detectionvehicule (id, detection_id, vehicule_id) VALUES (10, 10, 10);
