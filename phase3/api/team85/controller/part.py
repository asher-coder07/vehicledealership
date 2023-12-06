from flask import g
import psycopg2 as pg


def add_part(conn, part_json, purchase_order_number):
    part_number = part_json.pop('part_number')
    description = part_json.pop('description')
    # purchase_order_number = part_json.pop('purchase_order_number')
    cost = part_json.pop('cost')
    quantity = part_json.pop('quantity')
    status = part_json.pop('status')
    base_query = f'''
        INSERT INTO part (part_number, purchase_order_number, description, status, cost,
        quantity) VALUES ('{part_number}', '{purchase_order_number}', '{description}', '{status}',
        {cost}, {quantity});
    '''
    print(base_query)
    cursor = conn.cursor()
    cursor.execute(base_query)


def add_part_order(part_order_json):
    conn = g.pop('conn')  # retrieves psycopg2 connection object from flask g
    vin = part_order_json.pop('vin')
    part_vendor_name = part_order_json.pop('part_vendor_name')
    username = part_order_json.pop('username')
    total_cost = part_order_json.pop('total_cost')
    parts = part_order_json.pop('parts')
    print(parts[0])
    base_query = f'''
        WITH max_count AS (
        select TO_CHAR(count(*)+1, 'fm00') count from PartOrder where vin = '{vin}'
        ) INSERT INTO PartOrder (
        purchase_order_number, vin, part_vendor_name, username, total_cost
        ) VALUES (
        CONCAT({vin}, '-', (select count from max_count)), '{vin}', '{part_vendor_name}', '{username}', {total_cost})
        RETURNING purchase_order_number;
    '''
    
    print(base_query)
    cursor = conn.cursor()
    cursor.execute(base_query)
    
    res = cursor.fetchone()

    # For each part in insert into db
    pon = dict(res)['purchase_order_number']
    for part in parts:
        add_part(conn, part, pon)

    conn.commit()
    return True


def update_part_status(part_id, new_status):
    if not part_id or not new_status:
        return {"error":"The operation cannot be completed as the part_id or new_status is missing."}, 400

    conn = g.pop('conn')  
    cursor = conn.cursor()

    select_query = f'''
        SELECT status
        FROM part 
        WHERE part_number = %s; 
    '''
    cursor.execute(select_query,(part_id,))
    curr_status = cursor.fetchone()
    
    if (curr_status is None):
        return {"error":"No matches found with the provided part_id."}, 400
    
    curr_status = curr_status.get("status")

    if (curr_status == "Installed" and new_status in ["Ordered","Received"]) or (curr_status == "Received" and new_status == "Ordered"):
        return {"error":"Invalid Status Change."}, 422

    base_query = f'''
        UPDATE part 
        SET status = %s 
        WHERE part_number = %s; 
    '''
    try:
        cursor.execute(base_query,(new_status,part_id))
        conn.commit()
    except pg.errors.CheckViolation as error_constraint:
        return {"error":str(error_constraint)}, 422

    return cursor.rowcount, 200