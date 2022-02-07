import lib.func as func
import time

def processCommand(text):
    args = func.splitArgs(text)
    if args[0].lower() == "get":
        if len(args) <= 1: return __invalid__()
        email, password, fiveStarStatus, tags = func.getAccount(args[1])
        func.sendTitle()
        print(f'ACCOUNT FOUND!')
        print(f'---')
        print(f'Email: {email}')
        print(f'Password: {password}')
        print(f'Five Star? {fiveStarStatus}')
        print(f'Tags: [{tags}]\n--')

        processSub("get", input(f'Enter sub-command (edit | file | remove | exit): '), [email, password, fiveStarStatus, tags])
        return "get"
    elif args[0].lower() == "search":
        if len(args) <= 1: return __invalid__()
        accounts = func.searchAccounts(args[1])
        func.sendTitle()
        if " " in accounts[0]: print(f'There are a total of 0 accounts that match your query!')
        else: print(f'There are a total of {len(accounts)} account(s) that match your query!')

        processSub("search", input(f'Enter sub-command (file | print | exit): '), accounts)
        return "search"
    elif args[0].lower() == "count":
        func.sendTitle()
        count = func.countAccounts(None)
        print(f'There are a total of {count} registered account(s)!')

        # no sub-commands for 'count'
        return "count"
    elif args[0].lower() == "list":
        func.sendTitle()
        accounts = func.listAccounts(None)
        if " " in accounts[0]: print(f'There are a total of 0 registered accounts!')
        else: print(f'There are a total of {len(accounts)} registered account(s)!')

        processSub("list", input(f'Enter sub-command (file | print | exit): '), accounts)
        return "list"
    elif args[0].lower() == "add":
        if len(args) <= 4: return __invalid__()
        func.sendTitle()
        fiveStarStatus = "No"
        if args[3].lower() == "1" or args[3].lower() == "true" or args[3].lower() == "yes": fiveStarStatus = "Yes"
        tags = args[4:]
        tags[0] = tags[0].replace("[", "")
        tags[-1] = tags[-1].replace("]", "")
        if len(args) == 4: func.addAccount(args[1], args[2], fiveStarStatus, [])
        else: func.addAccount(args[1], args[2], fiveStarStatus, tags)
        print(f'ACCOUNT ADDED!')
        print(f'---')
        print(f'Email: {args[1]}')
        print(f'Password: {args[2]}')
        print(f'Five Star? {args[3]}')
        if len(args) == 4: print(f'Tags: []\n--')
        else: print(f'Tags: {tags}\n--')

        if len(args) == 4: processSub("add", input(f'Enter sub-command (edit | file | remove | view | exit): '), [args[1], args[2], args[3], "[]"])
        else: processSub("add", input(f'Enter sub-command (edit | file | remove | view | exit): '), [args[1], args[2], args[3], tags])
        return "add"
    elif args[0].lower() == "remove":
        if len(args) <= 1: return __invalid__()
        func.sendTitle()
        text = input("Are you sure you want to remove the account? (Y/N) ")
        if text.lower() == "y":
            func.sendTitle()
            func.removeAccount(args[1])
            print(f'ACCOUNT REMOVED!')
            print(f'---')
            print(f'You have successfully deleted the details of the account \'{args[1]}\' from the database!')
        else:
            func.sendTitle()
            print(f'Action cancelled! Returning to the main menu in 3 seconds...')
            time.sleep(3)
        
        # no sub-commands for 'remove'
        return "remove"
    elif args[0].lower() == "editemail":
        if len(args) <= 2: return __invalid__()
        func.sendTitle()
        func.editAccountEmail(args[1], args[2])
        print(f'ACCOUNT EDITED!')
        print(f'---')
        print(f'You have changed the details of an account:')
        print(f'-')
        print(f'Previous Email: {args[1]}')
        print(f'New Email: {args[2]}')
        print(f'-')
        
        processSub("editemail", input(f'Enter sub-command (edit | remove | view | exit): '), [args[1]])
        return "editemail"
    elif args[0].lower() == "editpassword":
        if len(args) <= 2: return __invalid__()
        func.sendTitle()
        func.editAccountPassword(args[1], args[2])
        print(f'ACCOUNT EDITED!')
        print(f'---')
        print(f'You have changed the details of an account:')
        print(f'-')
        print(f'Email: {args[1]}')
        print(f'New Password: {args[2]}')
        print(f'-')
        
        processSub("editpassword", input(f'Enter sub-command (edit | remove | view | exit): '), [args[1]])
        return "editpassword"
    elif args[0].lower() == "setfivestar":
        if len(args) <= 2: return __invalid__()
        func.sendTitle()
        fiveStar = False
        if args[2].lower() == "1" or args[2].lower() == "true" or args[2].lower() == "yes": fiveStar = True
        func.editAccountFiveStarStatus(args[1], fiveStar)
        print(f'ACCOUNT EDITED!')
        print(f'---')
        print(f'You have changed the details of an account:')
        print(f'-')
        print(f'Email: {args[1]}')
        if fiveStar == True: print(f'Has Five Star? Yes')
        else: print(f'Has Five Star? No')
        print(f'-')
        
        processSub("setfivestar", input(f'Enter sub-command (edit | remove | view | exit): '), [args[1]])
        return "setfivestar"
    elif args[0].lower() == "addnewtags":
        if len(args) <= 2: return __invalid__()
        func.sendTitle()
        tags = args[2:]
        tags[0] = tags[0].replace("[", "")
        tags[-1] = tags[-1].replace("]", "")
        func.addNewAccountTags(args[1], tags)
        print(f'ACCOUNT EDITED!')
        print(f'---')
        print(f'You have changed the details of an account:')
        print(f'-')
        print(f'Email: {args[1]}')
        print(f'Tags: {tags}')
        print(f'-')
        
        processSub("addnewtags", input(f'Enter sub-command (edit | remove | view | exit): '), [args[1]])
        return "addnewtags"
    else:
        return "exit"

def processSub(origCmd : str, sub : str, args = None):
    if origCmd.lower() in ["count", "remove"]:
        input(f'Click ENTER to return to the main menu!')
        return True
    
    if sub == "view":
        if args == None: return __invalidSub__()
        if len(args) == 0: return __invalidSub__()
        if origCmd.lower() in ["get", "search", "list"]: return __noSub__()

        processCommand("get " + args[0])
        return True
    elif sub == "edit":
        if args == None: return __invalidSub__()
        if len(args) == 0: return __invalidSub__()
        if origCmd.lower() in ["search", "list"]: return __noSub__()

        func.sendTitle()
        print(f"EDITING '{args[0]}'")
        print(f'---')
        edit = input(f'What do you want to edit? (email, password, fivestar) ')

        if edit.lower() == "email": 
            edit = input(f'Enter new email address: ')
            processCommand(f'editEmail {args[0]} {edit}')
        elif edit.lower() == "password": 
            edit = input(f'Enter new password: ')
            processCommand(f'editPassword {args[0]} {edit}')
        elif edit.lower() == "fivestar": 
            edit = input(f'Enter new five star status: ')
            processCommand(f'setFiveStar {args[0]} {edit}')
        else: 
            return __noSub__()
        return True
    elif sub == "remove":
        if args == None: return __invalidSub__()
        if len(args) == 0: return __invalidSub__()
        if origCmd.lower() in ["search", "list"]: return __noSub__()

        processCommand(f"remove {args[0]}")
        return True
    elif sub == "print":
        if args == None: return __invalidSub__()
        if len(args) == 0: return __invalidSub__()
        if origCmd.lower() in ["get", "add", "editemail", "editpassword", "setfivestar", "addnewtags"]: return __noSub__()

        func.sendTitle()
        print(f'VIEWING ACCOUNTS')
        print(f'---')
        _ = True
        for acc in args:
            email, password, fiveStarStatus, tags = acc
            if _ == False: print(f'----------')
            print(f'Email: {email}')
            print(f'Password: {password}')
            print(f'Five Star? {fiveStarStatus}')
            print(f'Tags: [{tags}]')
            print(f'----------')
            _ = False
        return True
    elif sub == "file":
        if args == None: return __invalidSub__()
        if len(args) == 0: return __invalidSub__()
        if origCmd.lower() in ["editemail", "editpassword", "setfivestar", "addnewtags"]: return __noSub__()

        func.sendTitle()
        if origCmd.lower() in ["search", "list"]:
            f = open("account.txt", "w")
            for account in args:
                email, password, _, tags = account
                f.write(f'Email: {email}\n')
                f.write(f'Password: {password}\n')
                f.write(f'Tags: [{tags}]\n')
                f.write(f'----------\n')
            f.close()
        else:
            f = open("account.txt", "w")
            f.write(f'Email: {args[0]}\n')
            f.write(f'Password: {args[1]}\n')
            f.write(f'Tags: [{args[2]}]\n')
            f.close()
        print(f'Success! Account details were written to the \'account.txt\' file.')
        return True
    elif sub == "exit":
        return True
    else:
        return __noSub__()

def __invalid__():
    func.sendTitle()
    print(f'Invalid command usage! Please read the usage. Tool will return to the main menu in 3 seconds...')
    time.sleep(3)
    return None

def __invalidSub__():
    func.sendTitle()
    print(f'Invalid arguments! Should this continue to occur, create a bug report on Github with the command and sub-command you used.\nTool will return to the main menu in 3 seconds...')
    time.sleep(3)
    return False

def __noSub__():
    func.sendTitle()
    print(f'Invalid option! Tool will return to the main menu in 2 seconds...')
    time.sleep(2)
    return False