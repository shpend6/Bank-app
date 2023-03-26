from Authentication import withdraw_eligibility
from Authentication import transfer_eligibility
from Authentication import get_list_clients
from Authentication import loan_eligibility
import random
import sqlite3
import getpass
from datetime import datetime
conn = sqlite3.connect("credentials_and_client_data")
cursor = conn.cursor()


def loan_logs(client_id, loan_amount):
    time = datetime.now()
    only_date = time.date()
    cursor.execute("INSERT INTO loan_logs VALUES(?,?,?,'-//-')", (client_id, loan_amount, only_date))
    conn.commit()

# Allows the admin to create a client, then saves his credentials in the 'credentials' table
# and his information in the client_data table. Allows the admin to view the
# list of all clients (their IDs and usernames).


def admin_operations():
    while True:
        print("Type 0 to create new customer")
        print("Type 1 to see list of clients")
        print("Type exit to log out")
        operation = input("")
        if operation == "0":
            user_name = input("Enter client's full name: ")
            user_password = getpass.getpass("Enter client's password: ")
            credit_score = round(random.uniform(5.0, 10.0), 1)
            cursor.execute("INSERT INTO credentials VALUES('client', ?, ?)", (user_name, user_password))
            cursor.execute("""INSERT INTO client_data 
            VALUES((SELECT MAX(rowid)  
            FROM credentials), ?, 0, ?, 10000, 12)""", (user_name, credit_score))
            conn.commit()
            print("New client added successfully!")
        elif operation == "1":
            get_list_clients()
        elif operation == "exit":
            break

# Allows the teller to issue a loan, then updates the CurrentAmount LoanLimit in client_data table.
# A loan can only be a positive number, not greater than the LoanLimit and the client's
# credit score has to be greater than 7.0
# Allows the teller to view the list of all clients (their IDs and usernames).


def teller_operations():
    while True:
        print("Enter 0 to issue loan")
        print("Enter 1 to see list of clients")
        print("Type exit to log out")
        operation = input("")
        if operation == "exit":
            break
        elif operation == "0":
            client_id = input("Enter client's ID: ")

            try:
                loan_amount = int(input("Enter loan amount: "))
            except:
                loan_amount = 0
            if loan_amount <= 0:
                print("==================")
                print("Loan amount has to be a valid number.")
                print("==================")
            elif loan_eligibility(client_id, loan_amount):
                cursor.execute("""UPDATE client_data SET CurrentAmount = CurrentAmount + ?, 
                LoanLimit = LoanLimit - ? 
                WHERE ID = ?""", (loan_amount, loan_amount, client_id))
                loan_logs(client_id, loan_amount)
                conn.commit()
                print("==================")
                print("Loan was issued successfully")
                print("==================")
            else:
                print("==================")
                print("Loan did not issue successfully.")
                print("==================")
        elif operation == "1":
            get_list_clients()
        else:
            print("Please enter a valid command.")


# Allows the client to do these operations: view balance, view LoanLimit, withdraw money, and
# transfer funds to another account.


def client_operations(client_id):
    while True:
        print("Press 0 to receive bank statement")
        print("Press 1 to see remaining loan limit")
        print("Press 2 to withdraw money")
        print("Press 3 to transfer funds to another account")
        print("Enter 'exit' to log out")
        operation = input("")
        if operation == 'exit':
            break
        if operation == "0":
            cursor.execute("SELECT CurrentAmount FROM client_data WHERE ID=?", (client_id,))
            items2 = cursor.fetchone()
            for item in items2:
                print("==================")
                print("Your current amount is: " + str(item))
                print("==================")
        elif operation == "1":
            cursor.execute("SELECT LoanLimit FROM client_data WHERE ID=?", (client_id,))
            items2 = cursor.fetchone()
            for item in items2:
                print("==================")
                print("Your loan limit is: " + str(item))
                print("==================")
        elif operation == "2":
            while True:
                try:
                    withdraw_amount = int(input("Enter the amount you wish to withdraw: "))
                except:
                    withdraw_amount = 0
                if withdraw_amount == -1:
                    break
                elif withdraw_amount <= 0:
                    print("==================")
                    print("Please enter a valid number.")
                    print("Enter -1 to exit screen.")
                    print("==================")
                elif withdraw_eligibility(client_id, withdraw_amount):
                    cursor.execute("""UPDATE client_data SET CurrentAmount = CurrentAmount - ?
                    WHERE ID = ?""", (withdraw_amount, client_id))
                    conn.commit()
                    print("==================")
                    print("Withdrawal successful.")
                    print("==================")
                    break
                else:
                    print("==================")
                    print("Insufficient funds, please enter a valid number. Enter -1 to exit screen.")
                    print("==================")
        elif operation == "3":
            receiver_id = input("Enter the ID of account receiving the money: ")
            transfer_amount = input("Enter the amount: ")
            if receiver_id == client_id:
                print("==================")
                print("You can't transfer money to your own account :)")
                print("==================")
            elif transfer_eligibility(client_id, receiver_id, transfer_amount):
                cursor.execute("""UPDATE client_data SET CurrentAmount = CurrentAmount - ? 
                WHERE ID = ?""", (transfer_amount, client_id))
                cursor.execute("""UPDATE client_data SET CurrentAmount = CurrentAmount + ?  
                WHERE ID = ?""", (transfer_amount, receiver_id))
                conn.commit()
                print("==================")
                print("Transfer is complete!")
                print("==================")
            else:
                print("==================")
                print("Transfer isn't eligible")
                print("==================")
