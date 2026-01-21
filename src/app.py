from flask import Flask, jsonify, render_template_string, request, url_for
from products import products
from markupsafe import escape
from flask_cors import CORS
import os
from flask import send_from_directory

app = Flask(__name__)
app.app_context().push()

# CORS(app)
CORS(app, resources={r"/*":{"origins":['http://localhost:40000', 'http://localhost:60000']}})

@app.route('/')
def index():
    return "API"

@app.route('/ping', methods=['GET'])
def ping():

    return jsonify({"message":"PONG!"})

# READ ALL PRODUCTS
@app.route('/products', methods=['GET'])
def get_products():

    return jsonify({"products": products,
                    "message": "Products List"})

# READ SINGLE PRODUCT
@app.route('/products/<string:product_name>', methods=['GET'])
def get_product(product_name):

    product_found = [product for product in products if product['name'] == product_name.lower()]
    print(product_found)

    if product_found:
        return jsonify({"product": product_found[0],
                   "message": "One Product"})
    else:
        return jsonify({"message": "Product Not Found: " + product_name })

# CREATE PRODUCT
@app.route('/products', methods=['POST'])
def add_product():
    # print(request.json)

    new_product = {
        "name": request.json['name'],
        "price": request.json['price'],
        "quantity": request.json['quantity']
    }
    print(new_product)
    products.append(new_product)

    return jsonify({"message": "Product Add Successfully",
                    "products": products}),201

# UPDATE PRODUCT
@app.route('/products/<string:product_name>', methods=['PUT'])
def edit_product(product_name):

    product_found = [product for product in products if product['name'] == product_name.lower()]
    # print(product_found)

    if product_found:

        product_found[0]['name'] = request.json['name']
        product_found[0]['price'] = request.json['price']
        product_found[0]['quantity'] = request.json['quantity']

        return jsonify({"product": product_found[0],
                   "message": "Product Updated"})
    else:
        return jsonify({"message": "Product Not Found: " + product_name })
    
# DELETE PRODUCT
@app.route('/products/<string:product_name>', methods=['DELETE'])
def delete_product(product_name):

    product_found = [product for product in products if product['name'] == product_name.lower()]
    # print(product_found)

    if product_found:

        products.remove(product_found[0])

        return jsonify({"products": products,
                   "message": "Product Deleted"})
    else:
        return jsonify({"message": "Product Not Found: " + product_name })

# @app.route('/<name>')
# def hello(name):
#     return "Hello " + escape(name)

@app.route('/projects/')
def projects():
    return 'The Projects Page!'

@app.route('/about')
def about():
    return 'About us!'

@app.errorhandler(404)
def not_found(error):

    return jsonify({"message": "Not Found"}), 404

@app.route('/search')
def search():
    query = request.args.get('q', '')

    template = '''
    <h1>Resultados para: %s </h1>
''' % escape(query)
    
    return render_template_string(template)

def query_string():
    print(request)
    print(request.query_string)
    print(request.args)
    print(request.args.get('page'))
    print(request.args.get('nombre'))
    return "OK"


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':

    app.add_url_rule('/query_string', view_func=query_string)
    # app.add_url_rule('/favicon', redirect_to=url_for('static', filename='favicon.ico'))
    app.run(debug=True, host="0.0.0.0")