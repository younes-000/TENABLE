import json
import requests
import sys
import time
import configparser
from datetime import datetime

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

# objectif recuperer les regles dynamic et static qui permettent de pouvoir attribuer des tags au assets automatiquement

url = "https://cloud.tenable.com/tags/values" # url pour récupérer les uuid des assets
response = requests.get(url, headers=headers) #  la requete
data = response.json() # la reponse en json
value_info_list = [] # le dictionnaire pour les uuid
if "values" in data and data["values"]: # condition si les valeurs sont présentes 
    for value in data.get("values", []): # boucle pour récupérer les valeurs
        value_info_list.append({ # ajout des valeurs dans le dictionnaire
            "uuid": value.get("uuid") # j'ajoute la valeur uuid dans le dictionnaire de mes assets
        })
else:
    print("Aucune values trouvé.") # si rien n'est trouvé
    sys.exit(1) # break


all_data = [] # le dictionnaire pour récupérer les données et pouvoir les mettre dans le json

for asset in value_info_list: # boucle pour récupérer les uuid des assets
    value_uuid = asset["uuid"] # je récupère l'uuid de l'asset
    url2 = f"https://cloud.tenable.com/tags/values/{value_uuid}" # url pour récupérer les tags
    response2 = requests.get(url2, headers=headers) # requete pour récupérer les tags
    json_data = response2.json() # fichier response en json
    all_data.append(json_data) # j'ajoute les données dans le dictionnaire all_data

with open('Regles_static_dynamic.json', 'w', encoding='utf-8') as file: # j'ouvre un fichier json pour mettre les données
    json.dump(all_data, file, indent=4, ensure_ascii=False) # j'ajoute les données dans le fichier json
