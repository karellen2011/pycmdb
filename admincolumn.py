from sqlalchemy import create_engine, text
import pandas as pd

from cmdbhtml import html_header, html_footer
from cmdbdb import cmdb_connect, cmdb_disconnect

def adminlistcolumns(table, column, display_value, display_order, data_type, length, column_default, update_data):

    # CREATE A NEW COLUMN (ACTUALLY DO IT)
    query = ''
    if table != '-- None --' and column != '' and data_type != '-- None --':
        query = create_column(table, column, display_value, display_order, data_type, length, column_default)

    # DELETE A COLUMN
    if table != '-- None --' and column != '' and data_type == '-- None --':
        query = delete_column(table, column)

    # UPDATE COLUMNS (ALL :/)
    if len(update_data.keys()) > 0:
        query = update_column(update_data)

    # LOAD DATA
    df_tc = list_table_column()
    df_tc['character_maximum_length'].fillna('0', inplace=True)
    df_tc['character_maximum_length'] = df_tc['character_maximum_length'].astype(int)
    df_tc['column_display_order'] = df_tc['column_display_order'].astype(int)
    tl = list(df_tc['table'].unique())
    if table != '-- None --' and table != '-- none --':
        df_tc = df_tc[df_tc['table'] == table]
    #pd.options.display.float_format = '{:,.0f}'.format

    output = html_header()
    #output += query + '<br>\n'
    #output += str(im_dict) + '<br>\n'
    #output += str(table) + '<br>\n'
    #output += str(data_type) + '<br>\n'
    #output += str(update_data.keys()) + '<br>\n'



    output += '<form action="/admin/column/" method="POST">\n'
    output += '<table id="default">\n'
    output += '<tr><th>Table</th><th>Column</th><th>Display Value</th><th>Order</th><th>Data Type</th><th>Length</th><th>Default</th><th></th></tr>\n'

    # CREATE A NEW COLUMN
    output += '<tr>\n'
    output += '<td><select name="table" onchange="this.form.submit()">\n'
    output += '<option value="-- None --">-- None --</option>\n'
    #tmp = ''
    for t in tl:
        if str(t) == table:
            #t_dv = str(df_tc[df_tc['table'] == t]['table_display_value'].unique()[0])
            output += '<option value="' + str(t) + '" selected>' + str(t) + '</option>\n'
        else:
            #t_dv = str(df_tc[df_tc['table'] == t]['table_display_value'].unique()[0])
            output += '<option value="' + str(t) + '">' + str(t) + '</option>\n'
    output += '</select></td>\n'
    #output += tmp
    output += '<td><input type="text" name="column"></td>\n'
    output += '<td><input type="text" name="display_value"></td>\n'
    output += '<td><input type="text" name="display_order"></td>\n'
    output += '<td><select name="data_type">\n'
    output += '<option value="-- None --">-- None --</option>\n'
    output += '<option value="reference">Reference</option>\n'
    output += '<option value="dictionary">Dictionary</option>\n'
    output += '<option value="function">Function</option>\n'
    output += '<option value="boolean">Boolean</option>\n'
    output += '<option value="integer">Integer</option>\n'
    output += '<option value="float">Float</option>\n'
    output += '<option value="character varying">Character Varying</option>\n'
    output += '<option value="date">Date</option>\n'
    output += '</select></td>\n'
    #if data_type == 'float':
    #    output += '<td><input type="text" name="length" value="8,2"></td>\n'
    #elif data_type == 'character varying':
    #    output += '<td><input type="text" name="length" value="32"></td>\n'
    #else:
    #    output += '<td><input type="text" name="length"></td>\n'
    output += '<td><input type="text" name="length"></td>\n'
    output += '<td><input type="text" name="column_default"></td>\n'
    output += '<td><button type="submit" name="create_column" value=""><img src="/static/create.png" alt="Create" width="20"></button></td>'
    output += '</tr>\n'

    # LIST ALL TABLES AND COLUMNS
    for i in df_tc.iterrows():
        output += '<tr>'
        output += '<td>' + str(i[1]['table']) + '</td>'
        output += '<td>' + str(i[1]['column']) + '</td>'
        if str(i[1]['column']) == 'uuid' or str(i[1]['column']) == 'name' or str(i[1]['column']) == 'active':
            output += '<td>' + str(i[1]['column_display_value']) + '</td>'
        else:
            output += '<td><input type="text" name="display_value::' + str(i[1]['table']) + '::' + str(i[1]['column']) + '" value="' + str(i[1]['column_display_value']) + '"></td>'
        output += '<td><input type="text" name="display_order::' + str(i[1]['table']) + '::' + str(i[1]['column']) + '" value="' + str(i[1]['column_display_order']) + '"></td>'
        output += '<td>' + str(i[1]['data_type']) + '</td>'
        output += '<td>' + str(i[1]['character_maximum_length']) + '</td>'
        output += '<td>' + str(i[1]['column_default']) + '</td>'

        if str(i[1]['column']) == 'uuid' or str(i[1]['column']) == 'name' or str(i[1]['column']) == 'active':
            output += '<td><button type="submit" name="update_column" value="' + str(i[1]['table']) + '::' + str(i[1]['column']) + '"><img src="/static/update.png" alt="Update" width="20"></button></td>'
        else:
            output += '<td><button type="submit" name="update_column" value="' + str(i[1]['table']) + '::' + str(i[1]['column']) + '"><img src="/static/update.png" alt="Update" width="20"></button><button type="submit" name="delete_column" value="' + str(i[1]['table']) + '::' + str(i[1]['column']) + '"><img src="/static/delete.png" alt="Delete" width="20"></button></td>'
        output += '</tr>\n'
    output += '</table>\n'
    output += '</form>\n'
    # SQL DEBUG
    output += '<div class="tab">\n'
    output += '<button class="tablinks" onclick="openTab(event, \'SQL\')">SQL</button>\n'
    output += '</div>\n'
    output += '<div id="SQL" class="tabcontent">\n'
    output += '<p id="debug">' + str(query) + '</p>\n'
    output += '</div>\n'
    output += html_footer()
    return output

def list_table_column():
    tc_query = """
SELECT
  pg_catalog.pg_tables.tablename AS table,
  information_schema.columns.column_name AS column,
  information_schema.columns.data_type AS data_type,
  information_schema.columns.character_maximum_length AS character_maximum_length,
  information_schema.columns.column_default AS column_default
FROM pg_catalog.pg_tables
JOIN information_schema.columns ON pg_catalog.pg_tables.tablename = information_schema.columns.table_name
WHERE pg_catalog.pg_tables.tableowner = 'cmdb'
  AND pg_catalog.pg_tables.tablename NOT LIKE '_sys_%'
ORDER BY pg_catalog.pg_tables.tablename, information_schema.columns.ordinal_position
;
    """
    dv_query = """
SELECT sys_table, sys_table_column, display_value, sys_order FROM _sys_display_value;
    """
    conn = cmdb_connect()
    df_tc = pd.read_sql(text(tc_query), conn)
    df_dv = pd.read_sql(text(dv_query), conn)
    cmdb_disconnect(conn)
    #df_tc.to_csv('df_tc.csv', index=False)
    #df_dv.to_csv('df_dv.csv', index=False)
    df_tc['table_display_value'] = ''
    df_tc['column_display_value'] = ''
    df_tc['column_display_order'] = ''
    for i in df_dv[df_dv['sys_table_column'] == ''][['sys_table', 'display_value']].iterrows():
        df_tc.loc[(df_tc['table'] == i[1]['sys_table']), 'table_display_value'] = i[1]['display_value']
    for i in df_dv[df_dv['sys_table_column'].notna()][['sys_table', 'sys_table_column', 'display_value', 'sys_order']].iterrows():
        df_tc.loc[(df_tc['table'] == i[1]['sys_table']) & (df_tc['column'] == i[1]['sys_table_column']), 'column_display_value'] = i[1]['display_value']
        df_tc.loc[(df_tc['table'] == i[1]['sys_table']) & (df_tc['column'] == i[1]['sys_table_column']), 'column_display_order'] = i[1]['sys_order']
    #df_tc.to_csv('df_tc2.csv', index=False)
    df_tc = df_tc.sort_values(by=['table', 'column_display_order', 'column'])
    return df_tc


def create_column(table_name, column_name, display_value, display_order, type_name, length, column_default):
    query = ''
    dv_query = ''
    debug_query = ''
    column_name = column_name.lower().replace(' ', '_').replace('-', '_')
    if display_value == '':
        display_value = column_name
    if display_order == '':
        display_order = 10
    query += 'create # ' + str(table_name) + ' # ' + str(column_name) + ' # ' + str(display_value) + ' # ' + str(display_order) + ' # ' + str(type_name) + ' # ' + str(length) + ' # ' + str(column_default) + ' #<br>\n'

    # VARCHAR
    if type_name == 'character varying':
        query = """
ALTER TABLE """ + str(table_name) + """
ADD COLUMN """ + str(column_name) + """
VARCHAR(""" + str(length) + """)
DEFAULT '""" + str(column_default) + """'
;
"""
        dv_query = """
INSERT INTO _sys_display_value (display_value, sys_table, sys_table_column, sys_order, include)
VALUES ('""" + str(display_value) + """', '""" + str(table_name) + """', '""" + str(column_name) + """', """ + str(display_order) + """, false)
;
        """
        debug_query = query
        debug_query += '<br>\n'
        debug_query += dv_query

    # BOOLEAN
    if type_name == 'boolean':
        query = """
ALTER TABLE """ + str(table_name) + """
ADD COLUMN """ + str(column_name) + """
BOOLEAN """
        if column_default != '':
            query += """
DEFAULT """ + str(column_default)
        query += """;"""
        dv_query = """
INSERT INTO _sys_display_value (display_value, sys_table, sys_table_column, sys_order, include)
VALUES ('""" + str(display_value) + """', '""" + str(table_name) + """', '""" + str(column_name) + """', """ + str(display_order) + """, false)
;
        """
        debug_query = query
        debug_query += '<br>\n'
        debug_query += dv_query

    # INTEGER
    if type_name == 'integer':
        # ADD ZERO AS DEFAULT!
        query = """
ALTER TABLE """ + str(table_name) + """
ADD COLUMN """ + str(column_name) + """
INTEGER """
        if column_default != '':
            query += """
DEFAULT """ + str(column_default)
        query += """;"""
        dv_query = """
INSERT INTO _sys_display_value (display_value, sys_table, sys_table_column, sys_order, include)
VALUES ('""" + str(display_value) + """', '""" + str(table_name) + """', '""" + str(column_name) + """', """ + str(display_order) + """, false)
;
        """
        debug_query = query
        debug_query += '<br>\n'
        debug_query += dv_query

    # FLOAT
    if type_name == 'float':
        if length == '':
            length = '8, 2'
        replace_column_default = length.replace(' ', '').split(',')
        precicion = '0'
        scale = int(replace_column_default[1]) * '0'
        query = """
ALTER TABLE """ + str(table_name) + """
ADD COLUMN """ + str(column_name) + """
NUMERIC(""" + str(length) + """) """
        #if column_default != '':
        query += """
DEFAULT """ + str(precicion + '.' + scale)
        query += """;"""
        dv_query = """
INSERT INTO _sys_display_value (display_value, sys_table, sys_table_column, sys_order, include)
VALUES ('""" + str(display_value) + """', '""" + str(table_name) + """', '""" + str(column_name) + """', """ + str(display_order) + """, false)
;
        """
        debug_query = query
        debug_query += '<br>\n'
        debug_query += dv_query

    # DATE
    if type_name == 'date':
        query = """
ALTER TABLE """ + str(table_name) + """
ADD COLUMN """ + str(column_name) + """
DATE """
        if column_default != '':
            query += """
DEFAULT '""" + str(column_default) + """'"""
        query += """;"""
        dv_query = """
INSERT INTO _sys_display_value (display_value, sys_table, sys_table_column, sys_order, include)
VALUES ('""" + str(display_value) + """', '""" + str(table_name) + """', '""" + str(column_name) + """', """ + str(display_order) + """, false)
;
        """
        debug_query = query
        debug_query += '<br>\n'
        debug_query += dv_query

    # DICTIONARY
    if type_name == 'dictionary':
        query = 'foo'
        # FIRST CREATE THE DICTIONARY ENTRY
        dict_query = """
INSERT INTO _sys_dictionary (sys_table, sys_table_column, dict_value, sys_order)
VALUES ('""" + str(table_name) + """', '""" + str(column_name) + """', '-- None --', 10);
        """
        conn = cmdb_connect()
        conn.execute(text(dict_query))
        conn.commit()
        cmdb_disconnect(conn)

        # GET THE UUID FOR -- None --
        get_query = """
SELECT uuid FROM _sys_dictionary
WHERE sys_table = '""" + str(table_name) + """'
  AND sys_table_column = '""" + str(column_name) + """'
  AND dict_value = '-- None --';
        """
        conn = cmdb_connect()
        rows = conn.execute(text(get_query))
        uuid = []
        for row in rows:
            uuid = row[0]
        cmdb_disconnect(conn)

        # ACTUALLY CREATE THE NEW COLUMN WITH NEW DEFAULT
        query = """
ALTER TABLE """ + str(table_name) + """
ADD COLUMN """ + str(column_name) + """
VARCHAR(""" + str(len(uuid)) + """)
DEFAULT '""" + str(uuid) + """'
;
"""
        dv_query = """
INSERT INTO _sys_display_value (display_value, sys_table, sys_table_column, sys_order, include)
VALUES ('""" + str(display_value) + """', '""" + str(table_name) + """', '""" + str(column_name) + """', """ + str(display_order) + """, false)
;
"""
        #debug_query = dict_query
        #debug_query += '<br>\n'
        #debug_query += get_query
        #debug_query += '<br>\n'
        #debug_query += str(uuid)
        #debug_query += '<br>\n'

    if type_name == 'reference':
        # FIRST CREATE THE REFERENCE ENTRY
        ref_query = """
INSERT INTO _sys_reference (source, target)
VALUES ('""" + str(table_name) + """', '""" + str(column_name) + """');
        """
        conn = cmdb_connect()
        conn.execute(text(ref_query))
        conn.commit()
        cmdb_disconnect(conn)

        # GET THE UUID FOR -- None --
        get_query = """
SELECT uuid FROM """ + str(column_name) + """
WHERE name = '-- None --'
;
        """
        conn = cmdb_connect()
        rows = conn.execute(text(get_query))
        uuid = []
        for row in rows:
            uuid = row[0]
        cmdb_disconnect(conn)

        # ACTUALLY CREATE THE NEW COLUMN WITH NEW DEFAULT
        query = """
ALTER TABLE """ + str(table_name) + """
ADD COLUMN """ + str(column_name) + """
VARCHAR(""" + str(len(uuid)) + """)
DEFAULT '""" + str(uuid) + """'
;
"""
        dv_query = """
INSERT INTO _sys_display_value (display_value, sys_table, sys_table_column, sys_order, include)
VALUES ('""" + str(display_value) + """', '""" + str(table_name) + """', '""" + str(column_name) + """', """ + str(display_order) + """, false)
;
"""

    if type_name == 'function':
        # FIRST CREATE THE NEW FUNCTION ENTRY
        func_query = """
INSERT INTO _sys_function (sys_table, sys_table_column, function_name)
VALUES ('""" + str(table_name) + """', '""" + str(column_name) + """', '""" + str(column_name) + """')
        """
        conn = cmdb_connect()
        conn.execute(text(func_query))
        conn.commit()
        cmdb_disconnect(conn)

        # ACTUALLY CREATE THE NEW COLUMN
        query = """
ALTER TABLE """ + str(table_name) + """
ADD COLUMN """ + str(column_name) + """
VARCHAR(1)
;
"""
        dv_query = """
INSERT INTO _sys_display_value (display_value, sys_table, sys_table_column, sys_order, include)
VALUES ('""" + str(display_value) + """', '""" + str(table_name) + """', '""" + str(column_name) + """', """ + str(display_order) + """, false)
;
"""

    # CREATE NEW COLUMN
    if query[0:9] != 'create # ':
        conn = cmdb_connect()
        conn.execute(text(query))
        conn.execute(text(dv_query))
        conn.commit()
        cmdb_disconnect(conn)
    else:
        debug_query = query

    return debug_query

def delete_column(table, column):
    query = """
ALTER TABLE """ + str(table) + """ DROP COLUMN """ + str(column) + """;
    """
    dv_query = """
DELETE FROM _sys_display_value WHERE sys_table = '""" + str(table) + """' AND sys_table_column = '""" + str(column) + """';
    """
    dict_query = """
DELETE FROM _sys_dictionary WHERE sys_table = '""" + str(table) + """' AND sys_table_column = '""" + str(column) + """';
    """
    func_query = """
DELETE FROM _sys_function WHERE sys_table = '""" + str(table) + """' AND sys_table_column = '""" + str(column) + """';
    """
    ref_query_source = """
DELETE FROM _sys_reference WHERE source = '""" + str(table) + """' AND target = '""" + str(column) + """';
    """
#    ref_query_target = """
#DELETE FROM _sys_reference WHERE target = '""" + str(table) + """';
#    """
    debug_query = query
    debug_query += '<br>\n'
    debug_query += dv_query
    conn = cmdb_connect()
    conn.execute(text(query))
    conn.execute(text(dv_query))
    conn.execute(text(dict_query))
    conn.execute(text(func_query))
    conn.execute(text(ref_query_source))
    #conn.execute(text(ref_query_target))
    conn.commit()
    cmdb_disconnect(conn)
    return debug_query

def update_column(update_data):
    query = ''
    for key in update_data.keys():
        if key[:13] == 'display_value' and update_data[key] != '':
            skey = key.split('::')
            query += """
UPDATE _sys_display_value
SET display_value = '""" + str(update_data[key]) + """'
WHERE sys_table = '""" + str(skey[1]) + """'
AND sys_table_column = '""" + str(skey[2]) + """'
;\n
            """
        if key[:13] == 'display_order' and update_data[key] != '':
            skey = key.split('::')
            query += """
UPDATE _sys_display_value
SET sys_order = """ + str(update_data[key]) + """
WHERE sys_table = '""" + str(skey[1]) + """'
AND sys_table_column = '""" + str(skey[2]) + """'
;\n
            """
    conn = cmdb_connect()
    conn.execute(text(query))
    conn.commit()
    cmdb_disconnect(conn)
    return query



