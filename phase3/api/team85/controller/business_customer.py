from flask import g

def get_business_customer(tax_id_number):
    conn = g.pop('conn')
    base_query = f'''
        select *
        from customerbusiness
        where tax_id_number = '{tax_id_number}'
    '''
    cursor = conn.cursor()
    cursor.execute(base_query)

    customers = []
    for customer in cursor:
        customers.append(customer)

    return customers


def add_business_customer(customer_json):
    conn = g.pop('conn')  # retrieves psycopg2 connection object from flask g
    street = valOrEmptyString(customer_json, 'street')
    city = valOrEmptyString(customer_json, 'city')
    state = valOrEmptyString(customer_json, 'state')
    postal_code = valOrEmptyString(customer_json, 'postal_code')
    phone_number = valOrEmptyString(customer_json, 'phone_number')
    tax_id_number = valOrEmptyString(customer_json, 'tax_id_number')
    contact_name = valOrEmptyString(customer_json, 'contact_name')
    title = valOrEmptyString(customer_json, 'title')

    base_query = f'''
        INSERT INTO customer (street, city, state, postal_code, phone_number)
        VALUES ('{street}', '{city}', '{state}', '{postal_code}', '{phone_number}')
    '''

    secondary_query = f'''
        INSERT INTO businesscustomer (tax_id_number, contact_name, title)
        VALUES ('{tax_id_number}', '{contact_name}', '{title}')
    '''

    cursor = conn.cursor()
    cursor.execute(base_query)
    cursor.execute(secondary_query)
    conn.commit()
    return True


def valOrEmptyString(obj, key):
    return obj.pop(key) if key in obj.keys() else ""
