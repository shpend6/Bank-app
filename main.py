from Operations import admin_operations
from Operations import teller_operations
from Operations import client_operations
from Authentication import authenticate_user
import sqlite3
import getpass  # This module is used to hide the password,
# but if you don't change your Pycharm configuration settings it will apparently crash your program
# Steps: 'Modify Run Configuration' > 'Emulate Terminal in Output Console'
conn = sqlite3.connect("credentials_and_client_data")  # connects to the database file
cursor = conn.cursor()  # creates a cursor of the file, to be used for commands later


def startapp():  # starts the application, using authenticate_user()
    while True:  # it calls respective operations of users
        confirmation = input("Press any key to continue, type 'exit' to exit the system entirely:\n")
        if confirmation == "exit":
            break
        user_id = input("Enter your ID: ")
        password = getpass.getpass("Enter password: ")
        if authenticate_user(user_id, password, cursor):  # authenticate_user() also returns
            if authenticate_user(user_id, password, cursor) == "teller":   # the role of the user
                teller_operations()
            elif authenticate_user(user_id, password, cursor) == "admin":
                admin_operations()
            elif authenticate_user(user_id, password, cursor) == "client":
                client_operations(user_id)

        print('Try again!')


startapp()
conn.close()
