import importlib.util
import sys
#from sqlalchemy import create_engine, text
import pandas as pd

import cmdbhtml
import cmdbdb

def tablelist(table, row_start, number_rows, filter_col, filter_con, filter_val, insert_data):

    # INSERT DATA BEFORE DOING ANYTHING ELSE
    if len(insert_data.keys()) > 0 and 'insert' in insert_data.keys() and insert_data['insert'] == 'insert':
        cmdbdb.update_table(table, insert_data)

    df_display_value = cmdbdb.get_display_value(table)
    df_table = cmdbdb.get_table(table)

    # ASSEMBLE DICTIONARY DATAFRAME
    df_dictionary = None
    for sys_table in list(df_display_value['sys_table'].unique()):
        df_tmp = cmdbdb.get_dictionary(sys_table)
        df_dictionary = pd.concat([df_dictionary, df_tmp])

    # LOAD ADDITIONAL FUNCTIONS
    #fs = []
    function_list = list(df_display_value[df_display_value['function'] == True]['sys_table_column'])
    for function_name in function_list:
        function_file = 'function/' + function_name + '/function.py'
        #function = importlib.import_module(function_name, package=None)
        spec = importlib.util.spec_from_file_location('once', function_file)
        function = importlib.util.module_from_spec(spec)
        sys.modules['once'] = function
        spec.loader.exec_module(function)
        #fs.append(function_file)
        #fs.append(function.functioncall())
    #fs.append(function.functioncall())

    output = cmdbhtml.html_header()

    #output += str(filter_col) + '<br>\n'
    #output += str(filter_con) + '<br>\n'
    #output += str(filter_val) + '<br>\n'
    
    #output += str(insert_data) + '<br>\n'

    #
    # ASSEMBLE TABLE HEADER START
    #
    #output += str(df_table.columns) + '<br>\n'
    output += '<form action="/table/list/' + str(table) + '" method="GET">\n'
    output += '<table id="default">\n'
    output += '<tr>\n'
    for col in df_display_value.iterrows():
        column = col[1]['sys_table_column']
        if column != 'uuid':
            column_table = col[1]['sys_table']
            column_dv = col[1]['display_value']
            column_data_type = col[1]['data_type']
            column_include = col[1]['include']
            internal_data_type = ''
            if col[1]['dictionary'] == False and col[1]['reference'] == False and col[1]['function'] == False:
                internal_data_type = 'direct'
            elif col[1]['dictionary'] == True and col[1]['reference'] == False and col[1]['function'] == False:
                internal_data_type = 'dictionary'
            elif col[1]['dictionary'] == False and col[1]['reference'] == True and col[1]['function'] == False:
                internal_data_type = 'reference'
            elif col[1]['dictionary'] == False and col[1]['reference'] == False and col[1]['function'] == True:
                internal_data_type = 'function'
            else:
                internal_data_type = 'unknown'

            output += '<th valign="top">'
            output += str(column_dv)
            #output += '<br>' + str(column)
            #output += '<br>' + str(column_data_type)
            #output += '<br>' + str(internal_data_type)
            #output += '<br>' + str(column_include)

            #
            # ASSEMBLE FILTER LIST
            #
            filter_list = []
            filter_value = ''
            filter_condition = ''
            if column in filter_col:
                filter_col_index = filter_col.index(column)
                filter_value = filter_val[filter_col_index]
                filter_condition = filter_con[filter_col_index]
                #if filter_value != '':
                #    output += str(filter_value) + '</br>\n'
            if internal_data_type == 'direct' and column != table:
                filter_list = list(df_table.sort_values(by=[column])[column].unique())
            if internal_data_type == 'dictionary': # and column_include == False:
                filter_list = list(df_dictionary[df_dictionary['sys_table_column'] == column]['dict_value'].unique())
            #if internal_data_type == 'dictionary' and column_include == True:
            #    filter_list = list(df_table[column + '_display_value'].unique())
            if internal_data_type == 'reference':
                #filter_list = list(df_table[column + '_name'].unique())
                filter_list = list(df_table.sort_values(by=[column + '_name'])[column + '_name'].unique())
            # Remove all empty entries and -- None -- entry, the re-add them in RIGHT order
            if '' in filter_list:
                filter_list.remove('')
            if '-- None --' in filter_list:
                filter_list.remove('-- None --')
                filter_list.insert(0, '-- None --')
            filter_list.insert(0, '')
            if len(filter_list) > 1:
                output += '<br>'
                output += '<select name="' + str(column) + '::condition">\n'
                for filter_condition_value in ['', '==', '!=']:
                    if filter_condition_value == filter_condition:
                        output += '<option value="' + str(filter_condition_value) + '" selected>' + str(filter_condition_value) + '</option>\n'
                    else:
                        output += '<option value="' + str(filter_condition_value) + '">' + str(filter_condition_value) + '</option>\n'
                output += '</select>\n<br>\n'
                output += '<select name="' + str(column) + '" onchange="this.form.submit()">\n'
                if column_data_type == 'date':
                    for item in filter_list:
                        if str(item) == filter_value:
                            output += '<option value="' + str(item) + '" selected>' + str(item)[:11] + '</option>\n'
                        else:
                            output += '<option value="' + str(item) + '">' + str(item)[:11] + '</option>\n'
                else:
                    for item in filter_list:
                        if str(item) == filter_value:
                            output += '<option value="' + str(item) + '" selected>' + str(item) + '</option>\n'
                        else:
                            output += '<option value="' + str(item) + '">' + str(item) + '</option>\n'
                output += '</select>\n'
            output += '</th>'

    output += '</tr>\n'
    output += '</form>\n'
    #
    # ASSEMBLE TABLE HEADER END
    #

    #
    # ASSEMBLE INPUT COLUMN START
    #
    output += '<form action="/table/list/' + str(table) + '" method="POST">\n'
    output += '<tr>\n'
    for col in df_display_value.iterrows():
        column = col[1]['sys_table_column']
        if column != 'uuid':
            column_table = col[1]['sys_table']
            column_dv = col[1]['display_value']
            column_data_type = col[1]['data_type']
            column_include = col[1]['include']
            column_default_value = col[1]['column_default']
            internal_data_type = ''
            if col[1]['dictionary'] == False and col[1]['reference'] == False and col[1]['function'] == False:
                internal_data_type = 'direct'
            elif col[1]['dictionary'] == True and col[1]['reference'] == False and col[1]['function'] == False:
                internal_data_type = 'dictionary'
            elif col[1]['dictionary'] == False and col[1]['reference'] == True and col[1]['function'] == False:
                internal_data_type = 'reference'
            elif col[1]['dictionary'] == False and col[1]['reference'] == False and col[1]['function'] == True:
                internal_data_type = 'function'
            else:
                internal_data_type = 'unknown'
            output += '<td valign="top">'
            #output += str(column_dv)
            #output += '<br>' + str(column)
            #output += '<br>' + str(column_default_value)
            #output += '<br>' + str(column_table)
            #output += '<br>' + str(column_data_type)
            #output += '<br>' + str(column_include)
            #output += '<br>' + str(internal_data_type)
            #output += '<br>'
            #output += '<br>'
            if column_include == False:
                if internal_data_type == 'direct':
                    if column_data_type == 'character varying':
                        if column_default_value == None:
                            column_default_value = ''
                        else:
                            column_default_value = column_default_value[1:-20]
                        output += '<input type="text" name="' + str(column) + '" value="' + column_default_value + '">\n'
                    if column_data_type == 'boolean':
                        output += '<select name="' + str(column) + '">\n'
                        if column_default_value == str('true'):
                            output += '<option value="true" selected>True</option>\n'
                            output += '<option value="false">False</option>\n'
                        else:
                            output += '<option value="true">True</option>\n'
                            output += '<option value="false" selected>False</option>\n'
                        output += '</select>\n'
                    if column_data_type == 'numeric':
                        output += '<input type="text" name="' + str(column) + '" value="' + column_default_value + '">\n'
                    if column_data_type == 'date':
                        column_default_value = column_default_value[1:-7]
                        output += '<input type="text" name="' + str(column) + '" value="' + column_default_value + '">\n'
                    if column_data_type == 'integer':
                        output += '<input type="text" name="' + str(column) + '" value="' + str(column_default_value) + '">\n'
                if internal_data_type == 'dictionary':
                    column_default_value = column_default_value[1:-20]
                    output += '<select name="' + str(column) + '">\n'
                    df_tmp_dict = df_dictionary[df_dictionary['sys_table_column'] == column][['uuid', 'dict_value']]
                    for dict_entry in df_tmp_dict.iterrows():
                        if column_default_value == dict_entry[1]['uuid']:
                            output += '<option value="' + dict_entry[1]['uuid'] + '" selected>' + dict_entry[1]['dict_value'] + '</option>\n'
                        else:
                            output += '<option value="' + dict_entry[1]['uuid'] + '">' + dict_entry[1]['dict_value'] + '</option>\n'
                    output += '</select>\n'
                if internal_data_type == 'reference':
                    df_reference = cmdbdb.get_referenced_values(column)
                    column_default_value = column_default_value[1:-20]
                    output += '<select name="' + str(column) + '">\n'
                    for ref_entry in df_reference.iterrows():
                        if column_default_value == ref_entry[1]['uuid']:
                            output += '<option value="' + ref_entry[1]['uuid'] + '" selected>' + ref_entry[1]['name'] + '</option>\n'
                        else:
                            output += '<option value="' + ref_entry[1]['uuid'] + '">' + ref_entry[1]['name'] + '</option>\n'
                    output += '</select>\n'



            output += '</td>'
    output += '<td><button type="submit" name="insert" value="insert"><img src="/static/create.png" alt="Insert" width="20"></button></td>\n'
    output += '</tr>\n'
    output += '</form>\n'
    #
    # ASSEMBLE INPUT COLUMN END
    #

    #
    # APPLY FILTER
    #
    for cc, fc in enumerate(filter_col):
        new_fc = ''
        fv = filter_val[cc]
        filter_condition = filter_con[cc]
        if fv != '':
            filter_include = df_display_value[df_display_value['sys_table_column'] == fc]['include'].iloc[0]
            filter_dictionary = df_display_value[df_display_value['sys_table_column'] == fc]['dictionary'].iloc[0]
            filter_reference = df_display_value[df_display_value['sys_table_column'] == fc]['reference'].iloc[0]
            filter_function = df_display_value[df_display_value['sys_table_column'] == fc]['function'].iloc[0]
            #output += '<tr><th>' + str(filter_include) + '</th><th>' + str(filter_dictionary) + '</th><th>' + str(filter_reference) + '</th><th>' + str(filter_function) + '</th></tr>\n'
            # DIRECT FILTER
            if filter_include == False and filter_dictionary == False and filter_reference == False and filter_function == False:
                new_fc = fc
                data_type = df_display_value[df_display_value['sys_table_column'] == new_fc]['data_type'].iloc[0]
                #output += '<tr><th>general ' + data_type + ' ' + new_fc + ' ' + fv + '</th></tr>\n'
                if data_type == 'boolean':
                    if fv == 'True':
                        #output += '<tr><th>direct ' + data_type + ' ' + new_fc + ' ' + fv + '</th></tr>\n'
                        #df_table = df_table[df_table[new_fc] == True].copy()
                        if filter_condition == '==':
                            df_table = df_table[df_table[new_fc] == True].copy()
                        elif filter_condition == '!=':
                            df_table = df_table[df_table[new_fc] != True].copy()
                    elif fv == 'False':
                        #df_table = df_table[df_table[new_fc] == False].copy()
                        if filter_condition == '==':
                            df_table = df_table[df_table[new_fc] == False].copy()
                        elif filter_condition == '!=':
                            df_table = df_table[df_table[new_fc] != False].copy()
                elif data_type == 'integer':
                    #df_table = df_table[df_table[new_fc] == int(fv)].copy()
                    if filter_condition == '==':
                        df_table = df_table[df_table[new_fc] == int(fv)].copy()
                    elif filter_condition == '!=':
                        df_table = df_table[df_table[new_fc] != int(fv)].copy()
                elif data_type == 'numeric':
                    #df_table = df_table[df_table[new_fc] == float(fv)].copy()
                    if filter_condition == '==':
                        df_table = df_table[df_table[new_fc] == float(fv)].copy()
                    elif filter_condition == '!=':
                        df_table = df_table[df_table[new_fc] != float(fv)].copy()
                else:
                   #output += '<tr><th>direct ' + data_type + ' ' + new_fc + ' ' + fv + '</th></tr>\n'
                   #df_table = df_table[df_table[new_fc] == fv].copy()
                    if filter_condition == '==':
                        df_table = df_table[df_table[new_fc] == fv].copy()
                    elif filter_condition == '!=':
                        df_table = df_table[df_table[new_fc] != fv].copy()
            # DICTIONARY FILTER
            if filter_dictionary == True and filter_reference == False and filter_function == False:
                new_fc = fc + '_display_value'
                #output += '<tr><th>dict ' + new_fc + ' ' + fv + '</th></tr>\n'
                if filter_condition == '==':
                    df_table = df_table[df_table[new_fc] == fv].copy()
                elif filter_condition == '!=':
                    df_table = df_table[df_table[new_fc] != fv].copy()
            # REFERENCE FILTER
            if  filter_include == False and filter_dictionary == False and filter_reference == True and filter_function == False:
                new_fc = fc + '_name'
                #output += '<tr><th>refe ' + new_fc + ' ' + fv + '</th></tr>\n'
                if filter_condition == '==':
                    df_table = df_table[df_table[new_fc] == fv].copy()
                elif filter_condition == '!=':
                    df_table = df_table[df_table[new_fc] != fv].copy()
            # INCLUDED REFERENCE FILTER
            # ERROR IN get_display_value, included reference appears as false
            if  filter_include == True and filter_dictionary == False and filter_reference == False and filter_function == False:
                new_fc = fc
                #output += '<tr><th>inc refe ' + new_fc + ' ' + fv + '</th></tr>\n'
                if filter_condition == '==':
                    df_table = df_table[df_table[new_fc] == fv].copy()
                elif filter_condition == '!=':
                    df_table = df_table[df_table[new_fc] != fv].copy()
    

    #
    # ASSEMBLE TABLE START
    #

    for row in df_table.iterrows():
        output += '<tr>'
        for col in df_display_value.iterrows():
            column = col[1]['sys_table_column']
            if column != 'uuid':
                column_table = col[1]['sys_table']
                column_dv = col[1]['display_value']
                column_data_type = col[1]['data_type']
                column_include = col[1]['include']
                internal_data_type = ''
                if col[1]['dictionary'] == False and col[1]['reference'] == False and col[1]['function'] == False:
                    internal_data_type = 'direct'
                elif col[1]['dictionary'] == True and col[1]['reference'] == False and col[1]['function'] == False:
                    internal_data_type = 'dictionary'
                elif col[1]['dictionary'] == False and col[1]['reference'] == True and col[1]['function'] == False:
                    internal_data_type = 'reference'
                elif col[1]['dictionary'] == False and col[1]['reference'] == False and col[1]['function'] == True:
                    internal_data_type = 'function'
                else:
                    internal_data_type = 'unknown'
                # OUTPUT DIRECT VALUE
                if internal_data_type == 'direct':
                    #output += '<td>'
                    if column == 'name':
                        output += '<td><a href="/view/' + str(table) + '/' + str(row[1]['uuid']) + '/">' + str(row[1][column]) + '</a></td>'
                    else:
                        if column_data_type == 'date':
                            output += '<td>' + str(row[1][column])[:11] + '</td>'
                        elif column_data_type == 'numeric':
                            scale = int(df_display_value[(df_display_value['sys_table'] == table) & (df_display_value['sys_table_column'] == column)]['scale'].iloc[0])
                            tmp_split = str(row[1][column])[:11].split('.')
                            add_scale = (scale - len(tmp_split[1])) * '0'
                            output += '<td align="right">' + str(row[1][column])[:11] + str(add_scale) + '</td>'
                        elif column_data_type == 'integer':
                            output += '<td align="right">' + str(row[1][column])[:11] + '</td>'
                        else:
                            output += '<td>' + str(row[1][column]) + '</td>'
                    #output += '</td>'
                # OUTPUT DICTIONARY
                if internal_data_type == 'dictionary':
                    if str(row[1][column + '_display_color']) != '':
                        output += '<td style="background:#' + str(row[1][column + '_display_color']) + '">' + str(row[1][column + '_display_value']) + '</td>'
                    else:
                        output += '<td>' + str(row[1][column + '_display_value']) + '</td>'
                # OUTPUT REFERENCE
                if internal_data_type == 'reference':
                    output += '<td>'
                    output += '<a href="/view/' + str(column) + '/' + str(row[1][column + '_uuid']) + '/">' + str(row[1][column + '_name']) + '</a>'
                    output += '</td>'
                # OUTPUT FUNCTION
                if internal_data_type == 'function':
                    output += '<td>'
                    #output += 'functioncall()'
                    output += str(function.functioncall(row[1]['uuid']))
                    output += '</td>'
        output += '</tr>\n'

    #
    # ASSEMBLE TABLE END
    #
    output += '</table>\n'

    # ASSEMBLE OUTPUT
    output += cmdbhtml.html_footer()

    return output

