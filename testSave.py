import WebScrape
import Data

if __name__ == "__main__":
    id = "135759416"
    product = WebScrape.Page(id)
    name = product.get_product_name()
    if name:
        comments = product.format_comments()
    else:
        comments = None
        
    Data.save(id, name, comments)
