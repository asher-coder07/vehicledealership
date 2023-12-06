import logging
from flask import g, request

logger = logging.getLogger(__name__)

def get_vehicle():
    conn = g.get('conn')  # retrieves psycopg2 connection object from flask g
    query = f'''
        select distinct
            v.*,
            s.purchase_price * 1.25 + po.total_cost * 1.1 as price
        from vehicle v
        left join vehiclecolor vc on v.vin = vc.vin
        left join sell s on v.vin = s.vin
        left join partorder po on v.vin = po.vin
    '''
    clauses = []
    manufacturer_name = request.args.get('manufacturer-name', None) or request.args.get('manufacturer', None)
    if manufacturer_name:
        clause = f"""v.manufacturer_name = '{manufacturer_name}'"""
        clauses.append(clause)
    vehicle_type = request.args.get('vehicle-type', None) or request.args.get('type', None)
    if vehicle_type:
        clause = f"""v.vehicle_type = '{vehicle_type}'"""
        clauses.append(clause)
    fuel_type = request.args.get('fuel-type', None) or request.args.get('fuel', None)
    if fuel_type:
        clause = f"""v.fuel_type = '{fuel_type}'"""
        clauses.append(clause)
    model_name = request.args.get('model-name', None) or request.args.get('model', None)
    if model_name:
        clause = f"""v.model_name ilike '{model_name}'"""
        clauses.append(clause)
    model_year = request.args.get('model-year', None) or request.args.get('year', None)
    if model_year:
        clause = f"""v.model_year = '{model_year}'"""
        clauses.append(clause)
    kw = request.args.get('kw', None)
    if kw:
        clause = f"""v.description ilike '%{kw}%'"""
        clauses.append(clause)
    mileage = request.args.get('mileage', None)
    if mileage:
        clause = f"""v.mileage <= '{mileage}'"""
        clauses.append(clause)
    # TODO: double check color
    colors = request.args.get('colors', None)
    if colors:
        color_list = colors.split(',')
        color_list_str = str(color_list).lstrip('[').rstrip(']')
        clause = f"""vc.color = all ({color_list_str})"""
        clauses.append(clause)
    price = request.args.get('price', None)    
    if price:
        clause = f"""(s.purchase_price * 1.25 + po.total_cost * 1.1) <= {price}"""
        clauses.append(clause)
    
    # TODO: need to verify user role as well!!!!
    vin = request.args.get('vin', None)
    if vin:
        clause = f"""v.vin ilike '{vin}'"""
        clauses.append(clause)
    # TODO: inventory clerk and sales people might have diff views.

    if len(clauses) > 0:
        query += ' where '
        query += f"""{' and '.join(clauses)}"""
    
    print(query)
    cursor = conn.cursor()
    cursor.execute(query)

    response = {}
    columns = [desc[0] for desc in cursor.description]
    logger.info(columns)
    response['metadata'] = columns

    data = cursor.fetchall()
    logger.info(data[:2])
    response['data'] = data

    return response


# def get_vehicle(vin, user_info):
#     conn = g.get('conn') 
#     #user_access = "owner"   # salespeople, clerk, manager, owner
#     user_access = user_info["user_role"]

#     if user_access:
#         if user_access == "salespeople":
#             select = "v.vin, v.vehicle_type, v.manufacturer_name, v.model_name, v.model_year, v.fuel_type, vc.color, v.mileage, v.description"
#             tables = """ LEFT JOIN VehicleColor vc ON v.vin = vc.vin"""
#         elif user_access in ["clerk", "manager", "owner"]:
#             select = "v.vin, v.vehicle_type, v.manufacturer_name, v.model_name, v.model_year, v.fuel_type, vc.color, v.mileage, v.description, c.phone_number, s.purchase_price, s.purchase_date"
#             tables = """ LEFT JOIN VehicleColor vc ON v.vin = vc.vin
#                         LEFT JOIN Sell s ON v.vin = s.vin 
#                         LEFT JOIN Customer c ON s.customer_id = c.customer_id """

#     base_query = '''SELECT '''+ select +  ''' FROM Vehicle v ''' +  tables + ''' WHERE v.vin = %s;'''

#     cursor = conn.cursor()
#     cursor.execute(base_query, (vin,))

#     data_veh = cursor.fetchone()
#     metadata = [desc[0] for desc in cursor.description]

#     vehicles_details = data_veh

#     if user_access in ("clerk", "manager", "owner"):
#         vehicles_details["parts_order"] = []  
#         query = '''SELECT p.purchase_order_number, p.part_vendor_name, p.total_cost 
#                 FROM PartOrder p 
#                 WHERE p.vin = %s 
#                 ORDER BY p.purchase_order_number; '''
#         cursor = conn.cursor()
#         cursor.execute(query, (vin,))
#         all_orders = cursor.fetchall()
#         metadata.append('parts_order')
#         for order in all_orders:
#             vehicles_details["parts_order"].append(order)
    
#     if user_access in ("manager", "owner"):
#         vehicles_details["buyer_info"] = {} 
#         query = '''SELECT CONCAT_WS(' ',ci.first_name, ci.last_name) AS contact_info, c.street, c.city, c.state, c.postal_code, c.phone_number, b.username 
#                     FROM Vehicle v 
#                     LEFT JOIN Buy b ON v.vin = b.vin 
#                     LEFT JOIN Customer c ON b.customer_id = c.customer_id 
#                     LEFT JOIN CustomerIndividual ci ON ci.customer_id = c.customer_id 
#                     WHERE v.vin = %s 
#                     UNION 
#                     SELECT CONCAT_WS(' ',cb.contact_name, cb.title) AS contact_info, c.street, c.city, c.state, c.postal_code, c.phone_number, b.username 
#                     FROM Vehicle v 
#                     LEFT JOIN Buy b ON v.vin = b.vin 
#                     LEFT JOIN Customer c ON b.customer_id = c.customer_id 
#                     LEFT JOIN CustomerBusiness cb ON cb.customer_id = c.customer_id 
#                     WHERE v.vin = %s ;  '''
#         cursor = conn.cursor()
#         cursor.execute(query, (vin,vin))

#         data_veh_buyer = cursor.fetchone()
#         metadata.append('buyer_info')
#         vehicles_buyer_info = data_veh_buyer

#         vehicles_details["buyer_info"] = vehicles_buyer_info

#     return {'data': vehicles_details, 'metadata': metadata}
