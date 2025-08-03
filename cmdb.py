from flask import Flask, render_template, redirect, url_for, request
import pandas as pd

from cmdbhtml import html_header, html_footer
#from cmdbdb import list_tables, list_table
#from cmdbadmin import create_table, drop_table, list_table_column

from admintable import adminlisttables
from admincolumn import adminlistcolumns
from admincolumn2 import adminlistcolumns2
from admindictionary import adminlistdict
from adminfunction import adminlistfunctions
from adminreport import createreport
from tablelist import tablelist
from cmdbview import cmdbview

app = Flask(__name__)

#
# START
#

@app.route("/")
def hello_world():
    output = html_header()
    output += html_footer()
    return output

#
# CASCADE TEST
#

@app.route('/cascade/', methods = ['POST', 'GET'])
def cascade():
    im_dict = None
    if request.method == 'POST':
        im_dict = request.form

    output = adminlistcolumns2(im_dict)

    return output

################################################################################
#
# ADMIN TABLE
#
################################################################################

@app.route('/admin/table/', methods = ['POST', 'GET'])
def admintable():

    im_dict = None
    create_table_name = ''
    display_value = ''
    drop_table_name = ''
    update_table_name = ''
    display_order = ''
    uuid = ''

    debug_str = ''

    if request.method == 'POST':
        im_dict = request.form
        if 'create_table' in im_dict.keys():
            create_table_name = str(im_dict['create_table']).lower()
            display_value = str(im_dict['display_value'])
            display_order = str(im_dict['display_order'])
        if 'drop_table' in im_dict.keys():
            drop_table_name = str(im_dict['drop_table']).lower()
        if 'update_table' in im_dict.keys():
            update_table_name = str(im_dict['update_table']).lower()
            display_value = str(im_dict[update_table_name + '::update_display_value'])
            display_order = str(im_dict[update_table_name + '::update_display_order'])
            #uuid = str(im_dict['uuid'])
            #debug_str = 'Update Display Value: table: ' + str(update_table_name) + ' DV: ' + str(display_value) + '<br>\n'

    output = adminlisttables(create_table_name, display_value, drop_table_name, update_table_name, display_order)
    #output += str(update_table_name) + '<br>\n'
    #output += str(display_value) + '<br>\n'
    #output += str(im_dict) + '<br>\n'
    return output

################################################################################
#
# ADMIN COLUMN
#
################################################################################

@app.route("/admin/column/", methods = ['POST', 'GET'])
def admincolumn():

    im_dict = None
    table = '-- None --'
    column = ''
    display_value = ''
    display_order = ''
    data_type = '-- None --'
    length = ''
    column_default = ''
    update_data = {}
    if request.method == 'POST':
        im_dict = request.form
        if 'table' in im_dict.keys():
            table = str(im_dict['table']).lower()
        if 'create_column' in im_dict.keys():
            table = str(im_dict['table']).lower()
            column = str(im_dict['column']).lower()
            display_value = str(im_dict['display_value'])
            display_order = str(im_dict['display_order'])
            data_type = str(im_dict['data_type']).lower()
            length = str(im_dict['length']).lower()
            column_default = str(im_dict['column_default']).lower()
        if 'delete_column' in im_dict.keys():
            table = im_dict['delete_column'].split('::')[0]
            column = im_dict['delete_column'].split('::')[1]
        if 'update_column' in im_dict.keys():
            for key in im_dict.keys():
                update_data[key] = im_dict[key]

    output = adminlistcolumns(table, column, display_value, display_order, data_type, length, column_default, update_data)
    return output

################################################################################
#
# ADMIN DICTIONARY
#
################################################################################

@app.route("/admin/dict/", methods = ['POST', 'GET'])
def admindict():
    im_dict = None
    table = ''
    column = ''
    dict_value = ''
    dict_color = ''
    display_order = ''
    action = ''
    uuid = ''
    if request.method == 'POST':
        im_dict = request.form
        if 'create_dict' in im_dict.keys():
            action = 'create'
            dict_value = str(im_dict['dict_value'])
            dict_color = str(im_dict['dict_color'])
            display_order = str(im_dict['display_order']).lower()
        if 'update_dict' in im_dict.keys():
            action = 'update'
            uuid = str(im_dict['update_dict'])
            if uuid + '::dict_value' in im_dict.keys():
                dict_value = im_dict[uuid + '::dict_value']
            else:
                dict_value = '-- None --'
            dict_color = im_dict[uuid + '::dict_color']
            display_order = im_dict[uuid + '::display_order']
        if 'table' in im_dict.keys():
            table = str(im_dict['table']).lower()
        if 'column' in im_dict.keys():
            column = str(im_dict['column']).lower()
    output = adminlistdict(table, column, dict_value, dict_color, display_order, action, uuid)
    #output += str(action) + ' ' + str(uuid) + '<br>\n'
    #output += str(table) + ' :: ' + str(column) + ' :: ' + str(dict_value) + ' :: ' + str(dict_color) + ' :: ' + str(display_order) + ' :: ' + '<br>\n'
    return output

################################################################################
#
# ADMIN FUNCTION
#
################################################################################

@app.route("/admin/function/", methods = ['POST', 'GET'])
def adminfunction():
    output = adminlistfunctions()
    return output

################################################################################
#
# ADMIN REPORT
#
################################################################################

@app.route("/admin/report/", methods = ['POST', 'GET'])
def adminreport():
    table = ''
    column = ''
    charttype = ''
    palette = 'colorblind'
    cmap = 'Wistia'
    if request.method == 'POST':
        im_dict = request.form
        if 'table' in im_dict.keys():
            table = str(im_dict['table'])
        if 'column' in im_dict.keys():
            column = str(im_dict['column'])
        if 'charttype' in im_dict.keys():
            charttype = str(im_dict['charttype'])
        if 'palette' in im_dict.keys():
            palette = str(im_dict['palette'])
        if 'cmap' in im_dict.keys():
            cmap = str(im_dict['cmap'])
    output = createreport(table, column, charttype, palette, cmap)
    return output

################################################################################
#
# LIST TABLE2
#
################################################################################

@app.route("/table/list/<string:table_name>/", methods = ['POST', 'GET'])
def table_list_new(table_name):
    row_start = 0
    number_rows = 50
    filter_col = []
    filter_con = []
    filter_val = []
    insert_data = {}
    output = ''
    #output = tablelist(table_name, row_start, number_rows, filter_col, filter_val, insert_data)
    if request.method == 'GET':
        for i in request.args:
            if str(i) != 'row_start' and str(i) != 'number_rows':
                if str(i)[-11:] == '::condition':
                    filter_con.append(request.args[i])
                else:
                    filter_col.append(str(i))
                    filter_val.append(request.args[i])
            elif str(i) == 'row_start':
                row_start = request.args[i]
            elif str(i) == 'number_rows':
                number_rows = request.args[i]
    if request.method == 'POST':
        im_dict = request.form
        if 'insert' in im_dict.keys():
            for key in im_dict.keys():
                insert_data[key] = im_dict[key]
    for cc, ff in enumerate(filter_col):
        if filter_con[cc] == '' and filter_val[cc] != '':
            filter_con[cc] = '=='
        if filter_con[cc] != '' and filter_val[cc] == '':
            filter_con[cc] = ''
    #output += str(filter_col) + '<br>\n'
    #output += str(filter_con) + '<br>\n'
    #output += str(filter_val) + '<br>\n'
    output += tablelist(table_name, row_start, number_rows, filter_col, filter_con, filter_val, insert_data)
    return output


@app.route("/table333/list/<string:table_name>/", methods = ['POST', 'GET'])
def table_list(table_name):

    row_start = 0
    number_rows = 50
    filter_col = []
    filter_val = []
    insert_data = {}
    if request.method == 'GET':
        for i in request.args:
            if str(i) != 'row_start' and str(i) != 'number_rows':
                filter_col.append(str(i))
                #filter_val.append(str(request.args[i]))
                filter_val.append(request.args[i])
            elif str(i) == 'row_start':
                row_start = request.args[i]
            elif str(i) == 'number_rows':
                number_rows = request.args[i]
    if request.method == 'POST':
        im_dict = request.form
        if 'insert' in im_dict.keys():
            for key in im_dict.keys():
                insert_data[key] = im_dict[key]
    
    output = tablelist(table_name, row_start, number_rows, filter_col, filter_val, insert_data)
    #output = ''
    #output += str(filter_col) + '<br>\n'
    #output += str(filter_val) + '<br>\n'
    #output += str(insert_data) + '<br>\n'
    return output

################################################################################
#
# VIEW
#
################################################################################

@app.route("/view/<string:table_name>/<string:uuid>/", methods = ['POST', 'GET'])
def view(table_name, uuid):
    data = {}
    if request.method == 'POST':
        im_dict = request.form
        for key in im_dict.keys():
            data[key] = im_dict[key]
    output = cmdbview(table_name, uuid, data)
    #output += str(data) + '<br>\n'
    return output







