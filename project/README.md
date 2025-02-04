# Manuel Web

## Activer l'environnement
``` bash
py -m venv myworld
```
`or`
```bash
myworld\Scripts\activate.bat
```
___
## Migration de la base de données
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
___
## Lancer le serveur web
```bash
python project/manage.py runserver
```
___
## Créer un accès **administrateur**
```bash
python project/manage.py createsuperuser
```