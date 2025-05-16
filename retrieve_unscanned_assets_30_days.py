from datetime import datetime, timedelta
import requests
import json
import time
import os
import configparser

# ce script va permettre de récupérer les actifs non scannés depuis plus de 30 jours


# permet de stocker les credentials 
config = configparser.ConfigParser()
config.read("config.ini") # le fichier config

ACCESS_KEY = config["API"]["ACCESS_KEY"] #access key
SECRET_KEY = config["API"]["SECRET_KEY"] #secret key


headers = { 
    "Accept": "application/json",
    "X-ApiKeys": f"accessKey={ACCESS_KEY}; secretKey={SECRET_KEY}"
}


url = "https://cloud.tenable.com/assets" # url de l'api utilisé 
file_path = "old_assets2.json" # pour la création du fichier ou nous mettrons les données 

# on récupère l'api
response = requests.get(url, headers=headers) # j'envoie une requete get pour récupérer tous les actifs 
threshold_date = datetime.utcnow() - timedelta(days=30)  # Seuil : 30 jours


if os.path.exists(file_path): # verification du fichier json
    with open(file_path, "r", encoding="utf-8") as file: # on l'ouvre en mode read
        try:
            existing_data = json.load(file) # si le fichier existe deja 
        except json.JSONDecodeError: # en cas d'erreur  si le fichier est mal formé
            existing_data = {"old_assets": []} # on recrée le fichier
else:
    existing_data = {"old_assets": []} # si le fichier n'a jamais été crée on le recrée


if response.status_code == 200: # code 200 le staus est juste et la page s'affiche
    assets = response.json().get("assets", [])  # je récupère la zliste des actifs dans la rubrique asset
    old_assets = []  # Liste des anciens actifs  ( ou on mettra les assets de -30 jours)

    for asset in assets: # boucle 
        asset_id = asset.get("id", "Unknown")  # on récupère l'id de chaque machine
        last_seen_str = asset.get("last_seen") # vérifie si l'asset a été vu

        if last_seen_str: 
            try:
                last_seen = datetime.strptime(last_seen_str, "%Y-%m-%dT%H:%M:%S.%fZ") # compare la date
                if last_seen < threshold_date: # comparaison
                    
                    hostname_list = asset.get("hostname", [])  # Liste de hostnames
                    ip_list = asset.get("ipv4", [])  # Liste d'adresses IPv4

                    old_asset_data = {
                        "id": asset_id,
                        "hostname": hostname_list[0] if hostname_list else "Unknown",  # Vérifie si la liste est vide
                        "ip": ip_list[0] if ip_list else "Unknown"  # Vérifie si la liste est vide
                    }
                    old_assets.append(old_asset_data) # on ajoute les données 
            except ValueError:
                print(f"Format de date invalide pour l'actif {asset_id}") # en cas d'erreur

   
    existing_data["old_assets"].extend(old_assets) # ajout 

    with open(file_path, "w", encoding="utf-8") as file: # ouverture du fichier 
        json.dump(existing_data, file, indent=4, ensure_ascii=False) # segmente mon fichier json

    print(f"{len(old_assets)} actifs non scannés depuis plus de 30 jours enregistrés dans {file_path}.") #
else:
    print(f"Erreur {response.status_code} lors de la récupération des actifs : {response.text}")
