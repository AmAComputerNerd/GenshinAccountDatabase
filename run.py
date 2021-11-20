import os
import time
import sys
import traceback
import sqlite3
import lib.func as func

db, db_cursor = func.setupDatabase()

text = ""
print("""
  /$$$$$$                                /$$       /$$                          
 /$$__  $$                              | $$      |__/                          
| $$  \__/  /$$$$$$  /$$$$$$$   /$$$$$$$| $$$$$$$  /$$ /$$$$$$$                 
| $$ /$$$$ /$$__  $$| $$__  $$ /$$_____/| $$__  $$| $$| $$__  $$                
| $$|_  $$| $$$$$$$$| $$  \ $$|  $$$$$$ | $$  \ $$| $$| $$  \ $$                
| $$  \ $$| $$_____/| $$  | $$ \____  $$| $$  | $$| $$| $$  | $$                
|  $$$$$$/|  $$$$$$$| $$  | $$ /$$$$$$$/| $$  | $$| $$| $$  | $$                
 \______/  \_______/|__/  |__/|_______/ |__/  |__/|__/|__/  |__/                



  /$$$$$$                                                      /$$              
 /$$__  $$                                                    | $$              
| $$  \ $$  /$$$$$$$  /$$$$$$$  /$$$$$$  /$$   /$$ /$$$$$$$  /$$$$$$            
| $$$$$$$$ /$$_____/ /$$_____/ /$$__  $$| $$  | $$| $$__  $$|_  $$_/            
| $$__  $$| $$      | $$      | $$  \ $$| $$  | $$| $$  \ $$  | $$              
| $$  | $$| $$      | $$      | $$  | $$| $$  | $$| $$  | $$  | $$ /$$          
| $$  | $$|  $$$$$$$|  $$$$$$$|  $$$$$$/|  $$$$$$/| $$  | $$  |  $$$$/          
|__/  |__/ \_______/ \_______/ \______/  \______/ |__/  |__/   \___/            
                                                                                
                                                                                
                                                                                
 /$$$$$$$              /$$               /$$                                    
| $$__  $$            | $$              | $$                                    
| $$  \ $$  /$$$$$$  /$$$$$$    /$$$$$$ | $$$$$$$   /$$$$$$   /$$$$$$$  /$$$$$$ 
| $$  | $$ |____  $$|_  $$_/   |____  $$| $$__  $$ |____  $$ /$$_____/ /$$__  $$
| $$  | $$  /$$$$$$$  | $$      /$$$$$$$| $$  \ $$  /$$$$$$$|  $$$$$$ | $$$$$$$$
| $$  | $$ /$$__  $$  | $$ /$$ /$$__  $$| $$  | $$ /$$__  $$ \____  $$| $$_____/
| $$$$$$$/|  $$$$$$$  |  $$$$/|  $$$$$$$| $$$$$$$/|  $$$$$$$ /$$$$$$$/|  $$$$$$$
|_______/  \_______/   \___/   \_______/|_______/  \_______/|_______/  \_______/
                                                                                  
----------------------------------------------------------------------------------
By SimplyAmazing | Database Application\n
Loading.... -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
""")

# Initialize variables.
running = True
time.sleep(3)
f = None

# Create the account .txt file if it doesn't already exist.
try:
    f = open("account.txt", "x")
except Exception as e:
    pass

# Start app loop.
try:
    while(running):
        text = func.sendStartingText() # Sends the MainMenu help menu.
        if text == "1" or text.lower() == "find account": # Enter to FindMode (no administrative commands, just account finding).
            text = func.sendAccountFinderText() # Sends the AccountFinder help menu.
            args = func.splitArgs(text) # Splits the args from the help menu so they can be determined easier.
            if args[0].lower() == "get":
                # Args check.
                if(len(args) <= 1):
                    func.sendTitle() # Clears the command prompt and sends a title.
                    print(f'Invalid command usage! Please read the usage. Tool will return to the main menu in 3 seconds...')
                    time.sleep(3)
                    continue
                # Get details and print them.
                email, password, fiveStar, tags = func.getAccount(args[1])
                func.sendTitle()
                print(f'ACCOUNT FOUND!')
                print(f'---')
                fiveStarStatus = "No"
                if fiveStar == 1: fiveStarStatus = "Yes"
                print(f'Email: {email}')
                print(f'Password: {password}')
                print(f'Five Star? {fiveStarStatus}')
                print(f'Tags: [{tags}]\n')
                # Sub-command input
                sub = input(f'Enter sub-command (file | delete | exit): ')
                if sub.lower() == "file":
                    # Open the 'account.txt' file and overwrite it with the account information.
                    f = open("account.txt", "w")
                    f.write(f'Email: {email}\n')
                    f.write(f'Password: {password}\n')
                    f.write(f'Tags: [{tags}]\n')
                    f.close()
                    func.sendTitle()
                    print(f'Success! Returning to the main menu in 3 seconds...')
                    time.sleep(3)
                    continue
                elif sub.lower() == "delete":
                    # Asks for confirmation before deleting the account.
                    func.sendTitle()
                    resp = input(f'Are you sure you want to remove this account? ')
                    if resp.lower() == "y" or resp.lower() == "yes":
                        func.sendTitle()
                        func.removeAccount(args[1])
                        print(f'ACCOUNT REMOVED!')
                        print(f'---')
                        print(f'You have successfully deleted the details of the account \'{email}\' from the database!\n')
                        input(f'Click ENTER to return to the main menu!')
                    else:
                        func.sendTitle()
                        print(f'Action cancelled! Returning to the main menu in 3 seconds...')
                        time.sleep(3)
                        continue
                else:
                    # Simply returns to the main menu.
                    continue
            elif args[0].lower() == "search":
                if(len(args) <= 1):
                    func.sendTitle()
                    print(f'Invalid command usage! Please read the usage. Tool will return to the main menu in 3 seconds...')
                    time.sleep(3)
                    continue
                # Search all the accounts to find ones with a matching tag to that of the user's input.
                func.sendTitle()
                accounts = func.searchAccounts(args[1])
                first = True
                count = 0
                for account in accounts:
                    count = count + 1
                print(f'There is {count} accounts total that fit your search!')
                sub = input(f'Enter sub-command (print | file | exit): ')
                if sub.lower() == "print":
                    # Prints the list of accounts to the command prompt window seperated by spacing.
                    func.sendTitle()
                    for account in accounts:
                        email, password, fiveStar, tags = account
                        if not first == True:
                            print(f'----------')
                        fiveStarStatus = ""
                        if fiveStar == 1: fiveStarStatus = "Yes"
                        else: fiveStarStatus = "No"
                        print(f'Email: {email}')
                        print(f'Password: {password}')
                        print(f'Five Star? {fiveStarStatus}')
                        print(f'Tags: [{tags}]')
                        print(f'----------')
                    input(f'Click ENTER to return to the main menu!')
                elif sub.lower() == "file":
                    # Open the 'account.txt' file and overwrite it with the list of accounts.
                    f = open("account.txt", "w")
                    for account in accounts:
                        email, password, fiveStar, tags = account
                        f.write(f'Email: {email}\n')
                        f.write(f'Password: {password}\n')
                        f.write(f'Tags: [{tags}]\n')
                        f.write(f'----------\n')
                    f.close()
                    func.sendTitle()
                    print(f'Success! Returning to the main menu in 3 seconds...')
                    time.sleep(3)
                    continue
                else:
                    continue
            elif args[0].lower() == "count":
                # Send a total count of registered accounts.
                func.sendTitle()
                count = func.countAccounts()
                print(f'There are a total of {count} registered accounts!\n')
                input(f'Click ENTER to return to the main menu!')
            elif args[0].lower() == "list":
                # List every single registered account to the console.
                func.sendTitle()
                sub = input(f'Enter sub-command (print | file | cancel): ')
                response = func.listAccounts()
                if sub.lower() == "print":
                    func.sendTitle()
                    first = True
                    for account in response:
                        email, password, fiveStar, tags = account
                        if not first == True:
                            print(f'----------')
                        fiveStarStatus = ""
                        if fiveStar == 1: fiveStarStatus = "Yes"
                        else: fiveStarStatus = "No"
                        print(f'Email: {email}')
                        print(f'Password: {password}')
                        print(f'Five Star? {fiveStarStatus}')
                        print(f'Tags: [{tags}]')
                        print(f'----------')
                    input(f'Click ENTER to return to the main menu!')
                elif sub.lower() == "file":
                    f = open("account.txt", "w")
                    for account in response:
                        email, password, fiveStar, tags = response
                        f.write(f'Email: {email}\n')
                        f.write(f'Password: {password}\n')
                        f.write(f'Tags: [{tags}]\n')
                        f.write(f'----------\n')
                    func.sendTitle()
                    print(f'Success! Returning to the main menu in 3 seconds...')
                    time.sleep(3)
                    continue
                else:
                    continue
            else:
                pass
        elif text == "2" or text.lower() == "management mode": # Enter to ManagementMode (all the administrative functions).
            text = func.sendAccountManagementText() # Sends the AccountManagement help menu.
            args = func.splitArgs(text)
            if args[0].lower() == "add":
                if(len(args) <= 4):
                    func.sendTitle()
                    print(f'Invalid command usage! Please read the usage. Tool will return to the main menu in 3 seconds...')
                    time.sleep(3)
                    continue
                # Add a new account to the database.
                func.sendTitle()
                fiveStar = 0
                if args[3].lower() == "1" or args[3].lower() == "true" or args[3].lower() == "yes": fiveStar = 1
                tags = args[4:]
                tags[0] = tags[0].replace("[", "")
                tags[-1] = tags[-1].replace("]", "")
                if len(args) == 4: func.addAccount(args[1], args[2], fiveStar, [])
                else: func.addAccount(args[1], args[2], args[3], tags)
                print(f'ACCOUNT ADDED!')
                print(f'---')
                print(f'Email: {args[1]}')
                print(f'Password: {args[2]}')
                print(f'Five Star? {args[3]}')
                if len(args) == 4: print(f'Tags: []\n')
                else: print(f'Tags: {tags}\n')
                input(f'Click ENTER to return to the main menu!')
            elif args[0].lower() == "remove":
                if(len(args) <= 1):
                    func.sendTitle()
                    print(f'Invalid command usage! Please read the usage. Tool will return to the main menu in 3 seconds...')
                    time.sleep(3)
                    continue
                # Attempt to remove an account from the database.
                func.sendTitle()
                resp = input(f'Are you sure you want to remove this account? ')
                if resp.lower() == "y" or resp.lower() == "yes":
                    func.sendTitle()
                    func.removeAccount(args[1])
                    print(f'ACCOUNT REMOVED!')
                    print(f'---')
                    print(f'You have successfully deleted the details of the account \'{args[1]}\' from the database!\n')
                    input(f'Click ENTER to return to the main menu!')
                else:
                    func.sendTitle()
                    print(f'Action cancelled! Returning to the main menu in 3 seconds...')
                    time.sleep(3)
                    continue
            elif args[0].lower() == "editemail":
                if(len(args) <= 2):
                    func.sendTitle()
                    print(f'Invalid command usage! Please read the usage. Tool will return to the main menu in 3 seconds...')
                    time.sleep(3)
                    continue
                # Change the email of an already registed account.
                func.sendTitle()
                func.editAccountEmail(args[1], args[2])
                print(f'ACCOUNT EDITED!')
                print(f'---')
                print(f'You have changed the details of an account:')
                print(f'Previous Email: {args[1]}')
                print(f'New Email: {args[2]}\n')
                input(f'Click ENTER to return to the main menu!')
            elif args[0].lower() == "editpassword":
                if(len(args) <= 2):
                    func.sendTitle()
                    print(f'Invalid command usage! Please read the usage. Tool will return to the main menu in 3 seconds...')
                    time.sleep(3)
                    continue
                # Change the password of a registered account.
                func.sendTitle()
                func.editAccountPassword(args[1], args[2])
                print(f'ACCOUNT EDITED!')
                print(f'---')
                print(f'You have changed the details of an account:')
                print(f'Account Email: {args[1]}')
                print(f'New Password: {args[2]}\n')
                input(f'Click ENTER to return to the main menu!')
            elif args[0].lower() == "editfivestar":
                if(len(args) <= 2):
                    func.sendTitle()
                    print(f'Invalid command usage! Please read the usage. Tool will return to the main menu in 3 seconds...')
                    time.sleep(3)
                    continue
                # Change whether or not a registered account shows up as having a five star.
                func.sendTitle()
                fiveStar = 0
                if args[2].lower() == "1" or args[2].lower() == "true" or args[2].lower() == "yes": fiveStar = 1
                func.editAccountFiveStarStatus(args[1], fiveStar)
                print(f'ACCOUNT EDITED!')
                print(f'---')
                print(f'You have changed the details of an account:')
                print(f'Account Email: {args[1]}')
                if fiveStar == 1: print(f'Has Five Star? Yes\n')
                else: print(f'Has Five Star? No\n')
                input(f'Click ENTER to return to the main menu!')
            elif args[0].lower() == "addnewtags":
                if(len(args) <= 2):
                    func.sendTitle()
                    print(f'Invalid command usage! Please read the usage. Tool will return to the main menu in 3 seconds...')
                    time.sleep(3)
                    continue
                # Add new tags to a registered account, typically used after pre-registering an account and using the wishes you get at AR 5.
                func.sendTitle()
                tags = args[2:]
                tags[0] = tags[0].replace("[", "")
                tags[-1] = tags[-1].replace("]", "")
                func.addNewAccountTags(args[1], tags)
                print(f'ACCOUNT EDITED!')
                print(f'---')
                print(f'You have changed the details of an account:')
                print(f'Account Email: {args[1]}')
                print(f'Added Tags: {tags}\n')
                input(f'Click ENTER to return to the main menu!')
        else: 
            # Simply exit the tool as that is the only other argument.
            func.exitTool()
except Exception as e:
    func.sendTitle()
    print(f'An error occurred that stopped the process from running further.')
    print(f'The error has been printed below.')
    print(f'\nError - {e}')
    traceback.print_exc()
    input(f"Press ENTER to exit the tool.")