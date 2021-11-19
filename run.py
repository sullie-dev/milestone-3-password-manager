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


def main():
    """Main function"""

    print(connect_db())

    while True:
        is_logged_in = login()
        if is_logged_in:
            print("But... we're in")


main()
