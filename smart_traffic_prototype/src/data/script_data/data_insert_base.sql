-- Inserting into Rue
INSERT INTO app_rue (idRue ,nomRue) VALUES (1, "Route d'Orléans");
INSERT INTO app_rue (idRue, nomRue) VALUES (2, "Route de Massy");

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
INSERT INTO app_feu (idFeu, nomFeu, rue_id, etatFeu_id) VALUES (2, 'Feu2', 2, 1);
INSERT INTO app_feu (idFeu, nomFeu, rue_id, etatFeu_id) VALUES (3, 'Feu3', 1, 2);
INSERT INTO app_feu (idFeu, nomFeu, rue_id, etatFeu_id) VALUES (4, 'Feu4', 2, 2);
