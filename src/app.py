from flask import Flask, jsonify, request
from products import products

app = Flask(__name__)

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




if __name__ == '__main__':

    app.run(debug=True)