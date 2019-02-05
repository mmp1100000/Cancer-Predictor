import hashlib

from database.mysql_connector import Connection

conn = Connection()


def user_validation(user, password):
    """
    Checks if the user and password are correct in DB.
    :param user:
    :param password:
    :return: True/False (OK/USER ERROR)
    """
    input_password = hashlib.sha256(password.encode("utf8"))
    hex_dig = input_password.hexdigest()
    true_password = conn.do_query('SELECT password FROM user WHERE email=\"' + user + '\";')
    if len(true_password) == 0:
        return False
    if true_password[0] == hex_dig:
        return True
    return False


def user_registration(firstname, lastname, email, password, repeated_password, rol):
    """
    Checks if patient has already been included in DB. Else includes it.
    :param firstname:
    :param lastname:
    :param email:
    :param password:
    :param repeated_password:
    :param rol:
    :return:
    """
    if password == repeated_password:
        name = firstname + ' ' + lastname
        input_password = hashlib.sha256(password.encode("utf8"))
        hex_dig = input_password.hexdigest()
        row = [name, hex_dig, email, rol]
        query = conn.do_query('SELECT username FROM user WHERE email=\"' + email + '\";')
        if len(query) != 0:
            return False
        else:
            regist = conn.do_query(
                'INSERT INTO user(username, password, email, rol) VALUES (\"' + '\",\"'.join(row) + '\");')
            conn.connection.commit()
            query = conn.do_query('SELECT username FROM user WHERE email=\"' + email + '\";')
            if len(query) == 0:  # User not added
                return False
            else:
                return True
    else:
        return False

