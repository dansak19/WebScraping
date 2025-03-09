from flask import Flask, render_template, request, redirect, url_for
import WebScrape
import Data

app = Flask(__name__)

# -------

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/extract', methods=['GET'])
def extract():
    return render_template('extraction.html')

@app.route('/extract', methods=['POST'])
def start_extraction():
    code = request.form['product_id']
    product = WebScrape.Page(code)
    check = product.connect()
    name = product.get_product_name()
    if not check['code'] and not name['code']:
        name = name['result']
        save_product(str(code))
        return redirect(url_for('product_page', product_id=code))
    else: 
        return redirect(url_for('error_redirect', product_id=code))

@app.route('/product/<product_id>')
def product_page(product_id):
    url = f'https://www.ceneo.pl/{product_id}'
    name = Data.get(product_id)["name"]
    return render_template('redirect.html', url=url, name = name, product_id = product_id)
    
@app.route('/product/error/<product_id>')
def error_redirect(product_id):
    return render_template('redirect_error.html', product_id = product_id)
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/products')
def products():
    extracts = []
    for id in Data.get_ids():
        x =  Data.get(id)
        x["id"] = id
        extracts.append(x)
    
    products = []
    
    for extract in extracts:
        product = {"id": extract["id"],
                   "name": extract["name"],
                   "opinions_count": extract["opinions amount"]}
        if extract["opinions"]:
            product["extracted_count"] = str(len(extract["opinions"]))
            advantages = 0
            disadvantages = 0
            avg = 0
            amo = 0
            for opinion in extract["opinions"]:
                if opinion["advantages"]:
                    advantages += len(opinion["advantages"])
                if opinion["disadvantages"]:
                    disadvantages += len(opinion["disadvantages"])
                if opinion["score"]:
                    avg += opinion["score"]
                    amo += 1
        
            product["advantage_count"] = advantages
            product["disadvantage_count"] = disadvantages
            avg = avg / amo
            product["average_rating"] = avg
        elif not extract["opinions amount"]:
            product["opinions_count"] = 0
        products.append(product)
        
    return render_template('products.html', products=products)

@app.route('/products/<product_id>')
def product_detail(product_id):
    product = Data.get(product_id)
    product["id"] = product_id
    reviews = []
    opinions = product["opinions"]
    if not opinions:
        opinions = []
    for opinion in opinions:
        review = {"id": opinion["id"],
                  "author": opinion["author"],
                  "score": opinion["score"],
                  "content": opinion["content"],
                  "advantages": [],
                  "disadvantages": [],
                  "likes": opinion["likes"],
                  "dislikes": opinion["dislikes"]}
        if opinion["recommendation"]:
            review["recommendation"] = opinion["recommendation"]
        if opinion["advantages"]:
            x = 1
            for adv in opinion["advantages"]:
                review["advantages"].append(f"{x})⠀{adv}")
                x += 1
        if opinion["disadvantages"]:
            x = 1
            for disadv in opinion["disadvantages"]:
                review["disadvantages"].append(f"{x})⠀{disadv}")
                x += 1
        if opinion["publish time"]:
            review["publish_time"] = opinion["publish time"].split()
        if opinion["purchase time"]:
            review["purchase_time"] = opinion["purchase time"].split()
        
        reviews.append(review)
        
    return render_template('product.html', product = product, reviews = reviews)

@app.route('/download/<product_id>/<format>')
def download_reviews(product_id, format):
    return f'Download {format} reviews for Product {product_id} - Implement download logic.'

@app.route('/products/<product_id>/charts')
def charts(product_id):
    return f'Charts for {product_id}'

# -------

def save_product(id):
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

# -------

if __name__ == '__main__':
    app.run(debug=True)