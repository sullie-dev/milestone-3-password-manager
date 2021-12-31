import os
import psycopg2
import random
import string
from cryptography.fernet import Fernet
from tabulate import tabulate


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
    """Encrypt users password"""
    key = os.getenv("KEY")
    encrypted_password = password.encode()
    encryption = Fernet(bytes(key, "utf-8"))

    encrypted_password = encryption.encrypt(encrypted_password).decode()

    return encrypted_password


def decrypt_password(password):
    """Decrypt password"""
    key = os.getenv("KEY")
    encryption = Fernet(bytes(key, "utf-8"))

    decrypted_password = encryption.decrypt(bytes(password, "utf-8")).decode()

    return decrypted_password


class PasswordCreation:

    @staticmethod
    def capture_username():
        capturing = True
        while capturing:
            try:
                username = input("Please enter the username ")

                if username == "":
                    raise ValueError
            except ValueError:
                print("Username field can't be empty, please enter a username.")
                continue
            return username

    @staticmethod
    def capture_password(password):
        capturing = True
        while capturing:
            if password is None:
                try:
                    password = input("Please enter your password,\n"
                                     "Passwords should be between 8 and 25 characters long ")
                    if password == "":
                        raise ValueError
                except ValueError:
                    print('Password field cannot be empty, please enter a password')
                    continue
                while len(password) > 0:
                    length_check = check_password(len(password))
                    if length_check is True:
                        break
                    else:
                        print(length_check)
                        password = input(
                            "Please enter your password\n"
                            "Passwords should be between 8 and 25 characters long ")

            capturing = False
        return password

    @staticmethod
    def capture_url():
        capturing = True
        while capturing:
            try:
                url = input('Please enter the url of the website ')
                if url == "":
                    raise ValueError
            except ValueError:
                print("URL can't be empty, please enter the address of the site")
                continue
            capturing = False
        return url

    @staticmethod
    def capture_password_name():
        capturing = True
        while capturing:
            try:
                password_name = input("What would you like to name this password? ")
                is_unique = search_database("password_name", password_name)
                if is_unique:
                    raise LookupError
                elif password_name == "":
                    raise ValueError

            except LookupError:
                print('Your password should have a unique name')
                continue
            except ValueError:
                print("The password name can't be left blank")
            capturing = False
        return password_name

    @staticmethod
    def write_password_to_db(connection, username, encrypt_password, url, password_name):
        connection = connection
        cursor = connection.cursor()

        insert_query = """ INSERT INTO passwords (username, password, url, password_name) VALUES (%s,%s,%s,%s)"""
        record_to_insert = (username, encrypt_password, url, password_name)
        cursor.execute(insert_query, record_to_insert)

        print("Adding your password.")
        print("Adding your password..")
        print("Adding your password...")

        connection.commit()
        print("Password added to the database\n")


def check_password(password):
    """
    Accepts the length of a password string to check if it is within 8-25 characters.
    Returns if the password is too long or too short. If the passwords is the right
    length it returns True, if statement is used to break the parent loop
    """
    if password < 8:
        return "Password is to short...\n"
    elif password > 25:
        return "Password is to long...\n"
    else:
        return True


def create_password(connection, password=None):
    """Allow user to create a new database entry"""

    manager = PasswordCreation
    username = manager.capture_username()
    password = manager.capture_password(password)
    url = manager.capture_url()
    password_name = manager.capture_password_name()
    encrypt_password = encrypt_user_password(password)
    manager.write_password_to_db(connection, username, encrypt_password, url, password_name)


def generate_password(length):
    """
    Generates a random password for the user
    Credit: Medium article on password generation in README.md
    """
    upper_string = string.ascii_uppercase
    lower_string = string.ascii_lowercase
    numerical = string.digits
    symbol = string.punctuation

    alphabet = upper_string + lower_string + numerical + symbol
    random_character = random.sample(alphabet, length)
    random_password = "".join(random_character)

    print(random_password)
    add_new_password = input("Do you want to save this as a new password, "
                             "(y)es or (n)o? ")

    if add_new_password == "y":
        create_password(connect_db(), random_password)
    else:
        menu()


def generate_table(values):
    """
    Add passwords to a table
    Credit: Create tables in Python in README.md

    """
    headers = ["Username", "Password", "URL", "Password name"]
    table_values = []
    for value in values:
        username, password, url, pw_name = value
        password = decrypt_password(value[1])
        temp_tup = (username, password, url, pw_name)
        table_values.append(temp_tup)

    print("\n" + tabulate(table_values, headers=headers) + "\n")


def search_database(column, search_term):
    """Search database for passwords"""
    connection = connect_db()
    cursor = connection.cursor()

    search_query = f"SELECT * from passwords WHERE {column}='{search_term}'"
    cursor.execute(search_query)
    connection.commit()
    result = cursor.fetchall()

    if not result:
        return False
    else:
        return result


def find_password():
    """Allow user to search by the email/username or password name"""

    column_search = int(input("Would you like to\n"
                              "1. Search by username\n"
                              "2. By the password name?\n"))
    search_term = input("What would you like to search for ")

    if column_search == 1:
        search = search_database("username", search_term)
    elif column_search == 2:
        search = search_database("password_name", search_term)

    if not search:
        print(f"No passwords found for {search_term}")
    else:
        return generate_table(search)


def delete_password():
    connection = connect_db()
    cursor = connection.cursor()

    while True:
        try:
            password_name = input("Enter the name of the password you want to remove:  ")
            does_entry_exists = search_database("password_name", password_name)
            if not does_entry_exists:
                raise LookupError
        except LookupError:
            print(f"There is no password with the name {password_name} saved")
            continue
        break

    delete_query = f""" DELETE from passwords WHERE password_name='{password_name}'"""
    cursor.execute(delete_query)
    connection.commit()
    print(f"Successfully deleted the password {password_name}\n")


def show_all():
    """Search database for all passwords"""
    connection = connect_db()
    cursor = connection.cursor()

    search_query = f"SELECT * FROM passwords"
    cursor.execute(search_query)
    connection.commit()
    result = cursor.fetchall()
    generate_table(result)

    if not result:
        return False
    else:
        return result


def menu():
    """Allows the user to be able to pick which option they want to select"""
    print("What option would you like to choose? (choose the menu number)\n")
    while True:

        menu_option = input("1. Add a new password\n"
                            "2. Generate a new password\n"
                            "3. Search for a password\n"
                            "4. Show all passwords\n"
                            "5. Delete a password\n"
                            "6. Exit password manager\n\n"
                            "Your choice: ")
        if menu_option == '1':
            create_password(connect_db())
        elif menu_option == '2':
            while True:
                password_length = int(input("How long do you want the password to be?\n"
                                            "Password's should be more than 8 characters and "
                                            "a max of 25 characters long.\n"))
                length_check = check_password(password_length)
                if length_check is True:
                    break
                else:
                    print(length_check)

            generate_password(password_length)
        elif menu_option == '3':
            find_password()
        elif menu_option == '4':
            show_all()
        elif menu_option == '5':
            delete_password()
        elif menu_option == '6':
            exit()
        else:
            print('\nInvalid option\n')


def main():
    """Main function"""

    while True:
        if login():
            menu()
        else:
            login()


main()
