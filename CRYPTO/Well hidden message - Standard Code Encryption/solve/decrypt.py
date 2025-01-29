import os

with open("secret.txt", 'r', encoding='ascii') as f:
    encrypted_text = f.read()

decrypted_text = []

for i, char in enumerate(encrypted_text):
    decrypted_char = chr((ord(char) - i) % 128) 
    decrypted_text.append(decrypted_char)

with open("decrypt.txt", 'w', encoding='utf-8') as f:
    f.write(''.join(decrypted_text))