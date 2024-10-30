import sys
from server.application_manager import ApplicationManager
from server.user_manager import UserManager

def main_menu():
    print("\nWelcome to the Loan Application CLI!")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    
    choice = input("Please select an option: ")
    return choice

def application_menu():
    print("\nApplication Management Menu:")
    print("1. Add New Application")
    print("2. Search for Application")
    print("3. Update Application Status")
    print("4. Check Application Status")
    print("5. Logout")
    
    choice = input("Please select an option: ")
    return choice

def get_application_details():
    user_id = input("Enter User ID: ")
    create_date = input("Enter Creation Date (YYYY-MM-DD) [optional]: ")
    status = input("Enter Application Status [optional]: ") or "SUBMITTED"
    return user_id, create_date, status

def main():
    user_manager = UserManager()
    app_manager = ApplicationManager()
    current_user = None

    while True:
        choice = main_menu()

        if choice == '1':
            # Register
            email = input("Enter your email: ")
            fullname = input("Enter your full name: ")
            password = input("Enter your password: ")
            role = input("Enter your role: ")
            department = input("Enter your department: ")

            result = user_manager.register_user(password, email, fullname, role, department)
            print(result)

        elif choice == '2':
            # Login
            email = input("Enter your email: ")
            password = input("Enter your password: ")

            result = user_manager.login_user(email, password)
            if "Welcome" in result:
                current_user = email  # Store logged in user's email
                print(result)
                
                while True:
                    app_choice = application_menu()
                    
                    if app_choice == '1':
                        # Add New Application
                        user_id, create_date, status = get_application_details()
                        result = app_manager.post(create_date=create_date, user_id=user_id, application_status=status)
                        print(result)
                    
                    elif app_choice == '2':
                        # Search for Application
                        user_id = input("Enter User ID to search for applications: ")
                        result = app_manager.get(user_id)
                        print(result)
                    
                    elif app_choice == '3':
                        # Update Application Status
                        app_id = input("Enter Application ID to update: ")
                        new_status = input("Enter new status: ")
                        result = app_manager.patch_status(app_id, new_status)
                        print(result)

                    elif app_choice == '4':
                        # Check Application Status
                        app_id = input("Enter Application ID to check status: ")
                        result = app_manager.get_status(app_id)
                        print(result)

                    elif app_choice == '5':
                        # Logout
                        current_user = None
                        print("You have been logged out.")
                        break

                    else:
                        print("Invalid option. Please try again.")

            else:
                print(result)

        elif choice == '3':
            print("Exiting the application.")
            sys.exit(0)

        else:
            print("Invalid option. Please try again.")

if __name__ == '__main__':
    main()
