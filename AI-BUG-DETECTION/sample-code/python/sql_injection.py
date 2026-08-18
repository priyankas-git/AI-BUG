import sqlite3

def get_user_profile(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Bug: SQL injection pattern via string formatting
    query = "SELECT * FROM users WHERE username = '%s'" % username
    cursor.execute(query)
    
    return cursor.fetchall()
