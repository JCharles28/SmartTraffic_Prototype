
CREATE TABLE IF NOT EXISTS "app_etatfeu" (
	"idEtatFeu"	integer NOT NULL,
	"nomEtatFeu"	varchar(50) NOT NULL,
	PRIMARY KEY("idEtatFeu" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "app_rue" (
	"idRue"	integer NOT NULL,
	"nomRue"	varchar(50) NOT NULL,
	PRIMARY KEY("idRue" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "app_temps" (
	"idTemps"	integer NOT NULL,
	"dateHeure"	datetime NOT NULL,
	"semaine"	integer NOT NULL,
	"jourSemaine"	varchar(50) NOT NULL,
	"isWeekEnd"	bool NOT NULL,
	PRIMARY KEY("idTemps" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "app_typevehicule" (
	"idTypeVehicule"	integer NOT NULL,
	"nomTypeVehicule"	varchar(50) NOT NULL,
	PRIMARY KEY("idTypeVehicule" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "app_detection" (
	"idDetection"	integer NOT NULL,
	"rue_id"	integer,
	"temps_id"	integer NOT NULL,
	"feu_id"	integer,
	FOREIGN KEY("feu_id") REFERENCES "app_feu"("idFeu") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("rue_id") REFERENCES "app_rue"("idRue") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("temps_id") REFERENCES "app_temps"("idTemps") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("idDetection" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "app_vehicule" (
	"idVehicule"	integer NOT NULL,
	"nomVehicule"	varchar(50) NOT NULL,
	"typeVehicule_id"	integer NOT NULL,
	FOREIGN KEY("typeVehicule_id") REFERENCES "app_typevehicule"("idTypeVehicule") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("idVehicule" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "app_detectionvehicule" (
	"id"	integer NOT NULL,
	"detection_id"	integer NOT NULL,
	"vehicule_id"	integer NOT NULL,
	FOREIGN KEY("vehicule_id") REFERENCES "app_vehicule"("idVehicule") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("detection_id") REFERENCES "app_detection"("idDetection") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "app_feu" (
	"idFeu"	integer NOT NULL,
	"nomFeu"	varchar(50) NOT NULL,
	"rue_id"	integer NOT NULL,
	"etatFeu_id"	integer NOT NULL,
	FOREIGN KEY("rue_id") REFERENCES "app_rue"("idRue") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("etatFeu_id") REFERENCES "app_etatfeu"("idEtatFeu") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("idFeu" AUTOINCREMENT)
);
