from lib.func import encrypt, decrypt

message = input(f'Input message to encrypt: ')
print(f'Your encrypted message is: {encrypt(message)}\n')
input(f'Click ENTER to close this tool.')