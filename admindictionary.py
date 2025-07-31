from sqlalchemy import create_engine, text
import pandas as pd

from cmdbhtml import html_header, html_footer
from cmdbdb import cmdb_connect, cmdb_disconnect

def adminlistdict(table, column, dict_value, dict_color, display_order, action, uuid):
    query = ''
    if table != '' and column != '' and dict_value != '' and display_order != '' and action == 'create':
        query = add_dict_entry(table, column, dict_value, dict_color, display_order)
    if table != '' and column != '' and dict_value != '' and display_order != '' and action == 'update' and uuid != '':
        query = up_dict_entry(table, column, dict_value, dict_color, display_order, uuid)

    df = get_dictionaries()
    if table != '':
        df = df[df['sys_table'] == table].copy()
    if column != '':
        df = df[df['sys_table_column'] == column].copy()
    tl = list(df['sys_table'].unique())
    tl.insert(0, '')
    cl = list(df['sys_table_column'].unique())
    cl.insert(0, '')

    output = html_header()
    #output += str(query) + '<br>\n'
    #output += str(table) + '<br>\n'
    #output += str(column) + '<br>\n'
    #output += str(dict_value) + '<br>\n'
    #output += str(display_order) + '<br>\n'
    output += '<form action="/admin/dict/" method="POST">\n'
    output += '<table id="default">\n'
    output += '<tr><th>Table</th><th>Column</th><th>Dict Value</th><th>Color</th><th>Order</th><th></th></tr>\n'

    # CREATE A NEW DICTIONARY
    output += '<tr>\n'
    output += '<td><select name="table" onchange="this.form.submit()">\n'
    for t in tl:
        if t == table:
            output +=  '<option value="' + str(t) + '" selected>' + str(t) + '</option>\n'
        else:
            output +=  '<option value="' + str(t) + '">' + str(t) + '</option>\n'
    output += '</select></td>\n'
    output += '<td><select name="column" onchange="this.form.submit()">\n'
    for c in cl:
        if c == column:
            output +=  '<option value="' + str(c) + '" selected>' + str(c) + '</option>\n'
        else:
            output +=  '<option value="' + str(c) + '">' + str(c) + '</option>\n'
    output += '</select></td>\n'
    if table != '' and column != '':
        output += '<td><input type="text" name="dict_value"></td>\n'
        output += '<td><input type="text" name="dict_color"></td>\n'
        output += '<td><input type="text" name="display_order"i value="10"></td>\n'
        output += '<td><button type="submit" name="create_dict" value=""><img src="/static/create.png" alt="Create" width="20"></button></td>'
    else:
        output += '<td></td>\n<td></td>\n<td></td>\n<td></td>\n'
    output += '</tr>\n'

    # LIST ALL TABLES AND COLUMNS AND DICTIONARIES
    for i in df.iterrows():
        output += '<tr>'
        output += '<td>' + str(i[1]['sys_table']) + '</td>'
        output += '<td>' + str(i[1]['sys_table_column']) + '</td>'
        if str(i[1]['dict_value']) == '-- None --':
            output += '<td style="background:#' + str(i[1]['color']) + ';">' + str(i[1]['dict_value']) + '</td>'
        else:
            output += '<td style="background:#' + str(i[1]['color']) + ';"><input type="text" name="' + str(i[1]['uuid']) + '::dict_value" value="' + str(i[1]['dict_value']) + '"></td>'
        output += '<td style="background:#' + str(i[1]['color']) + ';"><input type="text" name="' + str(i[1]['uuid']) + '::dict_color" value="' + str(i[1]['color']) + '"></td>'
        output += '<td><input type="text" name="' + str(i[1]['uuid']) + '::display_order" value="' + str(i[1]['sys_order']) + '"></td>'
        output += '<td><button type="submit" name="update_dict" value="' + str(i[1]['uuid']) + '"><img src="/static/update.png" alt="Update" width="20"></button></td>'
        output += '</tr>\n'


    output += '</table>\n'
    output += '</form>\n'
    output += html_footer()
    return output

def get_dictionaries():
    query = """
SELECT uuid, sys_table, sys_table_column, dict_value, sys_order, color
FROM _sys_dictionary
-- WHERE sys_table = 'product'
--   AND sys_table_column = 'condition'
ORDER BY sys_table, sys_table_column, sys_order, dict_value
;
    """
    conn = cmdb_connect()
    df = pd.read_sql(text(query), conn)
    cmdb_disconnect(conn)
    return df

def add_dict_entry(table, column, dict_value, dict_color, display_order):
    query = """
INSERT INTO _sys_dictionary (sys_table, sys_table_column, dict_value, color, sys_order)
VALUES ('""" + str(table) + """', '""" + str(column) + """', '""" + str(dict_value) + """', '""" + str(dict_color) + """', """ + str(display_order) + """);
    """
    conn = cmdb_connect()
    conn.execute(text(query))
    conn.commit()
    cmdb_disconnect(conn)
    return query

def up_dict_entry(table, column, dict_value, dict_color, display_order, uuid):
    query = """
UPDATE _sys_dictionary 
SET dict_value = '""" + str(dict_value) + """', sys_order = """ + str(display_order) + """, color = '""" + str(dict_color) + """' 
WHERE uuid = '""" + str(uuid) + """';
    """
    conn = cmdb_connect()
    conn.execute(text(query))
    conn.commit()
    cmdb_disconnect(conn)
    return query

