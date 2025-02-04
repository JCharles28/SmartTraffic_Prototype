# Smart Traffic - Application de détection & Plateforme web

## Mode d'emploi

### Créer et activer un environnement virtuel
``` bash
python -m env myenvironnement
```

### Activer l'environnement
- Sur `Windows`
    ``` bash
    .\myenvironnement\Scripts\activate
    ```
- Sur `Linux`
    ``` bash
    source myenvironnement/bin/activate
    ```

### Télécharger les modules nécessaires
``` bash
pip install -r requirements.txt
```
---
### Lancer le serveur web (**plateforme de montoring**)
```bash
python project/manage.py runserver
```

#### or

### Lancer l'**application de détection**
``` bash
streamlit run .\smart_traffic_prototype\src\application.py --server.maxUploadSize=500
```


