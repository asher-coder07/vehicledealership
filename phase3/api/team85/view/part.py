from flask import jsonify, Blueprint, request, Response
import team85.controller.part as poc

part_bp = Blueprint('parts', __name__)

# CRUD operations - create, read, update, delete

@part_bp.route('/order', methods=['POST'])
def add_part_order():
    body = request.json
    added = poc.add_part_order(body)
    
    return jsonify(added)


# @vehicle_bp.route('/', methods=['POST'])
# def add_vehicle():
#     body = request.body
#     added = vc.add_vehicle(body)

#     return jsonify(added)


# @vehicle_bp.route('/', methods=['PUT'])
# def update_vehicle():
#     pass
