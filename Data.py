import json
import os
import re

def save(id, name, amount, opinions):
    data = {"name": name,
            "opinions amount": amount,
            "opinions": opinions}
    
    path = f"data/{id}.json"
    
    with open(path, "w") as file:
        json.dump(data, file, indent=4)
        
def get(id):
    path = f"data/{id}.json"
    
    with open(path, "r") as file:
        data = json.load(file)
    
    return data

def get_ids():
    path = "data/"
    files = os.listdir(path)
    ids = re.findall("\\d+\\.json", str(files))
    ids = [id[:-5] for id in ids]
    
    return ids