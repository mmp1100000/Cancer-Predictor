from database.mysql_connector import Connection
from login import get_user_rol
from markupsafe import Markup


def generate_records_table(username, filter):
    rol = get_user_rol(username)
    if rol == "Doctor":
        body = '<table class="table" id="table">\
          <thead>\
            <tr>\
              <th scope="col">PATIENT ID</th>\
              <th scope="col">DATE</th>\
              <th scope="col">DATA</th>\
              <th scope="col">MODEL</th>\
              <th scope="col">OUTPUT</th>\
            </tr>\
          </thead>\
          <tbody>'
        conn = Connection()
        if filter == 'all':
            prediction = conn.do_query_mult_col(
                'SELECT PRE.patient_id, PRE.datetime, PRE.expression_file_path, PRE.result, PRE.model_id FROM prediction PRE, user U WHERE U.email=\"' + username + '\" and U.id=PRE.user_id;')
            print(prediction)
            if prediction is not None:  # There are data to show
                for row in prediction:
                    body += new_row(row)
        elif filter == 'file':
            pass
        elif filter == 'day':
            pass
        elif filter == 'subject':
            pass
        body += '  </tbody>\
                    </table>'
        return body
    elif rol == "Admin":
        body = '<table class="table">\
          <thead>\
            <tr>\
              <th scope="col">USER ID</th>\
              <th scope="col">DATE</th>\
              <th scope="col">MODEL</th>\
            </tr>\
          </thead>\
          <tbody>'
        conn = Connection()
        if filter == 'all':
            prediction = conn.do_query_mult_col(
                'SELECT PRE.user_id, PRE.datetime, PRE.model_id FROM prediction PRE;')
            print(prediction)
            if prediction is not None:  # There are data to show
                for row in prediction:
                    body += new_row(row)
        elif filter == 'user':
            pass
        elif filter == 'day':
            pass
        body += '  </tbody>\
                    </table>'
        return body


def generate_table_from_db(table):
    conn = Connection()
    cols = conn.do_query('SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=\"' + table + '\" AND TABLE_SCHEMA = \'' + conn.get_database() + '\' ORDER BY ORDINAL_POSITION;')
    table = conn.do_query_mult_col(
        'SELECT * FROM ' + table + ';')
    if cols is not None:
        body = '<table class="table" id="table">\
                              <thead>'
        body += new_head(tuple(cols))
        body += '<th> </th></thead>  \
                    <tbody>'
        if table is not None:
            for row in table:
                body += new_row(row).replace('</tr>', '<a href=""><span class="glyphicon glyphicon-remove"></span></a></tr>')

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
    col_num=1
    for col in row[1:]:
        row_html += '<th onclick="sortTable('+str(col_num)+')"><a href="#">' + str(col) + '</a></th>'
        col_num+=1
    row_html += '</tr>'
    return row_html