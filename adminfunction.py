import os
from pathlib import Path
import pandas as pd

from cmdbhtml import html_header, html_footer

def adminlistfunctions():
    output = html_header()
    df_func = get_functions()
    #output += str(df_func) + '<br>\n'
    output += '<table id="default">\n'
    output += '<tr>'
    for col in list(df_func.columns):
        output += '<th>' + col + '</th>'
    output += '</tr>\n'
    for row in df_func.iterrows():
        output += '<tr>'
        for col in list(df_func.columns):
            output += '<td>' + row[1][col] + '</td>'
        output += '</tr>\n'
    output += '</table>\n'
    #output += str(functions)
    output += html_footer()
    return output

def get_functions():
    output = ''
    data = {'Path': [], 'Name': [], 'Description': []}
    ldir = os.listdir('function/')
    for ld in ldir:
        output += ld + '<br>\n'
        function_file = 'function/' + ld + '/function.py'
        if Path(function_file):
            data['Path'].append(ld)
            desc = []
            with open(function_file, 'r') as docfile:
                for line in docfile.readlines()[1:3]:
                    desc.append(line.strip())
            for d in desc:
                if d[:6] == 'Name: ':
                    data['Name'].append(d[6:])
                if d[:13] == 'Description: ':
                    data['Description'].append(d[13:])
    df = pd.DataFrame(data)
    return df



