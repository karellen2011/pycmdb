from sqlalchemy import create_engine, text
import pandas as pd

from cmdbhtml import html_header, html_footer
#from cmdbdb import cmdb_connect, cmdbdb.cmdb_disconnect
from adminfunction import get_functions
import cmdbdb

def adminlistcolumns(form_data):

    update_key = ''
    update_data = {}
    update_query = ''

    if 'action' in form_data.keys() and form_data['action'] == 'insert':
        create_column(form_data)
    if 'drop_column' in form_data.keys():
        table = form_data['drop_column'].split('::')[0]
        column = form_data['drop_column'].split('::')[1]
        delete_column(table, column)
    if 'update_column' in form_data.keys():
        update_key = '::' + str(form_data['update_column'])
        for key in form_data.keys():
            if key[len(key)-len(update_key):] == update_key:
                update_data[key[:-len(update_key)]] = form_data[key]
        if update_data != {}:
            table = form_data['table']
            column = update_key.split('::')[2]
            update_query = update_column(table, column, update_data)



    data_tmp = {'sys_table': [''], 'display_value': ['']}
    df_tmp = pd.DataFrame(data_tmp)
    df_tmp_tablelist = cmdbdb.get_tablelist()
    df_tablelist = pd.concat([df_tmp, df_tmp_tablelist])
    table = ''
    if 'table' in form_data.keys():
        table = form_data['table']

    data_type = ''
    if 'data_type' in form_data.keys():
        data_type = form_data['data_type']

    output = html_header()
    #output += str(update_key) + '<br>\n'
    #output += str(update_data) + '<br>\n'
    #output += str(update_query) + '<br>\n'
    #output += '<br>\n'
    #output += str(form_data) + '<br>\n'
    #output += str(table) + '<br>\n'
    output += '<form action="/admin/column/" method="POST">\n'
    output += '<table id="default">\n'
    output += '<tr><th>Table</th><th>Data Type</th><th>Length</th><th>Default</th><th>Column</th><th>Display Value</th><th>Display Order</th><th>Include</th><th>Hide</th><th></th></tr>'

    # LIST TABLES
    output += '<tr>'
    output += '<td><select name="table" onchange="this.form.submit()">\n'
    for i in df_tablelist.iterrows():
        if table ==  i[1]['sys_table']:
            output += '<option value="' + i[1]['sys_table'] + '" selected>' + i[1]['display_value'] + '</option>\n'
        else:
            output += '<option value="' + i[1]['sys_table'] + '">' + i[1]['display_value'] + '</option>\n'
    output += '</select>\n'
    output += '</td>'

    # LIST COLUMN
    if table != '':
        data_type_dict = {'': '', 'reference': 'Reference', 'dictionary': 'Dictionary', 'function': 'Function', 'boolean': 'Boolean', 'integer': 'Integer', 'float': 'Float', 'character varying': 'Character Varying', 'date': 'Date'}
        output += '<td><select name="data_type" onchange="this.form.submit()">\n'
        for key in data_type_dict:
            if data_type == key:
                output += '<option value="' + str(key) + '" selected>' + str(data_type_dict[key]) + '</option>\n'
            else:
                output += '<option value="' + str(key) + '">' + str(data_type_dict[key]) + '</option>\n'
        output += '</select></td>\n'
        if data_type != '':
            if data_type == 'reference':
                df_ref = cmdbdb.get_tablelist()
                output += '<td></td><td></td>\n'
                output += '<td><select name="column">\n'
                for ref in df_ref.iterrows():
                    if table != ref[1]['sys_table']:
                        output += '<option value="' + ref[1]['sys_table'] + '">' + ref[1]['display_value'] + '</option>\n'
                output += '</select></td>\n'
            elif data_type == 'dictionary':
                output += '<td></td><td></td>\n'
                output += '<td><input type="text" name="column"></td>\n'
            elif data_type == 'function':
                output += '<td></td><td></td>\n'
                df_fun = get_functions()
                output += '<td><select name="column">\n'
                for fun in df_fun.iterrows():
                    output += '<option value="' + fun[1]['Name'] + '">' + fun[1]['Name'] + '</option>\n'
                output += '</select></td>\n'
            elif data_type == 'boolean':
                output += '<td></td>\n'
                output += '<td><select name="column_default">\n'
                output += '<option value=""></option>\n'
                output += '<option value="true">True</option>\n'
                output += '<option value="false">False</option>\n'
                output += '</select></td>\n'
                output += '<td>'
                output += '<input type="text" name="column">'
                output += '</td>\n'
            elif data_type == 'character varying':
                output += '<td>\n'
                output += '<input type="text" name="length" value="256">\n'
                output += '</td>'
                output += '<td>\n'
                output += '<input type="text" name="column_default">'
                output += '</td>'
                output += '<td>'
                output += '<input type="text" name="column">'
                output += '</td>\n'
            elif data_type == 'integer':
                output += '<td>\n'
                #output += '<input type="text" name="length" value="256">\n'
                output += '</td>'
                output += '<td>\n'
                output += '<input type="text" name="column_default" value="0">'
                output += '</td>'
                output += '<td>'
                output += '<input type="text" name="column">'
                output += '</td>\n'
            elif data_type == 'float':
                output += '<td>\n'
                output += '<input type="text" name="length" value="8,2">\n'
                output += '</td>'
                output += '<td>\n'
                output += '<input type="text" name="column_default" value="0.0">'
                output += '</td>'
                output += '<td>'
                output += '<input type="text" name="column">'
                output += '</td>\n'
            elif data_type == 'date':
                output += '<td>\n'
                #output += '<input type="text" name="length" value="8,2">\n'
                output += '</td>'
                output += '<td>\n'
                output += '<input type="text" name="column_default" value="1970-01-01">'
                output += '</td>'
                output += '<td>'
                output += '<input type="text" name="column">'
                output += '</td>\n'
            output += '<td>'
            output += '<input type="text" name="column_display_value">'
            output += '</td>\n'
            output += '<td>'
            output += '<input type="text" name="sys_order">'
            output += '</td>\n'
            output += '<td>'
            output += '<select name="include">\n'
            output += '<option value="true">True</option>\n'
            output += '<option value="false" selected>False</option>\n'
            output += '</select></td>\n'
            output += '<td>'
            output += '<select name="hide">\n'
            output += '<option value="true">True</option>\n'
            output += '<option value="false" selected>False</option>\n'
            output += '</select></td>\n'
            output += '<td><button type="submit" name="action" value="insert"><img src="/static/create.png" alt="Insert" width="20"></button></td>\n'
        else:
            output += '<td></td><td></td><td></td><td></td><td></td><td></td><td></td>'
    else:
        output += '<td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>'
    output += '</tr>'

    # LIST TABLE STRUCTURE
    if table != '':
        df_table_structure = cmdbdb.get_table_structure(table)
        for row in df_table_structure.iterrows():
            output += '<tr>'
            #for col in df_table_structure.columns:
            #    output += '<td>' + str(row[1][col]) + '</td>\n'
            output += '<td>' + str(row[1]['table']) + '</td>\n'
            output += '<td>' + str(row[1]['data_type']) + '</td>\n'
            output += '<td>' + str(row[1]['character_maximum_length']) + '</td>\n'
            output += '<td>' + str(row[1]['column_default']) + '</td>\n'
            output += '<td>' + str(row[1]['column']) + '</td>\n'
            if row[1]['column'] == 'uuid':
                output += '<td>' + str(row[1]['display_value']) + '</td>\n'
            else:
                output += '<td><input type="text" name="display_value::' + str(table) + '::' + str(row[1]['column']) + '" value="' + str(row[1]['display_value']) + '"></td>\n'
            output += '<td><input type="text" name="sys_order::' + str(table) + '::' + str(row[1]['column']) + '" value="' + str(row[1]['sys_order']) + '"></td>\n'
            output += '<td><select name="include::' + str(table) + '::' + str(row[1]['column']) + '">\n'
            for boolean in ['True', 'False']:
                if str(row[1]['include']) == boolean:
                    output += '<option value="' + boolean.lower() + '" selected>' + boolean + '</option>\n'
                else:
                    output += '<option value="' + boolean.lower() + '">' + boolean + '</option>\n'
            output += '</select></td>\n'
            output += '<td><select name="hide::' + str(table) + '::' + str(row[1]['column']) + '">\n'
            for boolean in ['True', 'False']:
                if str(row[1]['hide']) == boolean:
                    output += '<option value="' + boolean.lower() + '" selected>' + boolean + '</option>\n'
                else:
                    output += '<option value="' + boolean.lower() + '">' + boolean + '</option>\n'
            output += '</select></td>\n'
            output += '<td>'
            output += '<button type="submit" name="update_column" value="' + str(table) + '::' + str(row[1]['column']) + '"><img src="/static/update.png" alt="Update" width="20"></button>'
            if str(row[1]['column']) != 'uuid' and str(row[1]['column']) != 'name' and str(row[1]['column']) != 'active':
                output += '<button type="submit" name="drop_column" value="' + str(table) + '::' + str(row[1]['column']) + '"><img src="/static/delete.png" alt="Drop" width="20"></button>'
            output += '</td>'
            output += '</tr>\n'

    output += '</table>\n'
    output += '<form>\n'
    output += html_footer()
    return output

def create_column(form_data):
    table_name = form_data['table']
    column_name = form_data['column']
    display_value = form_data['column_display_value']
    display_order = form_data['sys_order']
    type_name = form_data['data_type']
    length = 0
    if length in form_data.keys():
        length = form_data['length']
    column_default = ''
    if column_default in form_data.keys():
        column_default = form_data['column_default']
    include = form_data['include']
    hide = form_data['hide']

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
INSERT INTO _sys_display_value (display_value, sys_table, sys_table_column, sys_order, include, hide)
VALUES ('""" + str(display_value) + """', '""" + str(table_name) + """', '""" + str(column_name) + """', """ + str(display_order) + """, """ + str(include) + """, """ + str(hide) + """)
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
INSERT INTO _sys_display_value (display_value, sys_table, sys_table_column, sys_order, include, hide)
VALUES ('""" + str(display_value) + """', '""" + str(table_name) + """', '""" + str(column_name) + """', """ + str(display_order) + """, """ + str(include) + """, """ + str(hide) + """)
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
INSERT INTO _sys_display_value (display_value, sys_table, sys_table_column, sys_order, include, hide)
VALUES ('""" + str(display_value) + """', '""" + str(table_name) + """', '""" + str(column_name) + """', """ + str(display_order) + """, """ + str(include) + """, """ + str(hide) + """)
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
INSERT INTO _sys_display_value (display_value, sys_table, sys_table_column, sys_order, include, hide)
VALUES ('""" + str(display_value) + """', '""" + str(table_name) + """', '""" + str(column_name) + """', """ + str(display_order) + """, """ + str(include) + """, """ + str(hide) + """)
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
INSERT INTO _sys_display_value (display_value, sys_table, sys_table_column, sys_order, include, hide)
VALUES ('""" + str(display_value) + """', '""" + str(table_name) + """', '""" + str(column_name) + """', """ + str(display_order) + """, """ + str(include) + """, """ + str(hide) + """)
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
        conn = cmdbdb.cmdb_connect()
        conn.execute(text(dict_query))
        conn.commit()
        cmdbdb.cmdb_disconnect(conn)

        # GET THE UUID FOR -- None --
        get_query = """
SELECT uuid FROM _sys_dictionary
WHERE sys_table = '""" + str(table_name) + """'
  AND sys_table_column = '""" + str(column_name) + """'
  AND dict_value = '-- None --';
        """
        conn = cmdbdb.cmdb_connect()
        rows = conn.execute(text(get_query))
        uuid = []
        for row in rows:
            uuid = row[0]
        cmdbdb.cmdb_disconnect(conn)

        # ACTUALLY CREATE THE NEW COLUMN WITH NEW DEFAULT
        query = """
ALTER TABLE """ + str(table_name) + """
ADD COLUMN """ + str(column_name) + """
VARCHAR(""" + str(len(uuid)) + """)
DEFAULT '""" + str(uuid) + """'
;
"""
        dv_query = """
INSERT INTO _sys_display_value (display_value, sys_table, sys_table_column, sys_order, include, hide)
VALUES ('""" + str(display_value) + """', '""" + str(table_name) + """', '""" + str(column_name) + """', """ + str(display_order) + """, """ + str(include) + """, """ + str(hide) + """)
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
        conn = cmdbdb.cmdb_connect()
        conn.execute(text(ref_query))
        conn.commit()
        cmdbdb.cmdb_disconnect(conn)

        # GET THE UUID FOR -- None --
        get_query = """
SELECT uuid FROM """ + str(column_name) + """
WHERE name = '-- None --'
;
        """
        conn = cmdbdb.cmdb_connect()
        rows = conn.execute(text(get_query))
        uuid = []
        for row in rows:
            uuid = row[0]
        cmdbdb.cmdb_disconnect(conn)

        # ACTUALLY CREATE THE NEW COLUMN WITH NEW DEFAULT
        query = """
ALTER TABLE """ + str(table_name) + """
ADD COLUMN """ + str(column_name) + """
VARCHAR(""" + str(len(uuid)) + """)
DEFAULT '""" + str(uuid) + """'
;
"""
        dv_query = """
INSERT INTO _sys_display_value (display_value, sys_table, sys_table_column, sys_order, include, hide)
VALUES ('""" + str(display_value) + """', '""" + str(table_name) + """', '""" + str(column_name) + """', """ + str(display_order) + """, """ + str(include) + """, """ + str(hide) + """)
;
        """

    if type_name == 'function':
        # FIRST CREATE THE NEW FUNCTION ENTRY
        func_query = """
INSERT INTO _sys_function (sys_table, sys_table_column, function_name)
VALUES ('""" + str(table_name) + """', '""" + str(column_name) + """', '""" + str(column_name) + """')
        """
        conn = cmdbdb.cmdb_connect()
        conn.execute(text(func_query))
        conn.commit()
        cmdbdb.cmdb_disconnect(conn)

        # ACTUALLY CREATE THE NEW COLUMN
        query = """
ALTER TABLE """ + str(table_name) + """
ADD COLUMN """ + str(column_name) + """
VARCHAR(1)
;
"""
        dv_query = """
INSERT INTO _sys_display_value (display_value, sys_table, sys_table_column, sys_order, include, hide)
VALUES ('""" + str(display_value) + """', '""" + str(table_name) + """', '""" + str(column_name) + """', """ + str(display_order) + """, """ + str(include) + """, """ + str(hide) + """)
;
        """

    # CREATE NEW COLUMN
    if query[0:9] != 'create # ':
        conn = cmdbdb.cmdb_connect()
        conn.execute(text(query))
        conn.execute(text(dv_query))
        conn.commit()
        cmdbdb.cmdb_disconnect(conn)
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
-- DELETE FROM _sys_reference WHERE source = '""" + str(table) + """' AND target = '""" + str(column) + """';
DELETE FROM _sys_reference WHERE source = '""" + str(table) + """';
    """
#    ref_query_target = """
#DELETE FROM _sys_reference WHERE target = '""" + str(table) + """';
#    """
    debug_query = query
    debug_query += '<br>\n'
    debug_query += dv_query
    conn = cmdbdb.cmdb_connect()
    conn.execute(text(query))
    conn.execute(text(dv_query))
    conn.execute(text(dict_query))
    conn.execute(text(func_query))
    conn.execute(text(ref_query_source))
    #conn.execute(text(ref_query_target))
    conn.commit()
    cmdbdb.cmdb_disconnect(conn)
    return debug_query

def update_column(table, column, update_data):
    query = """
UPDATE _sys_display_value SET 
display_value = '""" + str(update_data['display_value']) + """',
sys_order = """ + str(update_data['sys_order']) + """,
include = """ + str(update_data['include']) + """,
hide = """ + str(update_data['hide']) + """
WHERE sys_table = '""" + str(table) + """' 
AND sys_table_column = '""" + str(column) + """'
;
"""
    conn = cmdbdb.cmdb_connect()
    conn.execute(text(query))
    conn.commit()
    cmdbdb.cmdb_disconnect(conn)
    return query

