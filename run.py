import os
import psycopg2
import random
import string
import base64


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
    """Connects to the database"""
    try:
        database_url = os.getenv("DATABASE_URL")
        db_connection = psycopg2.connect(database_url, sslmode="require")
        return db_connection
    except Exception as e:
        print(e)


def encrypt_user_password(password):
    salt_1 = os.getenv('SALT_1')
    salt_2 = os.getenv("SALT_2")

    pre_encrypted_password = password + salt_1 + salt_2
    encrypted_password = base64.b64encode(bytes(pre_encrypted_password, 'utf-8'))
    return encrypted_password


def decrypt_password(password):
    salt_1 = os.getenv('SALT_1')
    salt_2 = os.getenv("SALT_2")
    hash_key = len(salt_1+salt_2)
    encrypted_password = password
    password = base64.b64decode(encrypted_password, altchars="'b", validate=True)

    return str(password[:hash_key])


def create_password(connection, password=None):
    """Allow user to create a new database entry"""
    username = input("Please enter the username ")
    if password is None:
        password = input("Please enter your password ")
    url = input('Please enter the url of the website ')
    password_name = input("What would you like to name this password? ")
    encrypt_password = encrypt_user_password(password)

    connection = connection
    cursor = connection.cursor()

    insert_query = """ INSERT INTO passwords (username, password, url, password_name) VALUES (%s,%s,%s,%s)"""
    record_to_insert = (username, encrypt_password, url, password_name)
    cursor.execute(insert_query, record_to_insert)

    print("Adding your password.")
    print("Adding your password..")
    print("Adding your password...")

    connection.commit()
    print("Password added to the database")


def generate_password(length):
    """Generates a random password for the user"""
    upper_string = string.ascii_uppercase
    lower_string = string.ascii_lowercase
    numerical = string.digits
    symbol = string.punctuation

    alphabet = upper_string + lower_string + numerical + symbol
    random_character = random.sample(alphabet, length)
    random_password = "".join(random_character)

    add_new_password = input("Do you want to enter this as a new password? ")

    if add_new_password == "yes":
        create_password(connect_db(), random_password)
    else:
        return random_password

    return random_password


def search_database(column, search_term):
    """Search database for passwords"""
    connection = connect_db()
    cursor = connection.cursor()

    search_query = f"SELECT * from passwords WHERE {column}='{search_term}'"
    cursor.execute(search_query)
    connection.commit()
    result = cursor.fetchall()

    if not result:
        result = f"No passwords found for {search_term}"

    return result


def find_password():
    """Allow user to search by the email/username or password name"""

    column_search = int(input("Would you like to\n1. Search by username/email\n2. By the password name?\n"))
    search_term = input("What would you like to search for ")

    try:
        if column_search == 1:
            search = search_database("username", search_term)
        elif column_search == 2:
            search = search_database("password_name", search_term)

    except ValueError as e:
        print(e)

    print(search)


def menu():
    """Allows the user to be able to pick which option they want to select"""
    print("What would you like to do?")
    menu_option = int(input("1. Add new password\n2. Generate a new password\n3. Search for password\n"))

    try:
        if menu_option == 1:
            create_password(connect_db())
        elif menu_option == 2:
            length = int(input("How long do you want the password to be? "))
            print(generate_password(length))
        elif menu_option == 3:
            find_password()
        else:
            print("Invalid choice")
    except ValueError as e:
        print(e)


def main():
    """Main function"""

    while True:
        is_logged_in = login()
        while is_logged_in:
            print("But... we're in")
            menu()


main()
