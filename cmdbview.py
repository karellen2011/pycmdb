import importlib.util
import sys
from sqlalchemy import create_engine, text
import pandas as pd

from cmdbhtml import html_header, html_footer
from cmdbdb import cmdb_connect, cmdb_disconnect

def cmdbview(table, uuid, data):

    # UPDATE BEFORE LOADING NEW
    update_query = ''
    if len(data.keys()) > 0:
        update_query += update_data(table, uuid, data)

    df, query = get_data(table, uuid)
    df_dv = get_display_value(table)
    df_dict = get_dict(table)
    table_display_value = get_table_display_value(table)

    display_columns = 2
    colspan = 2 * display_columns
    col_count = 0

    # LOAD ADDITIONAL FUNCTIONS
    function_list = list(df_dv[df_dv['data_type'] == 'function']['sys_table_column'])
    for function_name in function_list:
        function_file = 'function/' + function_name + '/function.py'
        #function = importlib.import_module(function_name, package=None)
        spec = importlib.util.spec_from_file_location('once', function_file)
        function = importlib.util.module_from_spec(spec)
        sys.modules['once'] = function
        spec.loader.exec_module(function)

    output = html_header()
    #output += str(table) + ' ' + str(uuid) + '<br>\n'
    #output += str(update_query) + '<br>\n'
    output += '<form action="/view/' + str(table) + '/' + str(uuid) + '" method="POST">\n'
    output += '<table id="default">\n'
    output += '<tr><th colspan="' + str(colspan) + '"><a id="headerlink" href="/table/list/' + str(table) + '">' + str(table_display_value) + '</a> > ' + str(df['name'].iloc[0]) + ' <button type="submit" name="update" value="update"><img src="/static/update.png" alt="Create" width="20"></button></th></tr>\n'
    output += '<tr>\n'
    #for cc, col in enumerate(list(df.columns)):
    df_dv = df_dv[df_dv['data_type'] != 'reference']
    for cc, col in enumerate(list(df_dv['sys_table_column'])):
        #if cc % display_columns == 0:
        #    output += '<tr>'
        col_dv = df_dv[df_dv['sys_table_column'] == col]['display_value'].iloc[0]
        data_type = df_dv[df_dv['sys_table_column'] == col]['data_type'].iloc[0]
        #if col in df_dict['sys_table_column'].unique():
        #    data_type = 'dictionary'
        #output += '<tr>'
        #output += '<td>' + str(col) + '</td>'
        #mc = cc % display_columns
        #dd = cc // display_columns
        #output += '<td>' + str(cc) + ' ' + str(mc) + ' ' + str(dd) + ' ' + str(col_dv)
        output += '<td>' + str(col_dv)
        #output += ' (' + str(data_type) + ')'
        output += '</td>'
        if data_type == 'character varying' and col == 'uuid':
            output += '<td>' + str(df[col].iloc[0]) + '</td>'
        elif data_type == 'character varying' and col != 'uuid':
            if str(df[col].iloc[0]) != '-- None --':
                output += '<td><input type="text" name="' + str(col) + '" value="' + str(df[col].iloc[0]) + '"></td>'
            #else:
            #     output += '<td>-- None --</td>'
        elif data_type == 'boolean':
            sel_list = ['True', 'False']
            output += '\n<td><select name="' + str(col) + '">\n'
            for sl in sel_list:
                if sl == str(df[col].iloc[0]):
                    output += '<option value="' + str(sl) + '" selected>' + str(sl) + '</option>\n'
                else:
                    output += '<option value="' + str(sl) + '">' + str(sl) + '</option>\n'
            output += '</select></td>'
        elif data_type == 'dictionary':
            df_sel = df_dict[df_dict['sys_table_column'] == str(col)]
            dict_color = df_sel[df_sel['uuid'] == str(df[col].iloc[0])]['color'].iloc[0]
            #dict_value = df_sel[df_sel['uuid'] == str(df[col].iloc[0])]['dict_value'].iloc[0]
            #df_sel.to_csv('df_sel.csv', index=False)
            output += '<td style="background:#' + str(dict_color) + ';">\n'
            #output += str(df[col].iloc[0]) + '<br>\n'
            #output += str(dict_color) + '<br>\n'
            #output += str(dict_value) + '<br>\n'
            #output += str(col) + '<br>\n'
            output += '<select name="' + str(col) + '">\n'
            for sl in df_sel.iterrows():
                if sl[1]['uuid'] == str(df[col].iloc[0]):
                    output += '<option value="' + sl[1]['uuid'] + '" selected>' + sl[1]['dict_value'] + '</option>\n'
                else:
                    output += '<option value="' + sl[1]['uuid'] + '">' + sl[1]['dict_value'] + '</option>\n'
            output += '</select></td>'
        elif data_type == 'integer':
            output += '<td><input type="text" name="' + str(col) + '" value="' + str(df[col].iloc[0]) + '"></td>'
        elif data_type == 'numeric':
            output += '<td><input type="text" name="' + str(col) + '" value="' + str(df[col].iloc[0]) + '"></td>'
        elif data_type == 'date':
            output += '<td><input type="text" name="' + str(col) + '" value="' + str(df[col].iloc[0]) + '"></td>'
        elif data_type == 'function':
            output += '<td>'
            output += str(function.functioncall(df['uuid'].iloc[0])) + '<br>'
            output += '</td>'
        else:
            output += '<td>' + str(df[col].iloc[0]) + '</td>'
        #if cc > 0 and cc % display_columns != 0:
        #    output += '</tr><tr>\n'
        col_count += 1
        if col_count == display_columns:
            col_count = 0
            output += '\n</tr><tr>\n'
    if col_count != 0:
        while col_count < display_columns:
            output += '<td></td><td></td>'
            col_count += 1
    output += '\n</tr>\n'
    output += '</table>\n'
    
    # DISPLAY REFERENCES
    df_dv = get_display_value(table)
    df_dv = df_dv[df_dv['data_type'] == 'reference']
    for cc, col in enumerate(list(df_dv['sys_table_column'])):
        col_dv = df_dv[df_dv['sys_table_column'] == col]['display_value'].iloc[0]
        df_ref, query_ref = get_data(col, df[col].iloc[0])
        df_dv_ref = get_display_value(col)
        df_dict_ref = get_dict(col)
        col_count = 0
        output += '<table id="default">\n'
        output += '<tr><th colspan="' + str(colspan) + '">'
        output += '<a id="headerlink" href="/table/list/' + str(col) + '/">' + str(col_dv) + '</a>'
        output += ' > '
        output += '<a id="headerlink" href="/view/' + str(col) + '/' + str(df_ref['uuid'].iloc[0]) + '/">' + str(df_ref['name'].iloc[0]) + '</a>'
        output +=  '</th></tr>\n'
        output += '<tr>\n'
        for cc, col_ref in enumerate(list(df_dv_ref['sys_table_column'])):
            col_dv_ref = df_dv_ref[df_dv_ref['sys_table_column'] == col_ref]['display_value'].iloc[0]
            data_type_ref = df_dv_ref[df_dv_ref['sys_table_column'] == col_ref]['data_type'].iloc[0]
            if col_ref != 'uuid':
                if data_type_ref == 'character varying' and col_ref != 'uuid':
                    if col_ref == 'name':
                        df_ref_ref = get_ref_table(col)
                        output += '<td>' + str(col_dv_ref) + '</td>'
                        output += '<td>'
                        output += '<select name="' + str(col) + '">\n'
                        for ref_ref in df_ref_ref.iterrows():
                            if ref_ref[1]['uuid'] == str(df_ref['uuid'].iloc[0]):
                                output += '<option value="' + ref_ref[1]['uuid'] + '" selected>' + ref_ref[1]['name'] + '</option>\n'
                            else:
                                output += '<option value="' + ref_ref[1]['uuid'] + '">' + ref_ref[1]['name'] + '</option>\n'
                        output += '<select> <a href="/view/' + str(col) + '/' + str(df_ref['uuid'].iloc[0]) + '/">\n'
                        #output += '<br>\n'
                        #output += '<a href="/view/' + str(col) + '/' + str(df_ref['uuid'].iloc[0]) + '/">' + str(df_ref[col_ref].iloc[0]) + '</a><br>'
                        output += '</td>'
                    else:
                        output += '<td>' + str(col_dv_ref) + '</td>'
                        output += '<td>' + str(df_ref[col_ref].iloc[0]) + '</td>'
                elif data_type_ref == 'dictionary':
                    #df_sel = df_dict[df_dict['sys_table_column'] == str(col)]
                    #dict_color = df_sel[df_sel['uuid'] == str(df[col].iloc[0])]['color'].iloc[0]
                    dict_value_ref = df_dict_ref[df_dict_ref['uuid'] == df_ref[col_ref].iloc[0]]['dict_value'].iloc[0]
                    dict_color_ref = df_dict_ref[df_dict_ref['uuid'] == df_ref[col_ref].iloc[0]]['color'].iloc[0]
                    #output += '<td>' + str(col_dv_ref) + ' ' + str(col_dv) + '</td>'
                    output += '<td>' + str(col_dv_ref) + '</td>'
                    output += '<td style="background:#' + str(dict_color_ref) + ';">' + str(dict_value_ref) + '</td>'
                elif data_type_ref == 'reference':
                    df_rs = get_ref_table_single(col_ref, df_ref[col_ref].iloc[0])
                    #output += '<td>' + str(col_ref) + '  ' + str(col_dv_ref) + '</td>'
                    #output += '<td>' + str(df_ref[col_ref].iloc[0]) + '</td>'
                    output += '<td>' + str(col_dv_ref) + '</td>\n'
                    output += '<td><a href="/view/' + str(col_ref) + '/' + str(df_rs['uuid'].iloc[0]) + '/">' + str(df_rs['name'].iloc[0]) + '</a></td>\n'

                else:
                    #output += '<td>' + str(col_ref) + '  ' + str(col_dv_ref) + '</td>'
                    output += '<td>' + str(col_dv_ref) + '</td>'
                    output += '<td>' + str(df_ref[col_ref].iloc[0]) + '</td>'

                col_count += 1
                if col_count == display_columns:
                    col_count = 0
                    output += '\n</tr><tr>\n'
        if col_count != 0:
            while col_count < display_columns:
                output += '<td></td><td></td>'
                col_count += 1

        output += '</tr>\n'
        output += '</table>\n'
    output += '</form>\n'

    # BACKWARD REFERENCE(S)
    df_br = get_backwards_reference(table)
    uuid = df['uuid'].iloc[0]
    for row in df_br.iterrows():
        output += '<table id="default">\n'
        output += '<tr><th colspan="' + str(colspan) + '">'
        output += '<a id="headerlink" href="/table/list/' + str(row[1]['source']) + '/">' + str(row[1]['source']) + '</a>'
        #output += str(row[1]['source']) + ' '  + str(uuid) + '<br>\n' 
        output += '</th></tr>\n'
        output += '</table>\n'
        df_brd = get_backwards_reference_data(table, row[1]['source'], uuid)
        output += '<table id="default">\n'
        output += '<tr>'
        for col in df_brd.columns:
            if str(col) != 'uuid' and col != table:
                output += '<th>' + str(col) + '</th>'
        output += '</tr>\n'
        for rowd in df_brd.iterrows():
            output += '<tr>'
            for col in df_brd.columns:
                if col != 'uuid' and col != table:
                    if col == 'name':
                        output += '<td><a href="/view/' + str(row[1]['source']) + '/' + str(rowd[1]['uuid']) + '/">' + str(rowd[1][col]) + '</a></td>'
                    else:
                        output += '<td>' + str(rowd[1][col]) + '</td>'
            output += '</tr>\n'
        output += '</table>\n'

    output += '<div class="tab">\n'
    output += '<button class="tablinks" onclick="openTab(event, \'Select\')">Select</button>\n'
    output += '</div>\n'
    output += '<div id="Select" class="tabcontent">\n'
    output += '<p id="debug">' + str(query).replace('\n', '<br>\n') + '</p>\n'
    output += '</div>\n'
    output += html_footer()
    return output

def get_data(table, uuid):
    query = """
SELECT *
FROM """ + str(table) + """
WHERE uuid = '""" + str(uuid) + """'
;
    """
    conn = cmdb_connect()
    df = pd.read_sql(text(query), conn)
    cmdb_disconnect(conn)
    return df, query

def get_display_value(table):
    query = """
SELECT
  sys_table,
  sys_table_column,
  display_value,
  sys_order,
  information_schema.columns.data_type AS data_type,
  information_schema.columns.column_default AS column_default,
  include
FROM _sys_display_value
JOIN information_schema.columns ON sys_table_column = information_schema.columns.column_name
WHERE sys_table = '""" + str(table) + """'
  AND sys_table_column <> ''
  AND information_schema.columns.table_name = _sys_display_value.sys_table
ORDER BY sys_order, display_value
;
    """
    conn = cmdb_connect()
    df = pd.read_sql(text(query), conn)
    cmdb_disconnect(conn)
    df_dict = get_dict(table)
    df_ref = get_ref(table)
    df_func = get_function(table)
    for i in df.iterrows():
        if i[1]['sys_table_column'] in list(df_dict['sys_table_column'].unique()):
            df.loc[(df['sys_table_column'] == i[1]['sys_table_column']), 'data_type'] = 'dictionary'
        if i[1]['sys_table_column'] in list(df_ref['target']):
            df.loc[(df['sys_table_column'] == i[1]['sys_table_column']), 'data_type'] = 'reference'
        if i[1]['sys_table_column'] in list(df_func['sys_table_column']):
            df.loc[(df['sys_table_column'] == i[1]['sys_table_column']), 'data_type'] = 'function'
    # INCLUDE
    #for ref in df[df['data_type'] == 'reference'].iterrows():
    #    ref_table = (ref[1]['sys_table_column'])
    #    df_inc = get_display_value_include(ref_table)
    #    if df_inc.shape[0] > 0:
    #        df = pd.concat([df, df_inc])
    return df

def get_dict(table):
    query = """
SELECT uuid, sys_table_column, dict_value, color
FROM _sys_dictionary
WHERE sys_table = '""" + str(table) + """'
ORDER BY sys_table_column, sys_order, dict_value
;
    """
    conn = cmdb_connect()
    df = pd.read_sql(text(query), conn)
    cmdb_disconnect(conn)
    return df

def get_ref(table):
    query = """
SELECT target
FROM _sys_reference
WHERE source = '""" + str(table) + """'
;
    """
    conn = cmdb_connect()
    df = pd.read_sql(text(query), conn)
    cmdb_disconnect(conn)
    return df

def get_function(table):
    query = """
SELECT sys_table, sys_table_column, function_name
FROM _sys_function
WHERE sys_table = '""" + str(table) + """'
;
    """
    conn = cmdb_connect()
    df = pd.read_sql(text(query), conn)
    cmdb_disconnect(conn)
    return df

def get_ref_table(table):
    query = """
SELECT uuid, name
FROM """ + str(table) + """
ORDER BY name
;
    """
    conn = cmdb_connect()
    df = pd.read_sql(text(query), conn)
    cmdb_disconnect(conn)
    return df

def get_ref_table_single(table, uuid):
    query = """
SELECT uuid, name
FROM """ + str(table) + """
WHERE uuid ='""" + str(uuid) + """'
ORDER BY name
;
    """
    conn = cmdb_connect()
    df = pd.read_sql(text(query), conn)
    cmdb_disconnect(conn)
    return df

def update_data(table, uuid, data):
    df_dv = get_display_value(table)
    query = 'UPDATE ' + str(table) + ' SET '
    for key in data.keys():
        if key != 'update' and data[key] != 'update':
            data_type = df_dv[df_dv['sys_table_column'] == key]['data_type'].iloc[0]
            #query += str(data_type) + ' '
            if data_type == 'character varying' or data_type == 'date' or data_type == 'dictionary' or data_type == 'reference':
                query += str(key) + ' = \'' + str(data[key]).replace("'", "''") + '\', '
            else:
                if data_type != 'function':
                    query += str(key) + ' = ' + str(data[key]) + ', '
    query = query[:-2]
    query += ' WHERE uuid = \'' + str(uuid) + '\';'
    conn = cmdb_connect()
    conn.execute(text(query))
    conn.commit()
    cmdb_disconnect(conn)
    return query

def get_table_display_value(table):
    table_display_value = ''
    query = """
SELECT
  display_value
FROM _sys_display_value
WHERE sys_table = '""" + str(table) + """'
  AND sys_table_column = ''
;
    """
    conn = cmdb_connect()
    df = pd.read_sql(text(query), conn)
    rows = conn.execute(text(query))
    for row in rows:
        table_display_value = row[0]
    cmdb_disconnect(conn)
    return table_display_value

def get_backwards_reference(table):
    query = """
SELECT source
FROM _sys_reference
WHERE target = '""" + str(table) + """';
    """
    conn = cmdb_connect()
    df = pd.read_sql(text(query), conn)
    cmdb_disconnect(conn)
    return df

def get_backwards_reference_data(table, source, uuid):
    query = """
SELECT *
FROM """ + str(source) + """
WHERE """ + str(table) + """ = '""" + str(uuid) + """'
    """
    conn = cmdb_connect()
    df_br = pd.read_sql(text(query), conn)
    cmdb_disconnect(conn)
    return df_br

