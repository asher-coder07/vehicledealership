import logging
from flask import g

logger = logging.getLogger(__name__)

def get_seller_history(*args, **kwargs):
    query = f"""
        select *
        from public.seller_history;
    """
    conn = g.pop('conn', None)
    cursor = conn.cursor()
    cursor.execute(query)
    
    response = {}
    columns = [desc[0] for desc in cursor.description]
    response['metadata'] = columns

    data = cursor.fetchall()
    response['data'] = data
    
    return response


def get_average_time_in_inventory(*args, **kwargs):
    query = f"""
        select *
        from public.average_time_in_inventory;
    """
    conn = g.pop('conn', None)
    cursor = conn.cursor()
    cursor.execute(query)
    
    response = {}
    columns = [desc[0] for desc in cursor.description]
    response['metadata'] = columns
    
    data = cursor.fetchall()
    response['data'] = data
    return response


def get_price_per_condition(*args, **kwargs):
    query = f"""
        select *
        from public.price_per_condition;
    """
    conn = g.pop('conn', None)
    cursor = conn.cursor()
    cursor.execute(query)
    
    response = {}
    columns = [desc[0] for desc in cursor.description]
    response['metadata'] = columns
    
    data = cursor.fetchall()
    response['data'] = data
    return response


def get_parts_statistics(*args, **kwargs):
    query = f"""
        select *
        from public.parts_statistics;
    """
    conn = g.pop('conn', None)
    cursor = conn.cursor()
    cursor.execute(query)
    
    response = {}
    columns = [desc[0] for desc in cursor.description]
    response['metadata'] = columns
    
    data = cursor.fetchall()
    response['data'] = data
    return response


def get_monthly_sales_summary(*args, **kwargs):
    query = f"""
        select *
        from public.monthly_sales_summary;
    """
    conn = g.pop('conn', None)
    cursor = conn.cursor()
    cursor.execute(query)
    
    response = {}
    columns = [desc[0] for desc in cursor.description]
    response['metadata'] = columns
    
    data = cursor.fetchall()
    response['data'] = data
    return response


def get_monthly_sales_drilldown(*args, **kwargs):
    year = kwargs.pop('year', None)
    month = kwargs.pop('month', None)
    query = f"""
        select *
        from public.monthly_sales_drilldown
    """
    if year and month:
        query = query + f"""
            where date_part('year', b.sale_date::date)::varchar = '{year}'
            and date_part('month', b.sale_date::date)::varchar = '{month}';
        """

    conn = g.pop('conn', None)
    cursor = conn.cursor()
    cursor.execute(query)
    
    response = {}
    columns = [desc[0] for desc in cursor.description]
    response['metadata'] = columns
    
    data = cursor.fetchall()
    response['data'] = data
    return response
