import json
import csv
import xlsxwriter
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

def delete(id):
    path = f"data/{id}.json"
    try: 
        os.unlink(path)
        return 0
    except:
        return 1

def delete_download():
    path = "download/"
    files = os.listdir(path)
    for file in files:
        os.unlink(path + file)

def save_json(id):
    delete_download()
    data = get(id)
    
    path = f"download/{id}.json"
    
    with open(path, "w") as file:
        json.dump(data, file, indent=4)
        
    return path
    

def save_xlsx(id):
    delete_download()
    data = get(id)
    
    path = f"download/{id}.xlsx"
    
    book = xlsxwriter.Workbook(path)
    sheet1 = book.add_worksheet("about")
    
    
    sheet1.write(0, 0, "Id:")
    sheet1.write(0, 1, id)
    sheet1.write(1, 0, "Name:")
    sheet1.write(1, 1, data["name"])
    sheet1.write(2, 0, "Opinions amount:")
    sheet1.write(2, 1, data["opinions amount"])
    
    if data["opinions"]:
        sheet2 = book.add_worksheet("opinions")
        for i, key in enumerate(data["opinions"][0].keys()):
            sheet2.write(0, i, key)
        for i, opinion in enumerate(data["opinions"]):
            for j, value in enumerate(opinion.values()):
                if str(type(value)) == "<class 'list'>":
                    l = value
                    value = ''
                    for r in l:
                        value += f"{r} "
                sheet2.write(i + 1, j, value)
    else: sheet1.write(2, 1, 0)
            
    
    book.close()
    
    return path

def save_csv(id):
    delete_download()
    
    data = get(id)
    
    path = f"download/{id}.csv"
    
    with open(path, "w") as file:
        csv_file = csv.writer(file)
        
        csv_file.writerow(["id:", id])
        csv_file.writerow(["name:", data["name"]])
        
        if data["opinions amount"]:
            csv_file.writerow(["opinions amount:", data["opinions amount"]])
        else: 
            csv_file.writerow(["opinions amount:", 0])
            
        if data["opinions"]:
            csv_file.writerow("")
            csv_file.writerow(data["opinions"][0].keys())
            
            for opinion in data["opinions"]:
                review = []
                for k, v in opinion.items():
                    if (k == "advantages" or k == "disadvantages") and v:
                        l = v
                        v = ''
                        for r in l:
                            v += f"{r} "
                        v = v[:-1]
                            
                    review.append(v)
                    
                csv_file.writerow(review)
                
    return path
        
if __name__ == "__main__":
    save_csv("66786315")