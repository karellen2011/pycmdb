from sqlalchemy import create_engine, text
import pandas as pd

from cmdbhtml import html_header, html_footer
from cmdbdb import cmdb_connect, cmdb_disconnect

def adminlistcolumns2(im_dict):
    output = html_header()

    # JavaScript
    output += '<!-- https://www.w3schools.com/howto/howto_js_cascading_dropdown.asp -->\n'
    output += '<script>\n'
    output += 'var subjectObject = {\n'
    output += '"Front-end": {\n'
    output += '"HTML": ["Links", "Images", "Tables", "Lists"],\n'
    output += '"CSS": ["Borders", "Margins", "Backgrounds", "Float"],\n'
    output += '"JavaScript": ["Variables", "Operators", "Functions", "Conditions"]\n'
    output += '},\n'
    output += '"Back-end": {\n'
    output += '"PHP": ["Variables", "Strings", "Arrays"],\n'
    output += '"SQL": ["SELECT", "UPDATE", "DELETE"]\n'
    output += '}\n'
    output += '}\n'
    output += 'window.onload = function() {\n'
    output += 'var subjectSel = document.getElementById("subject");\n'
    output += 'var topicSel = document.getElementById("topic");\n'
    output += 'var chapterSel = document.getElementById("chapter");\n'
    output += 'for (var x in subjectObject) {\n'
    output += 'subjectSel.options[subjectSel.options.length] = new Option(x, x);\n'
    output += '}\n'
    output += 'subjectSel.onchange = function() {\n'
    output += '//empty Chapters- and Topics- dropdowns\n'
    output += 'chapterSel.length = 1;\n'
    output += 'topicSel.length = 1;\n'
    output += '//display correct values\n'
    output += 'for (var y in subjectObject[this.value]) {\n'
    output += 'topicSel.options[topicSel.options.length] = new Option(y, y);\n'
    output += '}\n'
    output += '}\n'
    output += 'topicSel.onchange = function() {\n'
    output += '//empty Chapters dropdown\n'
    output += 'chapterSel.length = 1;\n'
    output += '//display correct values\n'
    output += 'var z = subjectObject[subjectSel.value][this.value];\n'
    output += 'for (var i = 0; i < z.length; i++) {\n'
    output += 'chapterSel.options[chapterSel.options.length] = new Option(z[i], z[i]);\n'
    output += '}\n'
    output += '}\n'
    output += '}\n'
    output += '</script>\n'

    output += 'Cascade<br>\n'
    if im_dict != None:
        output += str(im_dict) + '<br>\n'

    # HTML
    output += '<form name="form1" id="form1" action="/cascade/" method="POST">\n'
    output += '<table id="default">\n'
    output += '<tr>'
    output += '<th>Table:<br>\n'
    output += '<select name="table" id="table">\n'
    output += '<option value="" selected="selected">Select table</option>\n'
    output += '</select>\n'
    output += '</th><th>\n'
    output += 'Column:<br>\n'
    output += '<select name="column" id="column">\n'
    output += '<option value="" selected="selected">Please select table first</option>\n'
    output += '</select>\n'
    output += '</th><th>\n'
    output += 'Report:<br>\n'
    output += '<select name="report" id="report">\n'
    output += '<option value="" selected="selected">Please select column first</option>\n'
    output += '</select>\n'
    output += '</th>\n'
    output += '</tr>\n'
    output += '</table>\n'
    #output += '<input type="submit" value="Submit">\n'
    output += '</form>\n'

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



