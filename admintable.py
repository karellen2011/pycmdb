from sqlalchemy import create_engine, text
import pandas as pd

from cmdbhtml import html_header, html_footer
from cmdbdb import cmdb_connect, cmdb_disconnect

def adminlisttables(create_table_name, display_value, drop_table_name, update_table_name, display_order):
    create_query = ''
    if create_table_name != '' and drop_table_name == '' and display_value != '' and display_order != '':
        create_query = create_table(create_table_name, display_value, display_order)
    delete_query = ''
    if create_table_name == '' and drop_table_name != '':
        delete_query = drop_table(drop_table_name)
    update_query = ''
    if update_table_name != '' and display_value != '' and display_order != '':
        update_query = update_table(update_table_name, display_value, display_order)
    query = """
SELECT
  _sys_display_value.uuid AS uuid,
  pg_catalog.pg_tables.tablename AS tablename,
  _sys_display_value.display_value AS display_value,
  _sys_display_value.sys_order AS display_order
FROM pg_catalog.pg_tables
JOIN _sys_display_value ON pg_catalog.pg_tables.tablename = _sys_display_value.sys_table
WHERE tableowner = 'cmdb'
  AND tablename NOT LIKE '_sys_%'
  AND sys_table = tablename
  AND sys_table_column = ''
ORDER BY display_order, display_value
;
    """
    conn = cmdb_connect()
    df = pd.read_sql(text(query), conn)
    cmdb_disconnect(conn)

    # OUTPUT ALL TABLES
    output = html_header()
    #output += create_table_name + '<br>\n'
    #output += display_value + '<br>\n'
    #output += drop_table_name + '<br>\n'
    #output += update_table_name + '<br>\n' # ???
    #output += str(create_sql) + '<br>\n'
    #output += str(update_query) + '<br>\n'
    output += '<form action="/admin/table/" method="POST">\n'
    output += '<table id="default">\n'
    output += '<tr><th>Table</th><th>Display Value</th><th>Order</th><th></th>\n<tr>\n'
    output += '<td><input type="text" name="create_table"></td>\n'
    output += '<td><input type="text" name="display_value"></td>\n'
    output += '<td><input type="text" name="display_order"></td>\n'
    output += '<td><button type="submit"><img src="/static/create.png" alt="Create" width="20"></button></td>\n'
    output += '</tr>\n'
    #for c, table in enumerate(tables):
    for i in df.iterrows():
        output += '<tr>\n'
        output += '<td><a href="/table/list/' + str(i[1]['tablename']) + '/">' + str(i[1]['tablename']) + '</a></td>\n'
        #output += '<td><input type="text" name="update_table_dv|' + str(i[1]['tablename']) + '" value="' + str(i[1]['display_value']) + '"></td>\n'
        output += '<td><input type="text" name="' + str(i[1]['uuid']) + '::update_display_value" value="' + str(i[1]['display_value']) + '"></td>\n'
        output += '<td><input type="text" name="' + str(i[1]['uuid']) + '::update_display_order" value="' + str(i[1]['display_order']) + '"></td>\n'
        output += '<td>'
        output += '<button type="submit" name="update_table" value="' + str(i[1]['uuid']) + '"><img src="/static/update.png" alt="Update" width="20"></button>'
        output += '<button type="submit" name="drop_table" value="' + str(i[1]['tablename']) + '"><img src="/static/drop.png" alt="Drop" width="20"></button>'
        output += '</td>\n'
        output += '</tr>\n'
    output += '</table>\n'
    output += '</form>\n'

    # SQL DEBUG
    output += '<div class="tab">\n'
    output += '<button class="tablinks" onclick="openTab(event, \'Select\')">Select</button>\n'
    output += '<button class="tablinks" onclick="openTab(event, \'Create\')">Create</button>\n'
    output += '<button class="tablinks" onclick="openTab(event, \'Update\')">Update</button>\n'
    output += '<button class="tablinks" onclick="openTab(event, \'Delete\')">Delete</button>\n'
    output += '</div>\n'
    output += '<div id="Select" class="tabcontent">\n'
    output += '<p id="debug">' + str(query).replace('\n', '<br>\n') + '</p>\n'
    output += '</div>\n'
    output += '<div id="Create" class="tabcontent">\n'
    output += '<p id="debug">' + str(create_query).replace('\n', '<br>\n') + '</p>\n'
    output += '</div>\n'
    output += '<div id="Update" class="tabcontent">\n'
    output += '<p id="debug">' + str(update_query).replace('\n', '<br>\n') + '</p>\n'
    output += '</div>\n'
    output += '<div id="Delete" class="tabcontent">\n'
    output += '<p id="debug">' + str(delete_query).replace('\n', '<br>\n') + '</p>\n'
    output += '</div>\n'

    output += html_footer()
    return output

def create_table(tablename, display_value, display_order):
    query = ''
    html_query = ''
    conn = cmdb_connect()
    # FIRST CHECK IF TABLE DOES EXIST ALREADY
    query = "SELECT COUNT(1) FROM pg_catalog.pg_tables WHERE tableowner = 'cmdb' AND tablename = '" + tablename + "';"
    rows = conn.execute(text(query))
    table_exist = 0
    for row in rows:
        table_exist = int(row[0])
    if table_exist == 0:
        query = 'CREATE TABLE ' + tablename + ' (uuid VARCHAR(32) NOT NULL DEFAULT get_uuid(), name VARCHAR(256), active boolean NOT NULL DEFAULT true);'
        html_query += '<br>\n' + query
        conn.execute(text(query))
        #conn.commit()
        query = "INSERT INTO " + tablename + " (name) values ('-- None --');"
        html_query += '<br>\n' + query
        conn.execute(text(query))
        #conn.commit()
        query = "INSERT INTO _sys_display_value (sys_table, sys_table_column, display_value, sys_order, include) VALUES ('" + str(tablename) + "', '', '" + str(display_value) + "', " + str(display_order) + ", false);"
        html_query += '<br>\n' + query
        conn.execute(text(query))
        query = "INSERT INTO _sys_display_value (sys_table, sys_table_column, display_value, sys_order, include) VALUES ('" + str(tablename) + "', 'uuid', '" + str('UUID') + "', 10, false);"
        html_query += '<br>\n' + query
        conn.execute(text(query))
        query = "INSERT INTO _sys_display_value (sys_table, sys_table_column, display_value, sys_order, include) VALUES ('" + str(tablename) + "', 'name', '" + str('Name') + "', 20, false);"
        html_query += '<br>\n' + query
        conn.execute(text(query))
        query = "INSERT INTO _sys_display_value (sys_table, sys_table_column, display_value, sys_order, include) VALUES ('" + str(tablename) + "', 'active', '" + str('Active') + "', 30, false);"
        html_query += '<br>\n' + query
        conn.execute(text(query))
        conn.commit()
    cmdb_disconnect(conn)
    return html_query

def drop_table(tablename):
    html_query = ''
    conn = cmdb_connect()

    # DELETE ALL POSSIBLE DICTIONARIES
    query = """
DELETE FROM _sys_dictionary WHERE sys_table = '""" + str(tablename) + """';
    """
    html_query += '\n' + query
    conn.execute(text(query))
    conn.commit()

    # DELETE ALL POSSIBLE DISPLAY VALUES
    query = """
DELETE FROM _sys_display_value WHERE sys_table = '""" + str(tablename) + """';
    """
    html_query += '\n' + query
    conn.execute(text(query))
    conn.commit()

    # FINALLY DELETE THE TABLE
    query = """
DROP TABLE """ + tablename + """;
    """
    html_query += '\n' + query
    conn.execute(text(query))
    conn.commit()

    cmdb_disconnect(conn)
    return html_query

def update_table(table, display_value, display_order):
    query = """
UPDATE _sys_display_value 
SET display_value = '""" + str(display_value) + """', sys_order = '""" + str(display_order) + """'
WHERE uuid = '""" + str(table) + """'
AND sys_table_column = '';
    """
    conn = cmdb_connect()
    conn.execute(text(query))
    conn.commit()
    cmdb_disconnect(conn)
    return query

