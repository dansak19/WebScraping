from flask import Flask, render_template, request, redirect, url_for, send_file, Response
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import time
import WebScrape
import Data

app = Flask(__name__)

matplotlib.use('Agg') 

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
            product["average_rating"] = round(avg, 2)
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
    if format == "csv":
        path = Data.save_csv(product_id)
    elif format == "xlsx":
        path = Data.save_xlsx(product_id)
    elif format == "json":
        path = Data.save_json(product_id)
    print(path)
    return send_file(path, as_attachment=True)

@app.route('/products/<product_id>/charts')
def charts(product_id):
    name = Data.get(product_id)["name"]
    return render_template('charts.html', name = name, product_id = product_id)
@app.route('/products/<product_id>/delete')
def delete(product_id):
    name = Data.get(product_id)["name"]
    Data.delete(product_id)
    return render_template('delete.html', name = name, product_id = product_id)

@app.route('/products/<product_id>/pie')
def pie_cart(product_id):
    opinions = Data.get(product_id)["opinions"]
    recomendations = {'Polecam': 0, 
                      'Nie polecam': 0, 
                      'Niema rekomendacji': 0}
    
    for opinion in opinions:
        if opinion["recommendation"]:
            if opinion["recommendation"] == "Polecam":
                recomendations["Polecam"] += 1
            elif opinion["recommendation"] == "Nie polecam":
                recomendations["Nie polecam"] += 1
        else:
            recomendations["Niema rekomendacji"] += 1
            
    to_del = []
    for key, value in recomendations.items():
        if not value:
            to_del.append(key)
    for key in to_del:
        del recomendations[key]
        
    explode = [0.1]
    for i in range(len(recomendations.keys()) - 1):
        explode.append(0)
    print(explode)
    
    colors = ["#4A6572", "#C68F6C", "#7D7461"]

    fig, ax = plt.subplots()
    ax.pie(
        recomendations.values(),
        explode = explode,
        labels=recomendations.keys(),
        autopct='%1.1f%%', 
        colors=colors,
        startangle=90,
    )
    ax.axis('equal')  
    
    img = BytesIO()
    plt.savefig(img, format='png', dpi=300)
    img.seek(0)  
    plt.close()  

    time.sleep(0.05)

    return Response(img.getvalue(), mimetype='image/png')

@app.route('/products/<product_id>/bar')
def bar_chart(product_id):
    opinions = Data.get(product_id)["opinions"]
    ratings = {}
    scores = []
    for opinion in opinions:
        scores.append(opinion["score"])
    for score in set(scores):
        ratings[str(score)] = 0
    for opinion in opinions:
        ratings[str(opinion["score"])] += 1

    fig, ax = plt.subplots(figsize=(8, 6))
    
    colors = ["#4A6572", "#C68F6C", "#7D7461"]

    ax.bar(ratings.keys(), ratings.values(), color=colors)

    ax.set_title('Liczba opinii według oceny gwiazdkowej', fontsize=16)
    ax.set_xlabel('Ocena gwiazdkowa', fontsize=12)
    ax.set_ylabel('Liczba opinii', fontsize=12)

    img = BytesIO()
    plt.savefig(img, format='png', dpi=300)
    img.seek(0)
    plt.close()
    
    time.sleep(0.05)

    return Response(img.getvalue(), mimetype='image/png')

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