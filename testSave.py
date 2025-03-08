import WebScrape
import Data

if __name__ == "__main__":
# for id in Data.get_ids():
    id = "74463010"
    product = WebScrape.Page(id)
    if not product.connect()["code"]:
        name = product.get_product_name()
        if not name["code"]:
            name = name["result"]
            amount = product.get_comments_amount()
            if not amount["code"]:
                amount = amount["result"]
            else: amount = None
            comments = product.format_comments()
            if not comments["code"]:
                comments = comments["result"]
            else:
                comments = None
        
            Data.save(id, name, amount, comments)
        else: print("bad code")