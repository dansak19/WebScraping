import WebScrape
import Data

if __name__ == "__main__":
    ids = Data.get_ids()
    data = []
    for id in ids:
        d = Data.get(id)
        d["id"] = id
        data.append(d)
        
    print(data)
        
    for i in data:
        print()
        print(i["id"])
        print(i["name"])