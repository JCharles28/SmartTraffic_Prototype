--- Lister toutes les tables de la base en question
-- SELECT name FROM sqlite_master WHERE type='table';

--- Désactiver temporairement les contraintes des clés étrangères
PRAGMA foreign_keys = OFF;

--- Supprimer toutes les données des tables en respectant les contraintes des clés étrangères
DELETE FROM app_detectionvehicule;  -- Supprimer d'abord car dépend de Detection et Vehicule
DELETE FROM app_detection;          -- Supprimer ensuite car dépend de Rue et Temps
DELETE FROM app_vehicule;           -- Supprimer ensuite car dépend de TypeVehicule
DELETE FROM app_feu;                -- Supprimer ensuite car dépend de Rue et EtatFeu
DELETE FROM app_etatfeu;            -- Supprimer après Feu
DELETE FROM app_rue;                -- Supprimer après Feu et Detection
DELETE FROM app_typevehicule;       -- Supprimer après Vehicule
DELETE FROM app_temps;              -- Supprimer après Detection

--- Réactiver les contraintes des clés étrangères
PRAGMA foreign_keys = ON;
