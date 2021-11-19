import os
import psycopg2


def login():
    """Check to make sure the master password is correct"""
    password = input("Enter the master password: ")
    master_password = os.getenv("MASTER_PASSWORD")
    if password == master_password:
        print("Kittridge, You've Never Seen Me Very Upset!")
        return True
    else:
        print("Oh no, the password... it's wrong")
        return False


def connect_db():
    try:
        database_url = os.getenv("DATABASE_URL")
        db_connection = psycopg2.connect(database_url, sslmode="require")
        return db_connection
    except Exception as e:
        print(e)


def menu():
    print("What would you like to do?")
    menu_option = int(input("1. Add new password\n2. Generate a new password\n"))

    try:
        if menu_option == 1:
            print("menu option 1")
        elif menu_option == 2:
            print("menu option 2")
        else:
            print("Invalid choice")
    except ValueError as e:
        print(e)


def main():
    """Main function"""

    print(connect_db())

    while True:
        is_logged_in = login()
        if is_logged_in:
            print("But... we're in")
            menu()


main()
