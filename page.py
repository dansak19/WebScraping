from flask import Flask, render_template, request, redirect, url_for, send_file, Response
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
from WebScrape import Page
from Data import Database, Download 
from datetime import datetime
from threading import Lock

app = Flask(__name__)

matplotlib.use('Agg') 

chart_lock = Lock()

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
    product = Page(code)
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
    product = Database(product_id)
    name = product.get()["name"]
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
    for id in Database().get_ids():
        p = Database(id)
        x =  p.get()
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
    product = Database(product_id)
    product = product.get()
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
    file = Download(product_id)
    if format == "csv":
        path = file.csv()
    elif format == "xlsx":
        path = file.xlsx()
    elif format == "json":
        path = file.json()
    print(path)
    return send_file(path, as_attachment=True)

@app.route('/products/<product_id>/charts')
def charts(product_id):
    product = Database(product_id)
    name = product.get()["name"]
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
    return render_template('charts.html', name = name, product_id = product_id, timestamp=timestamp)

@app.route('/products/<product_id>/delete')
def delete(product_id):
    product = Database(product_id)
    name = product.get()["name"]
    product.delete()
    return render_template('delete.html', name = name, product_id = product_id)

@app.route('/products/<product_id>/pie')
def pie_cart(product_id):
    with chart_lock:
        product = Database(product_id)
        opinions = product.get()["opinions"]
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
            explode.append(float(f"0.0{i + 1}"))
    
        colors = ["#4A6572", "#C68F6C", "#7D7461"]

        fig, ax = plt.subplots()
        ax.pie(
            recomendations.values(),
            explode = sorted(explode),
            labels=recomendations.keys(),
            autopct='%1.1f%%', 
            colors=colors,
            startangle=90,
        )
        ax.axis('equal')  

        img = BytesIO()
        plt.savefig(img, format='png', dpi=300)
        img.seek(0)  
        plt.close(fig)  

        response = Response(img.getvalue(), mimetype='image/png')
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        return response

@app.route('/products/<product_id>/bar')
def bar_chart(product_id):
    with chart_lock:
        product = Database(product_id)
        opinions = product.get()["opinions"]
        ratings = {}
        scores = []
        for opinion in opinions:
            scores.append(opinion["score"])
        for score in sorted(list(set(scores))):
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
        plt.close(fig)
    
        response = Response(img.getvalue(), mimetype='image/png')
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        return response

# -------

def save_product(id):
    product = Page(id)
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
                
            product = Database(id)
            product.save(name, amount, comments)

# -------

if __name__ == '__main__':
    app.run(debug=True)