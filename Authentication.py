import sqlite3
conn = sqlite3.connect("credentials_and_client_data")
cursor = conn.cursor()

# Authenticates the user by checking their ID and password from the credentials table.


def authenticate_user(user_id, user_password, database_cursor):
    database_cursor.execute("""
    SELECT rowid, Role, Username, Password FROM credentials
     WHERE rowid=? AND Password=?""", (user_id, user_password))
    result = database_cursor.fetchone()
    if result:
        return True and result[1]
    else:
        return False

# Checks if a transfer is eligible, if receiver_id and sender_id exist and
# if sender's CurrentAmount isn't greater than transfer amount


def transfer_eligibility(sender_id, receiver_id, amount):
    cursor.execute("""SELECT * FROM client_data
    WHERE ID = ? AND CurrentAmount >= ?""", (sender_id, amount))
    sender = cursor.fetchone()
    cursor.execute("""SELECT * FROM client_data 
    WHERE ID = ?""", (receiver_id,))
    receiver = cursor.fetchone()
    if sender and receiver:
        return True
    else:
        return False

# Checks if a client's withdraw amount doesn't exceed their CurrentAmount


def withdraw_eligibility(client_id, withdraw_amount):
    cursor.execute("""
            SELECT * FROM client_data
             WHERE ID = ? AND CurrentAmount >= ?""", (client_id, withdraw_amount))
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False

# Fetches a list of all client (their IDs and usernames)
# for admins and tellers to see


def get_list_clients():
    cursor.execute("SELECT rowid, Username FROM credentials WHERE Role='client'")
    items = cursor.fetchall()
    for item in items:
        print(item)

# Checks the conditions if a client is eligible for a loan


def loan_eligibility(client_id, loan_amount):
    cursor.execute("""
        SELECT * FROM client_data
         WHERE ID = ? AND LoanLimit >= ? AND CreditScore >= 7.0""", (client_id, loan_amount))
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False
