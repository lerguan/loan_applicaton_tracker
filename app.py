import sys
from server.application_manager import ApplicationManager
from server.user_manager import UserManager
from tabulate import tabulate

def main_menu():
    print("\nWelcome to the Loan Application Tracker!")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    
    choice = input("Please select an option: ")
    return choice

def application_menu():
    print("\nApplication Management Menu:")
    print("1. Assign New Application to Me")
    print("2. Search for Application")
    print("3. Update Application Status")
    print("4. Check Application Status")
    print("5. Display Applications Assigned to Me")
    print("6. Logout")
    
    choice = input("Please select an option: ")
    return choice

def add_new_application():
    application_id = input("Enter application ID: ")
    status = input("Enter Application Status (Review, Approved, Issuing, Issued, Withdrawed, Expired) [optional]: ") or "Submitted"
    return application_id, status

def main():
    user_manager = UserManager()
    app_manager = ApplicationManager()
    current_user = None
    headers = ["ID", "Income", "Age", "Exp. Yrs", "Marital Status", "House Ownership", "Car Ownership", 
           "Profession", "City", "State", "Job Yrs", "House Yrs", "Risk Flag", "Date", "Status"]
    
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
            if type(result) is not str:
                current_user = result
                user_id = current_user.user_id
                print(f'Welcome back, {current_user.fullname}!')
                
                while True:
                    app_choice = application_menu()
                    
                    if app_choice == '1':
                        # Add New Application
                        application_id = input("Enter application ID to be assigned: ")
                        result = app_manager.post(user_id, application_id)
                        if result:
                            print('\n')
                            print(f'***Application already assigned OR not found***')
                        else:
                            print('\n')
                            print(f'***Application (ID: {application_id}) assigned sucessfully!***')
                    
                    elif app_choice == '2':
                        # Search for Application
                        application_id = input("Enter Application ID to search for applications: ")
                        result = app_manager.get_by_app_id(application_id)
                        if not result:
                            print('\n')
                            print("***Application not found!***")
                        else:
                            print('\n')
                            print(tabulate(result, headers, tablefmt='grid'))
                    
                    elif app_choice == '3':
                        # Update Application Status
                        application_id = input("Enter Application ID to update: ")
                        result = app_manager.get_status(user_id, application_id)
                        if not result:
                            print('\n')
                            print('***Application not found OR not assigned!***')
                        else:
                            print('\n')
                            print(f'The application (ID: {result[0][0]}) current status: {result[0][1]}')
                            new_status = input("Enter new status (Review, Approved, Issuing, Issued, Withdrawed, Expired): ") or 'Submitted'
                            result = app_manager.patch_status(application_id, new_status)
                            print(result)

                    elif app_choice == '4':
                        # Check Application Status
                        application_id = input("Enter Application ID to check status: ")
                        result = app_manager.get_status(user_id, application_id)
                        if not result:
                            print('\n')
                            print('***Application not found OR not assigned!***')
                        else:
                            print('\n')
                            print(f'The application (ID: {result[0][0]}) status: {result[0][1]}')

                    
                    elif app_choice == '5':
                        # Display Application
                        user_id = current_user.user_id
                        result = app_manager.get(user_id)
                        if result:
                            print('\n')
                            print(tabulate(result, headers, tablefmt='grid'))
                        else:
                            print('\n')
                            print('Application not found!')

                    elif app_choice == '6':
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
