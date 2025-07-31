from sqlalchemy import create_engine, text
import pandas as pd

from cmdbdb import cmdb_connect, cmdb_disconnect

def html_header():
    df = list_tables()
    output = '<!doctype html>\n'
    output += '<html lang="en">\n'
    output += '<head>\n'
    output += '<title>CMDB</title>\n'
    output += '<link rel="stylesheet" href="/static/styles.css">\n'
    output += '<script src="/static/script.js"></script>\n'
    output += '</head>\n'
    output += '<body>\n'
    output += '<div class="menu">\n'
    output += '<table id="default">\n'
    output += '<tr><th>CMDB</th></tr>\n'
    for i in df.iterrows():
        output += '<tr><td><a href="/table/list/' + str(i[1]['tablename']) + '/">' + str(i[1]['display_value']) + '</a></td></tr>\n'
    output += '<tr><th>Admin</th></tr>\n'
    output += '<tr><td><a href="/admin/table/">Table</a></td></tr>\n'
    output += '<tr><td><a href="/admin/column/">Column</a></td></tr>\n'
    output += '<tr><td><a href="/admin/dict/">Dictionary</a></td></tr>\n'
    output += '<tr><td><a href="/admin/function/">Function</a></td></tr>\n'
    output += '<tr><td><a href="/admin/report/">Report</a></td></tr>\n'
    output += '</table>\n'
    output += '</div>\n'
    output += '<div class="content">\n'
    return output

def html_footer():
    output = '</div>\n'
    output += '</body>\n'
    output += '</html>\n'
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




