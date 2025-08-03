from sqlalchemy import create_engine, text
import pandas as pd

from cmdbhtml import html_header, html_footer
from cmdbdb import cmdb_connect, cmdb_disconnect

def adminlistcolumns2(im_dict):
    output = html_header()

    df_table = list_tables()

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
    output += 'var subjectSel = document.getElementById("table");\n'
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


def list_tables():
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
    return df



