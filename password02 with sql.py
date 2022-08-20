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
welcome_message = '''Welcome!

Press 1 to: Add a new user
Press 2 to: Delete an user
Press 3 to: Generate a new password
Press 4 to: Retrieve a password
Press 5 to: Exit the program

Plase select one of the option above: '''


def pass_generation(length):
    pass_components = []
    # This block ensures that we have a minimum of 1 upper case, 1 lower case, 1 symbol, and 1 number
    pass_components.append(chr(random.randint(65, 90)))  #Uppercase
    pass_components.append(chr(random.randint(97, 112))) #Lowercase
    pass_components.append(chr(random.randint(33, 41)))  #Symbol
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
                pass_components.append(chr(random.randint(33, 41)))  #Symbol
            case 4:
                pass_components.append(chr(random.randint(48, 57)))  #Number
    random.shuffle(pass_components)
    return pass_components

def description_check(description, username):
    cursor.execute("SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='pass_schema' AND `TABLE_NAME`='userdb'")
    columns = cursor.fetchall()
    
    if ((description, ) in columns):
        cursor.execute("SELECT " + description + " FROM pass_schema.userdb WHERE username = '" + username + "';")
        password = cursor.fetchall()
        if password[0][0] == None:
            return False
        else:
            return True
    else:
        return False

def add_column(description):
    #Adds column into the database where the password will be stored
    
    try:    
        cursor.execute("ALTER TABLE pass_schema.userdb ADD COLUMN " + description + " VARCHAR(45) NULL AFTER `userpassword`;")
    except:
        print("Column Failure")

def add_password(user, description, password):
    try:
        query= ("UPDATE `pass_schema`.`userdb` SET " + description + " = '" + password + "' WHERE (`username` = '" + user + "');")
        cursor.execute(query)
        mydb.commit()
    except:
        print('Pass error')

def password_validation():
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

def main():
#    option = 0
#    password = ''
#    pass_length = 0
#    description = ''
    while(True):
        try:
            option = (int(input(welcome_message)))
            match option:
                case 1:
                    print()

                case 2:
                    print()

                case 3:
                    user = input("Please enter your username: ")
                    description = input('Please enter a description to identify the new password: ')
                    pass_length = password_validation()
                    if (description_check(description)):
                        #Here goes the code when the description added by the user already exists in the data base
                        go_back = input("The description you added already exists, do you wish to replace the existing password? (y/n): ")
                        if (go_back.lower == 'y'):
                            print()
                        else:
                            print("You will now return to the main menu. Press any key to continue")
                    else:
                        #Here goes the code when the description added by the user does not exist
                        
                        password = ''.join(pass_generation(pass_length))
                        add_column(description)
                        add_password(user, description, password)
                        print (password)
                    
                    
        except:
            system("CLS")
            print("Please enter a valid option")
        

main()
