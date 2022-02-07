import time
import traceback
import lib.func as func
import lib.commandHandler as handler

# Initialise variables.
text = ""

# Create the account.txt file if it doesn't already exist.
file = func.createAccountFile()

# run() function, called to start the program.
def run(option = None):
    if option == None:
        func.startingText()
        option = func.sendStartingText()
    elif option == "noani":
        option = func.sendStartingText()
    
    if option == "1" or option.lower() == "find account":
        text = func.sendAccountFinderText()
        cmd = handler.processCommand(text)
        if not cmd == "exit": input(f'--\nClick ENTER to return to the main menu!')
    elif option == "2" or option.lower() == "management mode":
        text = func.sendAccountManagementText()
        cmd = handler.processCommand(text)
        if not cmd == "exit": input(f'--\nClick ENTER to return to the main menu!')
    elif option == "3" or option.lower() == "exit":
        func.exitTool()
    elif option.lower() == "adm-encrypt":
        func.sendTitle()
        message = input(f'Enter message to encrypt: ')
        func.sendTitle()
        print(f'Your encrypted message is: {func.encrypt(message)}')
        print(f"Copy and paste this string into the 'func.py' file under the 'password' variable to change the password.")
        input(f'--\nClick ENTER to return to the main menu!')
    elif option.lower() == "adm-decrypt":
        func.sendTitle()
        message = input(f'Enter message to decrypt: ')
        func.sendTitle()
        print(f'Your decrypted message is: {func.decrypt(message)}')
        input(f'--\nClick ENTER to return to the main menu!')
    elif option.lower() == "adm-reload":
        func.reloadTool()
    else:
        func.sendTitle()
        print(f'Invalid input! Reloading in 3 seconds...')
        time.sleep(3)

if __name__ == "__main__":
    try:
        run() # initial call, show startup animation
        while True:
            run("noani")
    except Exception as e:
        func.sendTitle()
        print(f'An error occurred that stopped the process from running further.')
        print(f'The error has been printed below.')
        print(f'\nError - {e}\n')
        traceback.print_exc()
        input(f"\nPress ENTER to exit the tool.")