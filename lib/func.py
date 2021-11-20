import os
import time
import sys
import sqlite3

passwordRequired = False

def setupDatabase():
    DB_NAME = 'database'
    db_path = os.path.join(os.path.abspath(os.getcwd()), DB_NAME + ".db")
    db = sqlite3.connect(db_path)
    db_cursor = db.cursor()
    db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS registered (
        email TEXT PRIMARY_KEY,
        password TEXT,
        fiveStar INTEGER,
        tags TEXT
    )
    """)
    return db, db_cursor

db, db_cursor = setupDatabase()

def encrypt(s):
    newString = ""
    for l in s:
        newString = newString + str(ord(l) + 21) + "-"
    newString = newString[:-1]
    return newString

def decrypt(s):
    decryptedString = ""
    for l in s.split("-"):
        decryptedString = decryptedString + chr(int(l) - 21)
    return decryptedString

def splitArgs(inp):
    if inp == "": return [""]
    args = inp.split(" ")
    return args

def sendTitle():
    os.system(f'cmd /c "cls')
    print(f'GENSHIN ACCOUNT DATABASE')
    print(f'-----------------------------')

def sendStartingText():
    sendTitle()
    print(f'Select an option:')
    print(f'  - 1 = Find Account')
    print(f'  - 2 = Management Mode')
    print(f'  - 3 = Exit')
    print(f'-----------')

    value = input(" > ")
    return value

def sendAccountFinderText():
    sendTitle()
    print(f'Please input an action.')
    print(f'  - get [email] | Get an account directly by it\'s registered email.')
    print(f'  - search [tag] | Search accounts by character.')
    print(f'  - count | Get a count of the total registered accounts.')
    print(f'  - list | Get a list of all registered accounts.')
    print(f'  - exit | Go back to the main screen.')
    print(f'-----------')

    value = input(" > ")
    return value

def sendAccountManagementText():
    sendTitle()
    if passwordRequired == True:
        password = input("Enter password: ")
        if not password == decrypt("124-122-131-136-125-126-131-86-89-78-77-78"):
            sendTitle()
            print(f'Incorrect password. Tool will now reload.')
            time.sleep(3)
            reloadTool()
        sendTitle()
    print(f'Please input an action.')
    print(f'  - add [email] [password] [fiveStar] ([tags]) | Add a new account to the database.')
    print(f'  - remove [email] | Remove an account from the database.')
    print(f'  - editEmail [currentEmail] [newEmail] | Change the email of an account.')
    print(f'  - editPassword [email] [newPassword] | Change the password of an account.')
    print(f'  - editFiveStar [email] [hasFiveStar] | Note that an account is in posession of a 5 star item or character.')
    print(f'  - addNewTags [email] [[tags]] | Add a new list of tags to an account.')
    print(f'  - exit | Go back to the main screen.')
    print(f'-----------')

    value = input(" > ")
    return value

def reloadTool():
    os.startfile("run.py")
    sys.exit()

def exitTool():
    exit()

# -------------------------------------- #
#             ACCOUNT FINDER             #
# -------------------------------------- # 

def getAccount(email):
    db_cursor.execute("SELECT * FROM registered WHERE email=?", (email,))
    response = db_cursor.fetchone()
    if not response:
        return ["Not found!", "", 0, ""]
    return response

def searchAccounts(tag):
    toReturn = []
    db_cursor.execute("SELECT * FROM registered")
    response = db_cursor.fetchall()
    if not response:
        toReturn.append(["Not found!", "", 0, ""])
        return toReturn
    for account in response:
        tags = account[3]
        for tag1 in tags.split(" "):
            if tag.lower() == tag1.lower(): toReturn.append(account)
    return toReturn

def countAccounts():
    db_cursor.execute("SELECT COUNT(*) FROM registered")
    response = db_cursor.fetchone()
    return int(response[0])

def listAccounts():
    db_cursor.execute("SELECT * FROM registered")
    response = db_cursor.fetchall()
    if not response:
        return [["Not found!", "", 0, ""]]
    return response

# -------------------------------------- #
#           ACCOUNT MANAGEMENT           #
# -------------------------------------- # 

def addAccount(email, password, hasFiveStar, tags):
    tagsCondensed = ""
    for tag in tags:
        tagsCondensed = tagsCondensed + tag + " "
    if not tagsCondensed == "": tagsCondensed = tagsCondensed[:-1]
    db_cursor.execute("INSERT INTO registered VALUES (?, ?, ?, ?)", (email, password, hasFiveStar, tagsCondensed,))
    db.commit()

def removeAccount(email):
    db_cursor.execute("SELECT * FROM registered WHERE email=?", (email,))
    response = db_cursor.fetchone()
    if not response:
        return
    db_cursor.execute("DELETE FROM registered WHERE email=?", (email,))
    db.commit()

def editAccountEmail(currentEmail, newEmail):
    db_cursor.execute("SELECT * FROM registered WHERE email=?", (currentEmail,))
    response = db_cursor.fetchone()
    if not response:
        return
    temp, password, fiveStar, tags = response
    db_cursor.execute("INSERT INTO registered VALUES (?, ?, ?, ?)", (newEmail, password, fiveStar, tags,))
    db_cursor.execute("DELETE FROM registered WHERE email=?", (currentEmail,))
    db.commit()

def editAccountPassword(email, password):
    db_cursor.execute("SELECT * FROM registered WHERE email=?", (email,))
    response = db_cursor.fetchone()
    if not response:
        return
    db_cursor.execute("UPDATE registered SET password=? WHERE email=?", (password, email,))
    db.commit()

def editAccountFiveStarStatus(email, hasFiveStar):
    db_cursor.execute("SELECT * FROM registered WHERE email=?", (email,))
    response = db_cursor.fetchone()
    if not response:
        return
    db_cursor.execute("UPDATE registered SET fiveStar=? WHERE email=?", (hasFiveStar, email,))
    db.commit()

def addNewAccountTags(email, tags):
    tagsCondensed = ""
    for tag in tags:
        tagsCondensed = tagsCondensed + tag + " "
    tagsCondensed = tagsCondensed[:-1]
    db_cursor.execute("SELECT * FROM registered WHERE email=?", (email,))
    response = db_cursor.fetchone()
    if not response:
        return
    email, password, fiveStar, oldTags = response
    if not oldTags == "":
        tagsCondensed = oldTags + " " + tagsCondensed
    db_cursor.execute("UPDATE registered SET tags=? WHERE email=?", (tagsCondensed, email,))
    db.commit()