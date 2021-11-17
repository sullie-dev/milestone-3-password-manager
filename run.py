def login():
    """Check to make sure the master password is correct"""
    password = input("Enter the master password: ")
    master_password = "pw123"
    if password == master_password:
        print("Kittridge, You've Never Seen Me Very Upset!")
        return True
    else:
        print("Oh no, the password... it's wrong")
        return False


def main():
    """Main function"""
    while True:
        is_logged_in = login()
        if is_logged_in == True:
            print("But... we're in")
            break


main()
