import random
password = ''
pass_length = int(input('Enter the desired password length: '))


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
        if (character == 1):
            pass_components.append(chr(random.randint(65, 90)))  #Uppercase
        elif (character == 2):
            pass_components.append(chr(random.randint(97, 112))) #Lowercase
        elif (character == 3):
            pass_components.append(chr(random.randint(33, 41)))  #Symbol
        else:
            pass_components.append(chr(random.randint(48, 57)))  #Number
    random.shuffle(pass_components)
    return pass_components

password = ''.join(pass_generation(pass_length))
print (password)
print (len(password))