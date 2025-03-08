from flask import Flask, render_template, request
import WebScrape
import Data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/extract', methods=['GET'])
def extract():
    return render_template('extraction.html')

@app.route('/extract', methods=['POST'])
def start_extraction():
    code = request.form['product_id']
    # Here you would add your logic to extract data based on the product ID
    # Placeholder redirect to a hypothetical product page
    url = f"https://www.ceneo.pl/{code}"
    # return render_template('redirect.html', url=url)
    return render_template('redirect_error.html')

@app.route('/product/<product_id>')
def product_page(product_id):
    # This function should handle displaying the product and its reviews
    # For now, just return a placeholder response
    return f"Product Page for Product ID: {product_id}"

if __name__ == "__main__":
    app.run(debug=True)