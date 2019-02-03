import plotly.graph_objs as go
import plotly.offline as py

from database.mysql_connector import Connection
from db_management import get_user_rol, delete_by_id


def hist_from_db():
    conn = Connection()
    y = conn.do_query_mult_col('SELECT datetime FROM prediction;')
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
        if prediction is not None:  # There are data to show
            for row in prediction:
                body += new_row(row)
            body += '  </tbody>\
                    </table>'
    return body


def insert_row_model(num_cols, index_id, insert_row, cols):
    for i in range(1, num_cols + 1):
        if i == index_id + 1 or cols[i - 1] in ['train_date', 'acc']:
            insert_row.append(' ')
        elif cols[i - 1] in ['model_type', 'disease']:
            insert_row.append('<input class="form-control" name=\"' + cols[
                i - 1] + '\" style="border-width: thin; border-radius: 10px ; box-sizing: border-box; '
                         'width: 100%" '
                         'type="text" required></input>')
        elif cols[i - 1] in ['dataset_description', 'model_path', 'test_data_path']:
            file_description = {'dataset_description': 'Json file',
                                'model_path': 'Python pkl file',
                                'test_data_path': 'csv or arff file format'}
            file_type = {'dataset_description': 'accept=".json,.JSON"',
                                'model_path': 'accept="leukemia-2019-01-22_142251.pkl,.PKL"',
                                'test_data_path': 'accept=".csv,.CSV,.tsv,.TSV,.arff,.ARFF"'}
            insert_row.append('<div class="input-group">\
                <div class="custom-file">\
                    <input name=\"' + cols[i - 1] + '\" '+file_type[cols[i - 1]]+' style="size: auto" type="file" class="custom-file-input" id="inputGroupFile01" aria-describedby="inputGroupFileAddon01" required>\
                    <label class="custom-file-label" for="inputGroupFile01">' + file_description[cols[i - 1]] + '</label>\
                </div>\
            </div>')
    return insert_row


def generate_table_from_db(table_name):
    conn = Connection()
    cols = conn.do_query(
        'SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=\"' + table_name + '\" AND TABLE_SCHEMA = \'' + conn.get_database() + '\' ORDER BY ORDINAL_POSITION;')
    index_id = cols.index('id')
    num_cols = len(cols)
    table = conn.do_query_mult_col(
        'SELECT * FROM ' + table_name + ';')
    if cols is not None:
        body = '<form class="needs-validation" id="form_funciona" method="post" action="/administration/' + table_name + '/insert" enctype=multipart/form-data>'
        body += '<table class="table" id="table">\
                              <thead>'
        cols.append(' ')  # For delete column
        cols.append(' ')  # For update column
        body += new_head(tuple(cols))
        body += '</thead>  \
                    <tbody>'
        if table is not None:
            row_num = 1
            for row in table:
                row_id = row[index_id]
                body += new_row(row).replace('</tr>',
                                             '<td><a href="/administration/' + table_name + '/delete/' + str(
                                                 row_id) + '"><span class="glyphicon glyphicon-remove"></span></a></td>')  # Adds delete button to each row
                body += '<td><a href="#"><span class="glyphicon glyphicon-pencil" onclick="update_db(' + str(
                    row_num) + ')"></span></a></td></tr>'  # Adds delete button to each row
                row_num += 1
        insert_row = list()
        if table_name == 'model':
            insert_row = insert_row_model(num_cols, index_id, insert_row, cols)
        else:
            for i in range(1, num_cols + 1):
                if i == index_id + 1:
                    insert_row.append(' ')
                else:
                    insert_row.append('<input class="form-control" name=\"' + cols[
                        i - 1] + '\" style="border-width: thin; border-radius: 10px ; box-sizing: border-box; '
                                 'width: 100%" '
                                 'type="text" required></input>')
        insert_row.append(
            '<button class="btn btn-default" type="submit"><a href="#"><span class="glyphicon glyphicon-plus"></span></a></button>')
        insert_row.append(' ')
        body += new_insert_row_form(insert_row)
        print(body)
        body += '  </tbody>'
        body += '</table>'
        body += '</form>'
    return body


def new_row(row):
    row_html = '<tr>'
    row_html += '<th scope="row">' + str(row[0]) + '</th>'
    for col in row[1:]:
        row_html += '<td>' + str(col) + '</td>'
    row_html += '</tr>'
    return row_html


def new_insert_row_form(row):
    row_html = '<td>' + str(row[0]) + '</td>'
    for col in row[1:]:
        row_html += '<td>' + str(col) + '</td>'
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


if __name__ == '__main__':
    delete_by_id('user', 5)
