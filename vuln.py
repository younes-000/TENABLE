# ce script va nous permettre d''identifier les chemins d’attaque ouverts par priorité


import requests
import configparser
import logging
import json
import time


# le fichier config.ini
config = configparser.ConfigParser() 
config.read("config.ini")
ACCESS_KEY = config["API"]["ACCESS_KEY"]
SECRET_KEY = config["API"]["SECRET_KEY"]
url = "https://cloud.tenable.com/vulns/export/status"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-ApiKeys": f"accessKey={ACCESS_KEY}; secretKey={SECRET_KEY}"
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    
    
    with open("status.json", "w") as file:
        json.dump(data, file, indent=4)
    
  
    open("status22.json", "w").close()
    
  
    for export in data.get("exports", []):
        export_id = export.get("uuid")
        state = export.get("filters").get("state")
        severité = export.get("filters").get("severity")
        if state == ["OPEN"] and severité == ["HIGH", "CRITICAL"] :
            
            print(f"Export ID: {export_id} - State: {state}")
            

            with open("result.json", "a") as file:
                export_info = {"export_id": export_id, "status": state , "severity": severité}
                file.write(json.dumps(export_info) + "\n")
