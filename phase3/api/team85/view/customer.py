from flask import jsonify, Blueprint, request
import team85.controller.customer as c

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/search', methods=['GET'])
def search_customer():
    params = request.args
    customers = c.search_customer(**params)
    
    return jsonify(customers)


