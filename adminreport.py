from sqlalchemy import create_engine, text
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from cmdbhtml import html_header, html_footer
from cmdbdb import get_all_tables_columns, get_display_value, get_table

# JUST SOME SEABORN DEFAULT SETTINGS
plt.rcParams['figure.figsize'] = [16.0, 8.0]
plt.rcParams['figure.autolayout'] = True
sns.set_style('darkgrid')
#sns.set_palette('colorblind')
title_fontsize = 20
label_fontsize = 15

def createreport(table, column, charttype, palette, cmap):
    df_table_column = get_all_tables_columns()

    table_list = list(df_table_column.sort_values(by=['table_display_order'])['table_display_value'].unique())
    if '' in table_list:
        table_list.remove('')
    table_list.insert(0, '')

    column_list = []
    if table != '':
        table_name = df_table_column[(df_table_column['table_display_value'] == table)]['table'].iloc[0] # Ugly !!!

        df_display_value = get_display_value(table_name)
        #column_list = list(df_table_column[df_table_column['table_display_value'] == table].sort_values(by=['column_display_order'])['column_display_value'].unique())
        column_list = list(df_display_value['display_value'])
    if '' in column_list:
        column_list.remove('')
    if 'UUID' in column_list:
        column_list.remove('UUID')
    column_list.insert(0, '')

    chart_list = ['', 'Barplot', 'Countplot', 'Heatmap', 'Histplot']
    sns_palettes = ['hls', 'husl', 'Set2', 'Paired', 'deep', 'muted', 'pastel', 'bright', 'dark', 'colorblind']
    sns_cmaps = ['YlGnBu', 'Blues', 'coolwarm', 'BuPu', 'Greens', 'Oranges', 'Reds', 'Purples', 'YlOrBr', 'Wistia']
    
    #
    # Table, Column, Chart selection
    #
    output = html_header()
    #output += '<p id="debug">\n'
    #output += str(table_list) + '<br>\n'
    #output += str(column_list) + '<br>\n'
    #output += str(table) + '<br>\n'
    #output += str(column) + '<br>\n'
    #output += str(charttype) + '<br>\n'
    #output += '</p>\n'
    output += '<form name="report" id="report" action="/admin/report/" method="POST">\n'
    output += '<table id="default">\n'
    output += '<tr>\n'
    output += '<th valign="top">Table<br>\n'
    if len(table_list) > 1:
        output += '<select name="table" onchange="this.form.submit()">\n'
        for tl in table_list:
            if table == tl:
                output += '<option value="' + str(tl) + '" selected>' + str(tl) + '</option>\n'
            else:
                output += '<option value="' + str(tl) + '">' + str(tl) + '</option>\n'
        output += '</select>\n'
    output += '</th>\n'
    output += '<th valign="top">Column<br>\n'
    if table != '' and len(column_list) > 1:
        output += '<select name="column" onchange="this.form.submit()">\n'
        for cl in column_list:
            if column == cl:
                output += '<option value="' + str(cl) + '" selected>' + str(cl) + '</option>\n'
            else:
                output += '<option value="' + str(cl) + '">' + str(cl) + '</option>\n'
        output += '</select>\n'
    output += '</th>\n'
    output += '<th valign="top">Chart<br>\n'
    if table != '' and column != '':
        output += '<select name="charttype" onchange="this.form.submit()">\n'
        for cl in chart_list:
            if charttype == cl:
                output += '<option value="' + str(cl) + '" selected>' + str(cl) + '</option>\n'
            else:
                output += '<option value="' + str(cl) + '">' + str(cl) + '</option>\n'
        output += '</select>\n'
        if charttype == 'Barplot' or charttype == 'Countplot':
            output += '<select name="palette" onchange="this.form.submit()">\n'
            for pal in sns_palettes:
                if palette == pal:
                    output += '<option value="' + str(pal) + '" selected>' + str(pal) + '</option>\n'
                else:
                    output += '<option value="' + str(pal) + '">' + str(pal) + '</option>\n'
            output += '</select>\n'
        if charttype == 'Heatmap':
            output += '<select name="cmap" onchange="this.form.submit()">\n'
            for cm in sns_cmaps:
                if cmap == cm:
                    output += '<option value="' + str(cm) + '" selected>' + str(cm) + '</option>\n'
                else:
                    output += '<option value="' + str(cm) + '">' + str(cm) + '</option>\n'
            output += '</select>\n'
    output += '</th>\n'
    output += '</tr>\n'
    output += '</table>\n'
    output += '</form>\n'

    #
    # Get Data
    #
    if table != '' and column != '' and charttype != '':
        new_table = df_table_column[df_table_column['table_display_value'] == table]['table'].iloc[0]
        #new_column = df_table_column[(df_table_column['table_display_value'] == table) & (df_table_column['column_display_value'] == column)]['column'].iloc[0]
        new_column = df_display_value[df_display_value['display_value'] == column]['sys_table_column'].iloc[0]

        #output += new_table + '<br>\n'
        #output += new_column + '<br>\n'

        df_display_value = get_display_value(new_table)
        df_table = get_table(new_table)

        #output += str(list(df_display_value.columns)) + '<br>\n'
        #output += str(list(df_table.columns)) + '<br>\n'

        chart_include = df_display_value[df_display_value['sys_table_column'] == new_column]['include'].iloc[0]
        chart_dictionary = df_display_value[df_display_value['sys_table_column'] == new_column]['dictionary'].iloc[0]
        chart_reference = df_display_value[df_display_value['sys_table_column'] == new_column]['reference'].iloc[0]
        chart_function = df_display_value[df_display_value['sys_table_column'] == new_column]['function'].iloc[0]

        if chart_dictionary == True:
            new_column += '_display_value'
        if chart_reference == True:
            new_column += '_name'
        #output += new_column + '<br>\n'

        if new_column in list(df_table.columns) and charttype == 'Barplot':
            df_tmp = df_table[new_column].value_counts()
            g1 = sns.barplot(x = df_tmp.index, y = df_tmp.values, palette = palette)
            for container in g1.containers:
                g1.bar_label(container)
            g1.axes.set_title('Table: ' + table, fontsize=title_fontsize)
            g1.set_xlabel('Column: ' + column, fontsize=label_fontsize)
            g1.set_ylabel('Count', fontsize=label_fontsize)
            plt.xticks(rotation = 45)
            plt.savefig('static/barplot.png')
            plt.close()
            output += '<p align="center"><a href="/static/barplot.png" target="_new"><img src="/static/barplot.png" width="1000"></a></p>\n'

        if new_column in list(df_table.columns) and charttype == 'Countplot':
            df_tmp = df_table[new_column].value_counts()
            g1 = sns.barplot(x = df_tmp.values, y = df_tmp.index, palette = palette)
            for container in g1.containers:
                g1.bar_label(container)
            g1.axes.set_title('Table: ' + table, fontsize=title_fontsize)
            g1.set_xlabel('Count', fontsize=label_fontsize)
            g1.set_ylabel('Column: ' + column, fontsize=label_fontsize)
            plt.xticks(rotation = 0)
            plt.savefig('static/countplot.png')
            plt.close()
            output += '<p align="center"><a href="/static/countplot.png" target="_new"><img src="/static/countplot.png" width="1000"></a></p>\n'

        if new_column in list(df_table.columns) and charttype == 'Heatmap':
            df_heat = df_table[['name', new_column]].copy()
            df_heat['year'] = pd.DatetimeIndex(df_heat[new_column]).year
            df_heat['month'] = pd.DatetimeIndex(df_heat[new_column]).month
            df_heat['amount'] = 1
            tmp_pivot = pd.pivot_table(df_heat, index='month', columns='year', values='amount', aggfunc=np.sum)
            g1 = sns.heatmap(data=tmp_pivot, cmap=cmap, annot=True, fmt='.20g', cbar_kws={'label': 'Amount'})
            g1.axes.set_title(table + ' / ' + column, fontsize=title_fontsize)
            g1.set_xlabel('Year', fontsize=label_fontsize)
            g1.set_ylabel('Month', fontsize=label_fontsize)
            plt.yticks(rotation=0)
            plt.savefig('static/heatmap.png')
            plt.close()
            output += '<p align="center"><a href="/static/heatmap.png" target="_new"><img src="/static/heatmap.png" width="1000"></a></p>\n'

        if new_column in list(df_table.columns) and charttype == 'Histplot':
            data_points = df_table.shape[0]
            bins = int(np.sqrt(data_points))
            #bins = int(round(df_table[new_column].max()/10, 0))
            g1 = sns.histplot(df_table[new_column], bins=bins, kde=True)
            #g1 = sns.histplot(df_table[new_column], kde=True, palette = palette)
            g1.axes.set_title(table + ' / ' + column, fontsize=title_fontsize)
            g1.set_xlabel('Column: ' + column, fontsize=label_fontsize)
            g1.set_ylabel('Count', fontsize=label_fontsize)
            plt.savefig('static/histplot.png')
            plt.close()
            output += '<p align="center"><a href="/static/histplot.png" target="_new"><img src="/static/histplot.png" width="1000"></a></p>\n'

    output += html_footer()
    return output

