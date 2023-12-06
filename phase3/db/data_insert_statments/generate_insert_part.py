import re

reg_string = "(?P<vin>\w+)\t(?P<order_num>\d+)\t(?P<vendor_name>[A-z| |\-]+)\t(?P<part_number>[A-z| |\-|0-9]+)\t(?P<description>[A-z| |\\|\/|\-|:|0-9]+)\t(?P<price>\d+\.\d+)\t(?P<status>[A-z| |\-|0-9]+)\t(?P<qty>\d+)"

txt_file = "parts.tsv"
out_file = "insert_parts.txt"
fin = open(txt_file, 'r')
fout = open(out_file, "w")
data = fin.readlines()

for line in data:
    reg_res = re.search(reg_string, line)
    if (reg_res):
        vin = reg_res.group('vin')
        purchase_order_number = reg_res.group('order_num')
        part_number = reg_res.group('part_number')
        description = reg_res.group('description')
        status = reg_res.group('status')
        cost = reg_res.group('price')
        quantity = reg_res.group('qty')
        vendor_name = reg_res.group('vendor_name')

        values = f"VALUES ('{part_number}', '{purchase_order_number}', '{description}', '{status}', '{cost}', '{quantity}')"
        insert_query = "INSERT INTO part (part_number, purchase_order_number, description, status, cost, quantity) " + values + ";\n"
        fout.write(insert_query)

        # values = f"VALUES ('{purchase_order_number}', '{vin}', '{purchase_order_number}', '{vendor_name}', '', '0')"
        # insert_query = "INSERT INTO partorder (purchase_order_number, vin, order_number, part_vendor_name, username, total_cost)"



fin.close()
fout.close()