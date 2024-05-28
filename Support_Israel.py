import psycopg2
from datetime import date

Hostname = 'localhost'
Username = 'postgres'
Password = '07111989'
Database = 'support_israel'
connection = psycopg2.connect(host=Hostname, user=Username, password=Password, dbname=Database)
cursor = connection.cursor()

user_id = None
user_name = None
user_email = None
user_password = None

sign_up_status = None
institution_id = None
institution_website = None


initial_menu_choice = None # Auxiliar for menu: initial_menu


##########################################################################################################


def initial_menu():
    global initial_menu_choice
    global user_id
    global user_name
    global user_email
    global user_password

    print("")

    print("******************** INITIAL MENU ********************")
    print("*                                                    *")
    print("* Type 'I' to Sign in                                *")
    print("* Type 'U' to Sign up                                *")
    print("* Type 'E' to Exit                                   *")
    print("*                                                    *")
    print("******************************************************")

    initial_menu_choice = input("\n> What do you wanna do? ").lower()


##########################################################################################################

def sign_in_menu():

    global user_id
    global user_name
    global user_email
    global user_password

    global cursor
    global connection

    print("\n")
    print("******************** SIGN IN MENU ********************")
    aut_email = input("\n> Please enter your email: ").lower()
    aut_password = input("> Please enter your password (8 digits): ").lower()

    query = f'''
                 SELECT id , name , last_name , email , password 
                 FROM donators
                 WHERE email = %s
                 LIMIT 1;
                 '''

    cursor.execute(query, (aut_email,))
    connection.commit()
    result = cursor.fetchone()

    if result == False:
        print("Email not found")
        main()

    else:

        db_donator_id, db_donator_name, db_donator_last_name, db_donator_email, db_donator_password = result

        if db_donator_password != aut_password:
            print("Password incorrect")
            main()

        else:
            user_id = db_donator_id
            user_name = db_donator_name
            user_email = db_donator_email
            user_password = db_donator_password
            print(f"Login successful! It's nice to see you again {user_name}.\n")
            users_menu()


##########################################################################################################


def sign_up_menu():

    global cursor
    global connection

    global user_id
    global user_name
    global user_email
    global user_password

    print("\n")

    print("********************* SIGN UP MENU *********************")
    print("*                                                      *")
    print("* We are glad you want to sign up                      *")
    print("* Please enter the your personal details as requested  *")
    print("*                                                      *")
    print("*********************************************************")

    new_email = input("\n> Enter your email: ")

    query = f'''
                SELECT COUNT(email) 
                FROM donators
                WHERE email = %s
                LIMIT 1;
                '''

    cursor.execute(query, (new_email,))
    connection.commit()
    result = cursor.fetchone()
    occurrence = result[0]

    if occurrence > 0:

        print(
            "This email is associated to an existing account. Please sign in with your password or create a new account.\n")
        sign_up_status = 0
        main()

    else:

        new_name = input("> Enter your first name: ")
        new_last_name = input("> Enter your last name: ")
        new_country = input("> Enter your country: ")
        new_city = input("> Enter your city: ")
        new_phone = input("> Enter your phone: ")

        # while True:
        #     try:
        #         input_password = input("> Enter your password: ")
        #         if len(input_password) == 8:
        #             new_password = input_password
        #             break
        #         else:
        #             print("Your password must contain 8 characters. Please enter a valid password.")
        #
        #     except ValueError:
        #         print("Your password must contain 8 characters. Please enter a valid password.")

        while True:
            input_password = input("> Enter your password: ")
            if len(input_password) == 8:
                new_password = input_password
                break
            else:
                print("Your password must contain 8 characters. Please enter a valid password.")

        query = f'''
                INSERT INTO donators (name , last_name , country , city , email , phone , password) VALUES
                (%s , %s , %s , %s , %s , %s , %s) ;
        '''

        cursor.execute(query, (new_name, new_last_name, new_country, new_city, new_email, new_phone, new_password))
        connection.commit()

        print("Signup successful!")
        sign_up_status = 1

        user_name = new_name
        user_email = new_email
        user_password = new_password

        users_menu() # Takes user to menu: users_menu


##########################################################################################################


def users_menu():

    global user_id
    global user_name
    global user_email
    global user_password

    print("\n")

    print("********************* USER  MENU *********************")
    print("*                                                    *")
    print("* Type 'D' to Display institutions                   *")
    print("* Type 'S' to Show your donations history            *")
    print("* Type 'E' to Exit                                   *")
    print("*                                                    *")
    print("******************************************************")

    while True:

        users_menu_choice = input("\n> What do you wanna do? ").lower()

        if users_menu_choice == "d":
            institutions_menu()
            break

        elif users_menu_choice == "s":
            donations_history()
            break

        elif users_menu_choice == "e":
            break

        else:
            print("Invalid input. Try again.")
            continue



##########################################################################################################


def institutions_menu():

    global user_id
    global user_name
    global user_email
    global user_password

    print("\n")

    print("***************** INSTITUTIONS MENU *****************")
    print("*                                                   *")
    print("* Type 'A' to show ALL institutions                  *")
    print("* Type 'C' to show institutions by category         *")
    print("* Type 'R' to Return users menu                  *")
    print("*                                                   *")
    print("******************************************************")

    while True:

        institutions_menu_choice =  input("\n> What do you wanna do? ").lower()

        if institutions_menu_choice == "a":
            show_all_institutions()
            break

        elif institutions_menu_choice == "c":
            show_categories()
            break

        elif institutions_menu_choice == "r":
            users_menu()
            break

        else:
            print("Invalid input. Try again.")
            continue


##########################################################################################################


def donations_history():

    global user_id

    query = f'''
            SELECT d.institution_id , i.name , d.date , d.value , d.currency , d.payment_method , d.frequency , i.category , i.description
            FROM donations d
            JOIN institutions i
            ON d.institution_id = i.id
            WHERE donator_id = %s ;
            '''

    cursor.execute(query, (user_id,))
    connection.commit()
    result = cursor.fetchall()

    print("institution_id , institution_name , date , value , currency , payment_method , frequency, institution_category, institution_description")
    for items in result:
        print(items)

    users_menu()


##########################################################################################################


def show_all_institutions():

    global institution_id
    global institution_website

    print("\n")
    print("Please find the list of all institutions in our database:\n")

    query = f'''
                            SELECT id , name , category , description
                            FROM institutions ;
                            '''

    cursor.execute(query)
    connection.commit()
    result = cursor.fetchall()

    print("ID , Name , Category , Description")
    for items in result:
        print(items)

    print("")
    print("****************** ALL INSTITUTIONS ******************")
    print("*                                                    *")
    print("* Type the Instituion ID to make a donation          *")
    print("* Type 'C' to see institutions per Category          *")
    print("* Type 'R' to Return to Users menu                   *")
    print("*                                                    *")
    print("******************************************************")

    while True:

        show_all_institutions_choice = input("\n> What do you wanna do? ")

        try:
            show_all_institutions_choice = int(show_all_institutions_choice)

        except ValueError:
            show_all_institutions_choice = show_all_institutions_choice.lower()

        if isinstance(show_all_institutions_choice, int):

            query = f'''
                            SELECT url
                            FROM institutions
                            WHERE id = %s 
                            LIMIT 1;
                            '''
            cursor.execute(query, (show_all_institutions_choice,))
            connection.commit()
            result = cursor.fetchone()
            url_found = result[0]

            if url_found:
                institution_id = show_all_institutions_choice
                institution_website = url_found
                perform_donation()
                break

        elif show_all_institutions_choice == "c":
            show_categories()
            break

        elif show_all_institutions_choice == "r":
            users_menu()
            break

        else:
            print("Invalid input. Try again.")
            continue



##########################################################################################################


def show_categories():

    global institution_id
    global institution_website


    query = f'''
                            SELECT DISTINCT(category)
                            FROM institutions ;
                            '''

    cursor.execute(query)
    connection.commit()
    categories = cursor.fetchall()

    category_dict = {idx: category[0] for idx, category in enumerate(categories, start=1)}

    for idx, category in category_dict.items():
        print(f"{idx}. {category}")

    cat_index = int(
        input("> Do you wanna see institutions in which category? Enter the category index as above: "))
    selected_category = category_dict[cat_index]

    query = f'''
                            SELECT id , name , category , description 
                            FROM institutions 
                            WHERE category = %s ;
                         '''

    cursor.execute(query, (selected_category,))
    connection.commit()
    result = cursor.fetchall()

    print("ID , Name , Category , Description")
    for items in result:
        print(items)

    print("")
    print("*************** INSTITUTIONS  CATEGORY ***************")
    print("*                                                    *")
    print("* Type the Instituion ID to make a donation          *")
    print("* Type 'A' to show All institutions per Category     *")
    print("* Type 'R' to Return to Users menu                   *")
    print("*                                                    *")
    print("******************************************************")

    while True:

        show_categories_choice = input("\n> What do you wanna do? ")

        try:
            show_categories_choice = int(show_categories_choice)

        except ValueError:
            show_categories_choice = show_categories_choice.lower()

        if isinstance(show_categories_choice, int):

            query = f'''
                                SELECT url
                                FROM institutions
                                WHERE id = %s 
                                LIMIT 1;
                                '''
            cursor.execute(query, (show_categories_choice,))
            connection.commit()
            result = cursor.fetchone()
            url_found = result[0]

            if url_found:
                institution_id = show_categories_choice
                institution_website = url_found
                perform_donation()
                break

        elif show_categories_choice == "a":
            show_all_institutions()
            break

        elif show_categories_choice == "r":
            users_menu()
            break

        else:
            print("Invalid input. Try again.")
            continue

##########################################################################################################


def perform_donation():

    global user_id
    global user_name
    global user_email
    global user_password

    global institution_id
    global institution_website

    value_donator_id = user_id
    value_institution_id = institution_id
    value_date = date.today()
    value_currency = input("> Enter in which currency do you want to donate: ")

    ''' For donation_value - Validation integer'''
    while True:
        try:
            donation_value = input("> Enter how much do you want to donate: ")
            value_value = int(donation_value)
            break

        except ValueError:
            print("Your input must contain only numeric characters. Please try again.")



    ''' For payment_method - from list'''
    payment_method_options = [ 'Credit Card' , 'Direct' , 'Bank Transfer' , 'BIT']
    while True:
        print("Select the payment method from the options below:")

        for index, value in enumerate(payment_method_options):
            print(f"Option {index}: {value}")

        try:
            input_method = input("> Please enter your option: ")
            option_selected = int(input_method)
            if option_selected < len(payment_method_options):
                value_payment_method = payment_method_options[option_selected]
                break
            else:
                print("\nInvalid option. Please try again.")

        except ValueError:
            print("\nYour input must be in the list of payment options. Please try again.")



    ''' For donation_frequency - from list'''
    donation_frequency_options = ['one-time gift' , 'monthly-gift']
    while True:
        print("Select what will be the donation frequency from the option below:")

        for index, value in enumerate(donation_frequency_options):
            print(f"Option {index}: {value}")

        try:
            input_frequency = input("> Please enter your option: ")
            frequency_selected = int(input_frequency)
            if frequency_selected < len(donation_frequency_options):
                value_frequency = donation_frequency_options[frequency_selected]
                break
            else:
                print("\nInvalid option. Please try again.")

        except ValueError:
            print("\nYour input must be in the list of payment options. Please try again.")


    query = f'''
            INSERT INTO donations (donator_id , institution_id , date , value , currency , payment_method , frequency) VALUES
            (%s , %s , %s , %s , %s , %s , %s) ;
    '''

    cursor.execute(query, (value_donator_id, value_institution_id, value_date, value_value , value_currency , value_payment_method , value_frequency))

    connection.commit()

    print("\nYour donation was registered in our database. We will follow up in the next few days to confirm if it was completed.")
    print(f"Please complete the donation on the institution website: {institution_website}")
    print("Thank you for Supporting Israel! We hope to see you again in the future!")


##########################################################################################################


def main():

    while True:

        global user_id
        global user_name
        global user_email
        global user_password

        global cursor
        global connection

        global initial_menu_choice

        initial_menu()

        if initial_menu_choice == 'i':
            sign_in_menu()
            break

        elif initial_menu_choice == 'u':
            sign_up_menu()
            break

        elif initial_menu_choice == 'e':
            break

        else:
            print("Invalid choice. Please try again.")
            continue


##########################################################################################################


main()

cursor.close()
connection.close()
