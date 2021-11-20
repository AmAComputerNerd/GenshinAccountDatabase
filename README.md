# GenshinAccountDatabase
My horribly formatted and coded version of a database tool to store reroll accounts for Genshin Impact.

--------------------

**Note:** This file is meant to be run DIRECTLY and not through command prompt. It can be ran through command prompt, but in cases where the program needs to reload it will end up opening a new python window instead of just restarting within the command prompt.

--------------------

## More important things:

- **Tags:** When working with tags (except when using the `search` command), make sure you surround the tags in square brackets ([]) and separate each one by a space. This also means that these tags can not contain spaces. (**e.g.** *add randomemail@gmail.com password no [Noelle HuTao RaidenShogun]* adds an account with the tags `Noelle`, `HuTao`, and `RaidenShogun`.
- **Random features:** I added a password mode for Management Mode. If you want to use it, simply open the `func.py` file underneath the `lib` folder and change the boolean `passwordRequired = False` to `passwordRequired = True`. Furthermore, I also made an encryption thingy of sorts to make it harder to just find the password by opening the python file. If you want to change the default password (`genshinAD989`), you will need to open the `encryptTool.py` file, enter your desired password and copy it's output into the `password = ""` area in `func.py` inside the quotation marks.
