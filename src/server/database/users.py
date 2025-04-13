from db import cusor

def get_user(username):
    query = "SELECT * FROM users WHERE username = %s"
    cusor.execute(query, (username,))
    user = cusor.fetchone()
    if user:
        return {
            'id': user[0],
            'username': user[1],
            # 'password': user[2],
            'email': user[3],
            'first_name': user[4],
            'last_name': user[5],
            'phone': user[6],
            'address': user[7],
            'city': user[8],
            'state': user[9],
            'zip': user[10],
            'country': user[11],
            'status': user[12],
            'account_number': user[13],
            'created_at': str(user[14]),
            'updated_at': str(user[15])
        }
    else:
        return None
