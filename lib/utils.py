import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def get_input(question, previousLines = [], minimum = None, maximum = None):
    op = None
    clear_screen()

    while op == None or (minimum != None and op < minimum) or (maximum != None and op > maximum):
        for line in previousLines:
            print(line)
        
        if len(previousLines) > 0:
            print("")
        
        try:
            op = int(input(question))
            clear_screen()
        
        except ValueError:
            clear_screen()
            print("Invalid input, please try again.\n\n")
            op = None

    return op