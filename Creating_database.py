# This is how I created the database tables: credentials, client_data,and loan_logs
# I saved the file for personal reference and to show the procedure
# IT DOES NEED TO BE RUN AGAIN

import sqlite3
conn = sqlite3.connect("credentials_and_client_data")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE credentials (
    Role text,
    Username text,
    Password text
)""")
list_cred = [('admin', 'John Smith', '11111'), ('teller', 'Tiffany Scott', '2222'), ]
cursor.executemany("INSERT INTO credentials VALUES (?, ?, ?)", list_cred)
cursor.execute("""CREATE TABLE client_data (
    ID integer,
    Username text,
    CurrentAmount integer,
    CreditScore real,
    LoanLimit integer,
    LoanMonthLimit integer
)""")
cursor.execute("""CREATE TABLE loan_logs (
    ID int,
    LoanAmount integer,
    IssuanceDate text,
    ReturnDate text
)""")

conn.commit()

conn.close()
