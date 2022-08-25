from ast import AsyncFunctionDef
import random
from os import system
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root123",
  database="pass_schema"
)

cursor = mydb.cursor()



def pass_generation(length):
    pass_components = []
    # This block ensures that we have a minimum of 1 upper case, 1 lower case, 1 symbol, and 1 number
    pass_components.append(chr(random.randint(65, 90)))  #Uppercase
    pass_components.append(chr(random.randint(97, 112))) #Lowercase
    pass_components.append(chr(random.choice([numb for numb in range(33,41) if numb not in [34, 39]]))) #Symbol
    pass_components.append(chr(random.randint(48, 57)))  #Number
    # Fill the rest of the list with random components
    for i in range(length - 4):
        character = random.randint(1 , 4)
        match character:
            case 1 :
                pass_components.append(chr(random.randint(65, 90)))  #Uppercase
            case 2:
                pass_components.append(chr(random.randint(97, 112))) #Lowercase
            case 3:
                pass_components.append(chr(random.choice([numb for numb in range(33,41) if numb not in [34, 39]]))) #Symbol
            case 4:
                pass_components.append(chr(random.randint(48, 57)))  #Number
    random.shuffle(pass_components)
    return pass_components

def description_check(description, username):
    #This function will check if the description added by the user already exists in the database.
    #If the description doesn't exist, we call add_column to add said description as a column in the database, then we call add_password to add the newly generated password into the database.
    #If the description does exist, we call existing_password_check to verify if the password for said description exists or not.
    cursor.execute("SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='pass_schema' AND `TABLE_NAME`='userdb'")
    columns = cursor.fetchall()
    if ((description, ) in columns):
        return existing_password_check(description, username)
    else:
        return False

def existing_password_check(description, username):
    #This function will check if the description entered by the user already has an existing password.
    #We perform a SELECT query to retrieve the value stored in the database column that matches the description.
    #If the value is None we know the user has no saved password for said description. We will generate a new password and update the column in the database 
    #If the value is other than None, then we tell the user to use the "Update existing password" option in the main menu
    cursor.execute("SELECT " + description + " FROM pass_schema.userdb WHERE username = '" + username + "';")
    password = cursor.fetchall()
    if password[0][0] != None:
        return True

def add_column(description):
    #Adds column into the database where the password will be stored
    try:    
        cursor.execute("ALTER TABLE pass_schema.userdb ADD COLUMN " + description + " VARCHAR(45) NULL AFTER `userpassword`;")
    except:
        print("Column Failure")

def add_password(user, description, password):
    #Adds a password 
    #Following failing example: UPDATE `pass_schema`.`userdb` SET test2 = '0l'jK161f' WHERE (`username` = 'Alondra');
    try:
        query= ("UPDATE `pass_schema`.`userdb` SET " + description + " = '" + password + "' WHERE (`username` = '" + user + "');")
        cursor.execute(query)
        mydb.commit()
        print ('A password for', description, 'was created. Password:', password)
    except:
        print('There was an error when creating your password, please try again')

def password_validation():
    #This function will check if the length added by the user is valid
    while (True):
            try:
                pass_length = int(input('Enter the desired password length (at least 8 characters, maximum 24 characters): '))
                if (pass_length < 8 or pass_length > 24):
                    system('CLS')
                    print('Invalid length, please enter length from 8 to 24 characters')
                    continue
                return(pass_length)
            except:
                system('CLS')
                print('Please enter a valid, positive integer')

def user_authentication(user, user_password):
    #SELECT username FROM pass_schema.userdb WHERE username = 'Dani';
    cursor.execute("SELECT username, userpassword FROM pass_schema.userdb WHERE username = '" + user + "'")
    user_credentials = cursor.fetchall()
    if (not user_credentials):
      return False
    elif (user_password != user_credentials[0][1]):
      return False
    return True  

def retrieve_credentials(username):
  #This block of code will generate a list with all available columns
  cursor.execute("SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='pass_schema' AND `TABLE_NAME`='userdb'")
  columns = cursor.fetchall()
  del columns[0:2]
  descriptions = [item for t in columns for item in t]
  #This block of code will generate a list with all available passwords
  cursor.execute("SELECT * FROM pass_schema.userdb WHERE username = '" + username + "'")
  values = cursor.fetchall()
  passwords = [password for i in values for password in i]
  del passwords [0:2]
  #The dict and zip methods are used to create a dictionary, where the description will be the key, and the password will be the value
  user_credentials = dict(zip(descriptions, passwords))
  return user_credentials

def main():
    #User login
    user = input("Please enter your username: ")
    user_password = input('Enter your password: ')
    user_exists = user_authentication(user, user_password)
    welcome_message = '''
Press 1 to: Add a new user
Press 2 to: Delete an user
Press 3 to: Generate a new password
Press 4 to: Retrieve a password
Press 5 to: Exit the program

Plase select one of the option above: '''
    if user_exists:
        while(True):
        #try:
            system('CLS')
            option = (int(input(welcome_message)))
            match option:
                case 1:
                    print()

                case 2:
                    print()

                case 3:
                    system('CLS')
                    print("You are now generating a new password")
                    description = input('Enter a description to identify the new password: ')
                    if (description_check(description, user) is True):
                        cancel = input("A password for " + description + " already exists.\nDo you wish to update your password? (y/n): ")
                        if cancel.lower() == 'n':
                            input("You will now return to the main menu. Please press Enter to continue ")
                            continue
                    elif (description_check(description, user) is False):
                        add_column(description)                        
                    pass_length = password_validation()
                    password = ''.join(pass_generation(pass_length))
                    add_password(user, description, password)
                    
                    input('Press Enter to return to the main menu')
                case 4:
                    system('CLS')
                    print("You are now retrieving a password")
                    user_credentials = retrieve_credentials(user)
                    for descriptions in user_credentials:
                        print("[" + descriptions + "]", end = " ")
                    description_request = input("\nWhich password do you wish to retrieve?: ")
                    print(user_credentials.get(description_request))
                    input()
                    
        #except:
        #    system("CLS")
        #    print("Please enter a valid option")
    else:
        print("Incorrect username or password")
    

main()
