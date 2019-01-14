from database.mysql_connector import Connection
from login import get_user_rol
from markupsafe import Markup
import plotly.offline as py
import plotly.graph_objs as go

import numpy as np


def hist_from_db():
    conn = Connection()
    y = conn.do_query_mult_col('SELECT datetime FROM prediction;')
    print(y)
    x = list()
    for i in range(0, len(y)):
        x.append(y[i][0].day)

    data = [go.Histogram(x=x)]
    first_plot_url = py.plot(data, filename='./template/first_plot.html', auto_open=False)
    with open(first_plot_url.replace("file://", "")) as plot_html_file:
        return plot_html_file.read()


def generate_records_table(username):
    rol = get_user_rol(username)
    if rol == "Doctor":
        cols = ('PATIENT ID', 'DATE', 'DATA', 'MODEL', 'OUTPUT')
        body = '<table class="table" id="table">\
                                              <thead>'
        body += new_head(cols)
        body += '</thead>  \
                                    <tbody>'
        conn = Connection()
        if filter == 'all':
            prediction = conn.do_query_mult_col(
                'SELECT PRE.patient_id, PRE.datetime, PRE.expression_file_path, PRE.result, PRE.model_id FROM prediction PRE, user U WHERE U.email=\"' + username + '\" and U.id=PRE.user_id;')
            print(prediction)
            if prediction is not None:  # There are data to show
                for row in prediction:
                    body += new_row(row)
        body += '  </tbody>\
                    </table>'
        return body
    elif rol == "Admin":
        cols = ('PREDICTION ID', 'USER ID', 'DATE', 'MODEL')
        body = '<table class="table" id="table">\
                                      <thead>'
        body += new_head(cols)
        body += '</thead>  \
                            <tbody>'
        conn = Connection()
        prediction = conn.do_query_mult_col(
            'SELECT PRE.id, PRE.user_id, PRE.datetime, PRE.model_id FROM prediction PRE;')
        print(prediction)
        if prediction is not None:  # There are data to show
            for row in prediction:
                body += new_row(row)
            body += '  </tbody>\
                    </table>'
        print(body)
    return body


def generate_table_from_db(table):
    conn = Connection()
    cols = conn.do_query(
        'SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=\"' + table + '\" AND TABLE_SCHEMA = \'' + conn.get_database() + '\' ORDER BY ORDINAL_POSITION;')
    table = conn.do_query_mult_col(
        'SELECT * FROM ' + table + ';')
    if cols is not None:
        body = '<table class="table" id="table">\
                              <thead>'
        cols.append(' ')  # For delete column
        cols.append(' ')  # For update column
        body += new_head(tuple(cols))
        body += '</thead>  \
                    <tbody>'
        if table is not None:
            row_num = 1
            for row in table:
                body += new_row(row).replace('</tr>',
                                             '<td><a href="#"><span class="glyphicon glyphicon-remove"></span></a></td>')  # Adds delete button to each row
                body += '<td><a href="#"><span class="glyphicon glyphicon-pencil" onclick="update_db(' + str(
                    row_num) + ')"></span></a></td></tr>'  # Adds delete button to each row
                row_num += 1

        body += '  </tbody>\
                        </table>'
        print(body)
    return body


def new_row(row):
    row_html = '<tr>'
    row_html += '<th scope="row">' + str(row[0]) + '</th>'
    for col in row[1:]:
        row_html += '<td>' + str(col) + '</td>'
    row_html += '</tr>'
    return row_html


def new_head(row):
    row_html = '<tr>'
    row_html += '<th scope="row">' + str(row[0]) + '</th>'
    col_num = 1
    for col in row[1:]:
        row_html += '<th onclick="sortTable(' + str(col_num) + ')"><a href="#">' + str(col) + '</a></th>'
        col_num += 1
    row_html += '</tr>'
    return row_html
