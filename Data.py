import json
import csv
import xlsxwriter
import os
import re

class Database():
    def __init__(self, id = None):
        self.id = id
    
    def save(self, name, amount, opinions):
        self.data = {"name": name,
                "opinions amount": amount,
                "opinions": opinions}
    
        self.path = f"data/{self.id}.json"
    
        with open(self.path, "w") as file:
            json.dump(self.data, file, indent=4)
        
    def get(self):
        self.path = f"data/{self.id}.json"
    
        with open(self.path, "r") as file:
            data = json.load(file)
    
        return data

    def get_ids(self):
        self.path = "data/"
        self.files = os.listdir(self.path)
        self.ids = re.findall("\\d+\\.json", str(self.files))
        self.ids = [id[:-5] for id in self.ids]
    
        return self.ids

    def delete(self):
        self.path = f"data/{self.id}.json"
        try: 
            os.unlink(self.path)
            return 0
        except:
            return 1

class Download():
    def __init__(self, id):
        self.id = id
        self.product = Database(self.id)
        self.data = self.product.get()
    
    def delete_download(self):
        path = "download/"
        files = os.listdir(path)
        for file in files:
            os.unlink(path + file)

    def json(self):
        self.delete_download()
    
        path = f"download/{self.id}.json"
    
        with open(path, "w") as file:
            json.dump(self.data, file, indent=4)
        
        return path
    

    def xlsx(self):
        self.delete_download()
        
        path = f"download/{id}.xlsx"
        
        book = xlsxwriter.Workbook(path)
        sheet1 = book.add_worksheet("about")
        
        
        sheet1.write(0, 0, "Id:")
        sheet1.write(0, 1, self.id)
        sheet1.write(1, 0, "Name:")
        sheet1.write(1, 1, self.data["name"])
        sheet1.write(2, 0, "Opinions amount:")
        sheet1.write(2, 1, self.data["opinions amount"])
        
        if self.data["opinions"]:
            sheet2 = book.add_worksheet("opinions")
            for i, key in enumerate(self.data["opinions"][0].keys()):
                sheet2.write(0, i, key)
            for i, opinion in enumerate(self.data["opinions"]):
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

    def csv(self):
        self.delete_download()
        
        path = f"download/{self.id}.csv"
        
        with open(path, "w") as file:
            csv_file = csv.writer(file)
        
            csv_file.writerow(["id:", self.id])
            csv_file.writerow(["name:", self.data["name"]])
        
            if self.data["opinions amount"]:
                csv_file.writerow(["opinions amount:", self.data["opinions amount"]])
            else: 
                csv_file.writerow(["opinions amount:", 0])
            
            if self.data["opinions"]:
                csv_file.writerow("")
                csv_file.writerow(self.data["opinions"][0].keys())

                for opinion in self.data["opinions"]:
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