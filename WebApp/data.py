from database.mysql_connector import Connection


def generate_table(username, filter):
    body = '<table class="table">\
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


def new_row(row):
    row_html = '<tr>'
    row_html += '<th scope="row">' + str(row[0]) + '</th>'
    for col in row[1:]:
        row_html += '<td>' + str(col) + '</td>'
    row_html += '</tr>'
    return row_html
