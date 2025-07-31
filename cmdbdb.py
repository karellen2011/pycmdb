from sqlalchemy import create_engine, text
import pandas as pd

################################################################################
#
# DATABASE CONNECTION
#
################################################################################

def cmdb_connect():
    database = 'cmdb3'
    username = 'cmdb'
    password = 'cmdb'
    host = '127.0.0.1'
    port = 5432
    cmdb_engine = 'postgresql://' + username + ':' + password + '@' + host + '/' + database
    conn = None
    sqlEngine = create_engine(cmdb_engine)
    conn = sqlEngine.connect()
    return conn

def cmdb_disconnect(conn):
    conn.close()

################################################################################
#
# DISPLAY VALUE
#
################################################################################

def get_display_value_include(table):
    query = """
WITH cte_dictionary AS (
  SELECT DISTINCT sys_table_column
  FROM _sys_dictionary
  WHERE sys_table = '""" + str(table) + """'
), cte_reference AS (
  SELECT DISTINCT target
  FROM _sys_reference
  WHERE source = '""" + str(table) + """'
), cte_function AS (
  SELECT DISTINCT function_name AS function_name
  FROM _sys_function
  WHERE sys_table = '""" + str(table) + """'
)
SELECT
  _sys_display_value.sys_table AS sys_table,
  _sys_display_value.sys_table_column AS sys_table_column,
  _sys_display_value.display_value AS display_value,
  _sys_display_value.sys_order AS sys_order,
  information_schema.columns.data_type AS data_type,
  information_schema.columns.column_default AS column_default,
  _sys_display_value.include AS include,
  CASE
    WHEN cte_dictionary.sys_table_column IS NOT NULL THEN True
    ELSE False
  END AS dictionary,
  CASE
    WHEN cte_reference.target IS NOT NULL THEN True
    ELSE False
  END AS reference,
  CASE
    WHEN cte_function.function_name IS NOT NULL THEN True
    ELSE False
  END AS function
FROM _sys_display_value
JOIN information_schema.columns ON sys_table_column = information_schema.columns.column_name
LEFT JOIN cte_dictionary ON _sys_display_value.sys_table_column = cte_dictionary.sys_table_column
LEFT JOIN cte_reference ON _sys_display_value.sys_table_column = cte_reference.target
LEFT JOIN cte_function ON _sys_display_value.sys_table_column = cte_function.function_name
WHERE _sys_display_value.sys_table = '""" + str(table) + """'
  AND _sys_display_value.sys_table_column <> ''
  AND information_schema.columns.table_name = _sys_display_value.sys_table
  AND _sys_display_value.include = true
ORDER BY sys_order, display_value
;
    """
    conn = cmdb_connect()
    df = pd.read_sql(text(query), conn)
    cmdb_disconnect(conn)
    return df

def get_display_value(table):
    query = """
WITH cte_dictionary AS (
  SELECT DISTINCT sys_table_column
  FROM _sys_dictionary
  WHERE sys_table = '""" + str(table) + """'
), cte_reference AS (
  SELECT DISTINCT target
  FROM _sys_reference
  WHERE source = '""" + str(table) + """'
), cte_function AS (
  SELECT DISTINCT function_name AS function_name
  FROM _sys_function
  WHERE sys_table = '""" + str(table) + """'
)
SELECT
  _sys_display_value.sys_table AS sys_table,
  _sys_display_value.sys_table_column AS sys_table_column,
  _sys_display_value.display_value AS display_value,
  _sys_display_value.sys_order AS sys_order,
  information_schema.columns.data_type AS data_type,
  information_schema.columns.column_default AS column_default,
  _sys_display_value.include AS include,
  CASE
    WHEN cte_dictionary.sys_table_column IS NOT NULL THEN True
    ELSE False
  END AS dictionary,
  CASE
    WHEN cte_reference.target IS NOT NULL THEN True
    ELSE False
  END AS reference,
  CASE
    WHEN cte_function.function_name IS NOT NULL THEN True
    ELSE False
  END AS function
FROM _sys_display_value
JOIN information_schema.columns ON sys_table_column = information_schema.columns.column_name
LEFT JOIN cte_dictionary ON _sys_display_value.sys_table_column = cte_dictionary.sys_table_column
LEFT JOIN cte_reference ON _sys_display_value.sys_table_column = cte_reference.target
LEFT JOIN cte_function ON _sys_display_value.sys_table_column = cte_function.function_name
WHERE _sys_display_value.sys_table = '""" + str(table) + """'
  AND _sys_display_value.sys_table_column <> ''
  AND information_schema.columns.table_name = _sys_display_value.sys_table
ORDER BY sys_order, display_value
;
    """
    conn = cmdb_connect()
    df = pd.read_sql(text(query), conn)
    cmdb_disconnect(conn)
    # Update include, a table should never include itself
    df['include'] = False
    #for include_column in list(df[df['reference'] == True]['sys_table_column']):
    #    df_tmp = get_display_value_include(include_column)
    #    if df_tmp.shape[0] > 0:
    #        df = pd.concat([df, df_tmp])
    for include_column in list(df[df['reference'] == True]['sys_table_column']):
        df_tmp = get_display_value_include(include_column)
        if df_tmp.shape[0] > 0:
            ind = df[df['sys_table_column'] == include_column].index.values.astype(int)[0] + 1
            df_start = df.iloc[:ind]
            df_end = df.iloc[ind:]
            df = pd.concat([df_start, df_tmp, df_end])
    return df

################################################################################
#
# DICTIONARY, REFERENCE AND FUNCTION
#
################################################################################

def get_dictionary(table):
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

def get_reference(table):
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

def get_referenced_values(table):
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

################################################################################
#
# TABLE
#
################################################################################

def get_table(table):
    df_display_value = get_display_value(table)
    df_dictionary = get_dictionary(table)
    cte_query = ''
    query = 'SELECT\n'
    from_query = 'FROM ' + str(table) + '\n'
    select_query = ''
    reference_join = ''
    dictionary_join = ''
    for col in df_display_value.iterrows():
        if col[1]['include'] == False:
            if col[1]['dictionary'] == False and col[1]['reference'] == False and col[1]['function'] == False:
                select_query += col[1]['sys_table'] + '.' + col[1]['sys_table_column'] + ' AS ' + col[1]['sys_table_column'] + ', \n'
            if col[1]['dictionary'] == True and col[1]['reference'] == False and col[1]['function'] == False:
                if cte_query == '':
                    cte_query = 'WITH cte_dict_' + col[1]['sys_table'] + '_' + col[1]['sys_table_column'] + ' AS (\n'
                else:
                    cte_query += ', cte_dict_' + col[1]['sys_table'] + '_' + col[1]['sys_table_column'] + ' AS (\n'
                cte_query += 'SELECT uuid, dict_value, color\n'
                cte_query += 'FROM _sys_dictionary\n'
                cte_query += 'WHERE sys_table = \'' + col[1]['sys_table'] + '\' AND sys_table_column = \'' + col[1]['sys_table_column'] + '\'\n'
                cte_query += ')\n'
                select_query += 'cte_dict_' + col[1]['sys_table'] + '_' + col[1]['sys_table_column'] + '.dict_value AS ' + col[1]['sys_table_column'] + '_display_value, \n'
                select_query += 'cte_dict_' + col[1]['sys_table'] + '_' + col[1]['sys_table_column'] + '.color AS ' + col[1]['sys_table_column'] + '_display_color, \n'
                dictionary_join += 'JOIN cte_dict_' + col[1]['sys_table'] + '_' + col[1]['sys_table_column'] + ' ON ' + col[1]['sys_table'] + '.' + col[1]['sys_table_column'] + ' = cte_dict_' + col[1]['sys_table'] + '_' + col[1]['sys_table_column'] + '.uuid\n'
            if col[1]['dictionary'] == False and col[1]['reference'] == True and col[1]['function'] == False:
                select_query += col[1]['sys_table_column'] + '.uuid AS ' + col[1]['sys_table_column'] + '_uuid, \n'
                select_query += col[1]['sys_table_column'] + '.name AS ' + col[1]['sys_table_column'] + '_name, \n'
                df_inc = df_display_value[(df_display_value['sys_table'] == col[1]['sys_table_column']) &
                                          (df_display_value['include'] == True)]
                if df_inc.shape[0] > 0:
                    for col_inc in df_inc.iterrows():
                        select_query += col[1]['sys_table_column'] + '.' + col_inc[1]['sys_table_column'] + ' AS ' + col_inc[1]['sys_table_column'] + ', \n'
                reference_join += 'JOIN ' + col[1]['sys_table_column'] + ' ON ' + table + '.' + col[1]['sys_table_column'] + ' = ' + col[1]['sys_table_column'] + '.uuid\n'
            if col[1]['dictionary'] == False and col[1]['reference'] == False and col[1]['function'] == True:
                select_query += col[1]['sys_table'] + '.' + col[1]['sys_table_column'] + ' AS ' + col[1]['sys_table_column'] + ', \n'
        if col[1]['include'] == True:
            if col[1]['dictionary'] == True and col[1]['reference'] == False and col[1]['function'] == False:
                if cte_query == '':
                    cte_query = 'WITH cte_dict_' + col[1]['sys_table'] + '_' + col[1]['sys_table_column'] + ' AS (\n'
                else:
                    cte_query += ', cte_dict_' + col[1]['sys_table'] + '_' + col[1]['sys_table_column'] + ' AS (\n'
                cte_query += 'SELECT uuid, dict_value, color\n'
                cte_query += 'FROM _sys_dictionary\n'
                cte_query += 'WHERE sys_table = \'' + col[1]['sys_table'] + '\' AND sys_table_column = \'' + col[1]['sys_table_column'] + '\'\n'
                cte_query += ')\n'
                select_query += 'cte_dict_' + col[1]['sys_table'] + '_' + col[1]['sys_table_column'] + '.dict_value AS ' + col[1]['sys_table_column'] + '_display_value, \n'
                select_query += 'cte_dict_' + col[1]['sys_table'] + '_' + col[1]['sys_table_column'] + '.color AS ' + col[1]['sys_table_column'] + '_display_color, \n'
                dictionary_join += 'JOIN cte_dict_' + col[1]['sys_table'] + '_' + col[1]['sys_table_column'] + ' ON ' + col[1]['sys_table'] + '.' + col[1]['sys_table_column'] + ' = cte_dict_' + col[1]['sys_table'] + '_' + col[1]['sys_table_column'] + '.uuid\n'
    query = cte_query + query
    query += select_query[:-3] + '\n'
    query += from_query
    query += reference_join
    query += dictionary_join
    query += 'ORDER BY name'
    #print(query)
    conn = cmdb_connect()
    df = pd.read_sql(text(query), conn)
    cmdb_disconnect(conn)
    return df

################################################################################
#
# UPDATE TABLE
#
################################################################################

def update_table(table, insert_data):
    df_display_value = get_display_value(table)
    values = ''
    insert_query = 'INSERT INTO ' + str(table) + ' ('
    for key in insert_data.keys():
        if key != 'insert' and insert_data[key] != 'insert':
            insert_query += str(key) + ', '
            data_type = str(df_display_value[df_display_value['sys_table_column'] == key]['data_type'].iloc[0])
            #values += value_type + ', ' + str(insert_data[key]) + ', '
            if data_type == 'character varying' or data_type == 'date' or data_type == 'dictionary' or data_type == 'reference':
                values += "'" + str(insert_data[key]) + "', "
            else:
                values += str(insert_data[key]) + ', '
    insert_query = insert_query[:-2]
    insert_query += ') VALUES ('
    insert_query += values[:-2]
    insert_query += ');'
    conn = cmdb_connect()
    conn.execute(text(insert_query))
    conn.commit()
    cmdb_disconnect(conn)
    return insert_query

################################################################################
#
# OTHER STUFF...
#
################################################################################

def get_all_tables_columns():
    query = """
WITH cte_table_display_value AS (
  SELECT sys_table, display_value, sys_order
  FROM _sys_display_value
  WHERE sys_table_column = ''
), cte_column_display_value AS (
  SELECT sys_table, sys_table_column, display_value, sys_order
  FROM _sys_display_value
  WHERE sys_table_column != ''
)
SELECT
  pg_catalog.pg_tables.tablename AS table,
  cte_table_display_value.display_value AS table_display_value,
  cte_table_display_value.sys_order AS table_display_order,
  information_schema.columns.column_name AS column,
  cte_column_display_value.display_value AS column_display_value,
  cte_column_display_value.sys_order AS column_display_order,
  information_schema.columns.data_type AS data_type,
  information_schema.columns.character_maximum_length AS character_maximum_length,
  information_schema.columns.column_default AS column_default
FROM pg_catalog.pg_tables
JOIN information_schema.columns ON pg_catalog.pg_tables.tablename = information_schema.columns.table_name
JOIN cte_table_display_value ON pg_catalog.pg_tables.tablename = cte_table_display_value.sys_table
JOIN cte_column_display_value ON (pg_catalog.pg_tables.tablename = cte_column_display_value.sys_table AND information_schema.columns.column_name = cte_column_display_value.sys_table_column)
WHERE pg_catalog.pg_tables.tableowner = 'cmdb'
  AND pg_catalog.pg_tables.tablename NOT LIKE '_sys_%'
ORDER BY pg_catalog.pg_tables.tablename, information_schema.columns.ordinal_position
;
    """
    conn = cmdb_connect()
    df = pd.read_sql(text(query), conn)
    cmdb_disconnect(conn)
    return df



