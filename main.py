from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

def connect_db():
    connectDB = psycopg2.connect(
        host="localhost",
        database="product_db",
        user="saintvandora",
        password="1234567890"
    )
    return connectDB

@app.route('/product', methods=['POST'])
def create_product():
    data = request.json
    name = data['name']
    attributes = data['attributes']

    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (name, attributes) VALUES (%s, %s) RETURNING id",
        (name, psycopg2.extras.Json(attributes))
    )
    product_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": product_id, "message": "Product created successfully!"}), 201

@app.route('/products', methods=['GET'])
def get_products():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name, attributes FROM products")
    products = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{"id": p[0], "name": p[1], "attributes": p[2]} for p in products]), 200

@app.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    name = data.get('name')  # Get the name from the request
    attributes = data.get('attributes')  # Get the attributes from the request

    conn = connect_db()
    cur = conn.cursor()

    # Update both name and attributes
    cur.execute(
        "UPDATE products SET name = %s, attributes = %s WHERE id = %s",
        (name, psycopg2.extras.Json(attributes), product_id)
    )
    
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Product updated successfully!"}), 200

@app.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Product deleted successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)