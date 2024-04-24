import connexion

from flask import jsonify, request

from config import CONFIG
from stock import read_all, add, read_one, update, delete

app = connexion.FlaskApp(__name__)
# Route to read all stock
@app.route('/stock', methods=['GET'])
def get_stock():
    return read_all()

# Route to add stock
@app.route('/stock', methods=['POST'])
def add_stock():
    med = request.json
    return add(med)

# Route to read one stock item
@app.route('/stock/<int:med_id>', methods=['GET'])
def get_one_stock(med_id):
    return read_one(med_id)

# Route to update stock
@app.route('/stock/<int:med_id>', methods=['PUT'])
def update_stock(med_id):
    med = request.json
    return update(med_id, med)

# Route to delete stock
@app.route('/stock/<int:med_id>', methods=['DELETE'])
def delete_stock(med_id):
    return delete(med_id)

app.add_api("pharm-api.yml")
app.run(host=CONFIG["server"]["listen_ip"], port=CONFIG["server"]["port"], debug=CONFIG["server"]["debug"])