#  ce script permet de pouvoir récupérer les vulnérabilités fixed sur teenable

import json
import requests
import configparser

# Config de mon api
config = configparser.ConfigParser()
config.read("config.ini") # fichier ini
ACCESS_KEY = config["API"]["ACCESS_KEY"] # access key
SECRET_KEY = config["API"]["SECRET_KEY"] # secret key

headers = { # connexion
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-ApiKeys": f"accessKey={ACCESS_KEY}; secretKey={SECRET_KEY}" # keys
}


asset_id = input("Entrez l'ID de l'actif: ") # il faut rentrer l'id de la machine
# ici les filtres permettent de récupérer la valeur fixed pour les vulnérabilitées d'un actif 
url = f"https://cloud.tenable.com/workbenches/assets/{asset_id}/vulnerabilities?filter.0.filter=tracking.state&filter.0.quality=eq&filter.0.value=Fixed" 
response = requests.get(url, headers=headers) # envoie de la requete 

# Enregistrement du résultat sous forme de fichier JSON
with open('fixed_vulnerabilities.json', 'w', encoding='utf-8') as file:
    json.dump(response.json(), file, indent=4, ensure_ascii=False)

print("Les données ont été enregistrées ")
