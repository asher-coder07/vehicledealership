from flask import g

def get_individual_customer(drivers_license_number):
    conn = g.pop('conn')
    base_query = f'''
        select *
        from customerindividual
        where drivers_license_number = '{drivers_license_number}'
    '''
    cursor = conn.cursor()
    cursor.execute(base_query)

    customers = []
    for customer in cursor:
        customers.append(customer)
    return customers


def add_individual_customer(customer_json):
    conn = g.pop('conn')  # retrieves psycopg2 connection object from flask g
    street = valOrEmptyString(customer_json, 'street')
    city = valOrEmptyString(customer_json, 'city')
    state = valOrEmptyString(customer_json, 'state')
    postal_code = valOrEmptyString(customer_json, 'postal_code')
    phone_number = valOrEmptyString(customer_json, 'phone_number')
    drivers_license_number = valOrEmptyString(customer_json, 'drivers_license_number')
    first_name = valOrEmptyString(customer_json, 'first_name')
    last_name = valOrEmptyString(customer_json, 'last_name')

    base_query = f'''
        INSERT INTO customer (street, city, state, postal_code, phone_number)
        VALUES ('{street}', '{city}', '{state}', '{postal_code}', '{phone_number}')
    '''

    secondary_query = f'''
        INSERT INTO customerindividual (tax_id_number, first_name, last_name)
        VALUES ('{drivers_license_number}', '{first_name}', '{last_name}')
    '''

    cursor = conn.cursor()
    cursor.execute(base_query)
    cursor.execute(secondary_query)
    conn.commit()
    return True


def valOrEmptyString(obj, key):
    return obj.pop(key) if key in obj.keys() else ""
