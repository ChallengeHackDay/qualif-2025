import socket
import threading
import sys
import time
from random import *
import base64
import datetime
import hashlib
import os
import dotenv
from deep_translator import GoogleTranslator as Translator


dotenv.load_dotenv()

_HOST = os.getenv('HOST')
_PORT = int(os.getenv('PORT'))
_MAX_THREADS = int(os.getenv('MAX_THREADS'))
active_threads = []
_FLAG_1 = os.getenv('FLAG_1')
_FLAG_2 = os.getenv('FLAG_2')
_FLAG_3 = os.getenv('FLAG_3')

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((_HOST, _PORT))
server_socket.listen()

print(f"Server is listening on port {_PORT}")


def close_socket(client_socket, client_address):
    client_socket.send(b"See you next time!\n")
    client_socket.shutdown(socket.SHUT_RDWR)
    client_socket.close()
    print(f"Connection with {client_address[0]}:{client_address[1]} closed")


def close_socket_timeout(client_socket, client_address):
    client_socket.send(b"... guess you don't want to answer me ... \n")
    close_socket(client_socket, client_address)

# --------------------------------------------------------------------------------

def start_chall(client_socket):
    client_socket.send(b"I'm feeling so lonely in this dead city...\nSince this industrial revolution, no one has come to talk to me...\nIf only there was someone to talk to...\nOH wait, YOU ... YES YOU!\n")
    client_socket.send(b"Would you care to spend some time with me ...?\n")

# --------------------------------------------------------------------------------

def client_confirmation(client_socket, client_address):
    try:
        data_recv = client_socket.recv(50)
        output = str(data_recv, "utf-8")

        if "yes" in output:
            client_socket.send(b"Excellent, so we can start talking!\n")
            return
        close_socket(client_socket, client_address)
    except TimeoutError:
        close_socket_timeout(client_socket, client_address)


def question1(client_socket, client_address, prev_answer):
    bot_names = ["Zebulon Mavromichali Parsons", "Zephaniah Lancelot Stillingfleet", "Archibald Buford Palmer", "Dionysia Anastasia Powers", "Hope Rosalind Bray", "Ermelinde Parthena Lewis", "Patrick Marcellus Playfoot", "Thodeoric Josephus Canning", "Ezekiel Gearwright", "Vesper Cogsworth", "Arabella Etheridge", "Thaddeus Ironclad", "Lydia Steamwell", "Montague Brassington", "Cassandra Clockspire", "Felix Emberforge", "Octavia Gaslight", "Phineas Tinkerbane"]
    bot_name = bot_names[randint(0, len(bot_names)-1)]
    client_socket.send(b"Starting with the basics, the name! Mine is " + bytes(bot_name, 'utf-8') + b"\nWhat's yours?\n")
    try:
        data_recv = client_socket.recv(100)
        output = str(data_recv, "utf-8").strip()
        prev_answer.append(output)
        client_socket.send(b"Nice to meet you " + bytes(output, 'utf-8') + b"!\n")
    except TimeoutError:
        close_socket_timeout(client_socket, client_address)
    return bot_name


def question2(client_socket, client_address, prev_answer):
    units = [b"Celsius", b"Fahrenheit", b"Kelvin"]
    answer_ranges = [(900, 940), (1650, 1720), (1170, 1210)]
    choice = randint(0, 2)
    client_socket.send(b"What's the fusion temperature of brass? Give it to me in " + units[choice] + b" and strip off decimals\n")
    try:
        data_recv = client_socket.recv(50)
        output = str(data_recv, "utf-8").strip().replace(" ", "")
        prev_answer.append(output)
        if output.isdigit() and answer_ranges[choice][0] <= int(output) <= answer_ranges[choice][1]:
            client_socket.send(b"Nice, you're good in physics!\n")
            return
        close_socket(client_socket, client_address)
    except TimeoutError:
        close_socket_timeout(client_socket, client_address)
    except Exception as e:
        print(e)


def question3(client_socket, client_address, prev_answer):
    trains = [b"vapor train", b"diesel train", b"electric train", b"magnetic suspension train"]
    answer = [("1804",), ("1912", "1923", "1925"), ("1879", "1837"), ("1912", "1979", "1984")]
    choice = randint(0,3)
    client_socket.send(b"But, what about history? When was the first " + trains[choice] + b" built? Give me the year please!\n")
    try:
        data_recv = client_socket.recv(50)
        output = str(data_recv, "utf-8").strip().replace(" ", "")
        prev_answer.append(output)
        if output in answer[choice]:
            client_socket.send(b"Can't have you on this point, you know your basics! We'll see if you can keep up!\n")
            return
        close_socket(client_socket, client_address)
    except TimeoutError:
        close_socket_timeout(client_socket, client_address)
    except Exception as e:
        print(e)


def question4(client_socket, client_address, prev_answer):
    base = ["base85", "base64", "base32"]
    question = b"I know many encoding bases, but which one i'm using...? (write your answer in lowercase like 'base64')"
    choice = randint(0,2)
    if base[choice] == "base64":
        encoded = base64.b64encode(question)
    elif base[choice] == "base32":
        encoded = base64.b32encode(question)
    elif base[choice] == "base85":
        encoded = base64.b85encode(question)
    else:
        choice = 'base64'
        encoded = base64.b64encode(question)
    client_socket.send(encoded + b"\n")
    
    try:
        data_recv = client_socket.recv(50)
        output = str(data_recv, "utf-8").strip()
        prev_answer.append(output)
        if output == base[choice]:
            client_socket.send(b"Even in the encoding, you're good! Let's move on!\n")
            return
        close_socket(client_socket, client_address)
    except TimeoutError:
        close_socket_timeout(client_socket, client_address)
    except Exception as e:
        print(e)


def question5(client_socket, client_address, prev_answer):
    total_answer = f"{prev_answer[0]},{prev_answer[1]},{prev_answer[2]},{prev_answer[3]}"
    hashs = ["md5", "sha1", "sha256", "sha512"]
    choice = randint(0,3)
    client_socket.send(b"I'm preparing the other questions...\nWhile you wait, can you hash the previous answers in " + bytes(hashs[choice], 'utf-8') + b"?\nYou start with your name (format: hash(1,2,3,4))\n")
    try:
        data_recv = client_socket.recv(500)
        output = str(data_recv, "utf-8").strip().replace(" ", "")
        expected_hash = hashlib.new(hashs[choice], total_answer.encode()).hexdigest()
        if output == expected_hash or output == expected_hash + "\n":
            client_socket.send(b"Good memory, nice for you!\nYou make me feel like I'm not alone anymore, and you seem to be quite skilled!\n")
            client_socket.send(b"Here's the first flag: " + bytes(_FLAG_1, 'utf-8') + b"\nLet's keep talking!\n")
            return
        close_socket(client_socket, client_address)
    except TimeoutError:
        close_socket_timeout(client_socket, client_address)


def question6(client_socket, client_address, prev_answer):
    win = False
    moves = ["R", "P", "S"]
    client_socket.send(b"Now, I would like to play a little game with you, something more interactive!\n \
I hope you know the game rock-paper-scissors!\n \
I modified it a little bit, i'll explain.\n \
I'm going to give you my first move, and you'll answer with your two moves.\n \
My second move will be drawn randomly, and we'll see who wins!\n \
In case of draw, we play another pair of moves in the same way.\n \
To be simple, we're going to use R for Rock, P for Paper and S for Scissors.\n \
The format of your answer should be: R,P\nLet's play together!\n")

    while not win:
        system_moves = [moves[randint(0,2)] for _ in range(2)]

        client_socket.send(b"My first move is " + bytes(system_moves[0], 'utf-8') + b"! What are yours?\n")
        try:
            data_recv = client_socket.recv(50)
            output = str(data_recv, "utf-8").strip().split(",")

            if len(output) != 2: 
                close_socket(client_socket, client_address)
            elif output[0] not in moves or output[1] not in moves:
                close_socket(client_socket, client_address)
            elif (system_moves[0] == "R" and output[0] == "P") or (system_moves[0] == "P" and output[0] == "S") or (system_moves[0] == "S" and output[0] == "R"):
                if system_moves[1] == output[1]:
                    continue
                elif (system_moves[1] == "R" and output[1] == "P") or (system_moves[1] == "P" and output[1] == "S") or (system_moves[1] == "S" and output[1] == "R"):
                    win = True
        except TimeoutError:
            close_socket_timeout(client_socket, client_address)

    client_socket.send(b"Good game, you won!\n")
    return


def question7(client_socket, client_address, prev_answer):
    client_socket.send(b"Let's keep these interactions going, it feels good!\nNow, we're gonna play 'Guess the number'!\n \
I'm thinking of a number between 0 and 20, and you have 5 tries to find it!\n \
Let's start!\n")
    number = randint(0,20)

    for _ in range(5):
        try:
            data_recv = client_socket.recv(50)
            try:
                output = int(str(data_recv, "utf-8").strip())
            except ValueError:
                close_socket(client_socket, client_address)

            if output == number:
                client_socket.send(b"Yay, you found it!\nPretty scary, like you're reading my mind!\nAnyway, let's move on!\n")
                return
            elif output < number:
                client_socket.send(b"Oups, it's bigger than that!\n")
            elif output > number:
                client_socket.send(b"Oups, it's smaller than that!\n")
        except TimeoutError:
            close_socket_timeout(client_socket, client_address)

    client_socket.send(b"Sorry, you didn't find it, but it was fun!\n")
    close_socket(client_socket, client_address)


def question8(client_socket, client_address, prev_answer):
    languages = [
    ("af", "afrikaans"),
    ("ar", "arabic"),
    ("bn", "bengali"),
    ("de", "german"),
    ("el", "greek"),
    ("es", "spanish"),
    ("fr", "french"),
    ("hi", "hindi"),
    ("it", "italian"),
    ("ja", "japanese"),
    ("ko", "korean"),
    ("mr", "marathi"),
    ("ms", "malay"),
    ("no", "norwegian"),
    ("pl", "polish"),
    ("pt", "portuguese"),
    ("ro", "romanian"),
    ("ru", "russian"),
    ("sv", "swedish"),
    ("ta", "tamil"),
    ("tr", "turkish"),
    ("uk", "ukrainian"),
    ("vi", "vietnamese")
]
    
    with open('words.txt', 'r') as f:
        word = f.readlines()[randint(0, 50)].strip()

    number = randint(0, len(languages)-1)
    translator = Translator(source='en', target=languages[number][0])
    translation = translator.translate(word)

    client_socket.send(b"You're tough, let's see if you are so good in languages, because personally, I know a lot of them!\n \
I want you to translate the word /" +bytes(word, 'utf-8') + b"/ in /" + bytes(languages[number][1], 'utf-8') + b"/\n")

    try:
        data_recv = client_socket.recv(50)
        output = str(data_recv, "utf-8").strip()

        if output == translation:
            client_socket.send(b"Good job! You're a polyglot!\n")
            client_socket.send(b"Your skills are impressive, I think I can trust you and give you the second flag: " + bytes(_FLAG_2, 'utf-8') + b"\n")
            return
        close_socket(client_socket, client_address)
    except TimeoutError:
        close_socket_timeout(client_socket, client_address)


def question9(client_socket, client_address, prev_answer):
    with open('rockyou2.txt', 'r', errors='ignore') as f:
        password = f.readlines()[randint(0,100)].strip()

    client_socket.send(b"This time, we're going to play with hashes!\n \
I'm going to give you a password, but I'm not going to tell you what it is!\n \
I'll give you the md5 hash of it, and you'll have to find the password!\n \
I'm giving you a hint, you're kind to me, so I'm kind to you!\n \
The password is in the first hundred lines of the rockyou.txt file!\n")
    
    client_socket.send(b"Here's the hash: /" + hashlib.md5(password.encode()).hexdigest().encode() + b"/\n")

    try:
        data_recv = client_socket.recv(100)
        output = str(data_recv, "utf-8").strip()

        if output == password:
            client_socket.send(b"Wow, you're a hacker!\nLet's move on!\n")
            return
        close_socket(client_socket, client_address)
    except TimeoutError:
        close_socket_timeout(client_socket, client_address)


def question10(client_socket, client_address, prev_answer, bot_name):
    current = datetime.datetime.today()
    current = str(current.day) + "/" + str(current.month) + "/" + str(current.year)
    p1, p2, p3 = False, False, False
    color = ["white", "black", "orange", "red", "yellow", "brown", "green", "blue", "purple", "pink"]
    color_choice = color[randint(0,9)]
    
    client_socket.send(b"We are almost at the end of our conversation, and I must say that I'm having a great time with you!\n \
I have a few more questions for you, and if you answer them correctly, I'll give you the last flag!\n \
Get ready, this one is no joke! I'll ask you three questions!\n")
    client_socket.send(b"What's the color of Henri IV's " + bytes(color_choice, 'utf-8') + b" horse?\n")

    try:
        data_recv = client_socket.recv(50)
        output = str(data_recv, "utf-8").strip()

        if color_choice in output.lower():
            client_socket.send(b"Not bad, you're not colorblind!\n")
            p1 = True
        else:
            close_socket(client_socket, client_address)
    except TimeoutError:
        close_socket_timeout(client_socket, client_address)

    if p1:
        time.sleep(1)
        client_socket.send(b"Which day are we? (dd/mm/yyyy)\n")

        try:
            data_recv = client_socket.recv(50)
            output = str(data_recv, "utf-8").strip()

            if output == current:
                client_socket.send(b"Bravo, you know your calendar!\n")
                p2 = True
            else:
                close_socket(client_socket, client_address)
        except TimeoutError:
            close_socket_timeout(client_socket, client_address)

    if p1 and p2:
        time.sleep(1)
        client_socket.send(b"Last but not the least, do you remember my name?\n \
Because I remember yours, " + bytes(prev_answer[0], 'utf-8') + b", and I'm happy to have met you!\n")
        print("p3")

        try:
            data_recv = client_socket.recv(50)
            output = str(data_recv, "utf-8").strip()

            if output == bot_name:
                client_socket.send(b"Good memory, you're a good friend!\n")
                p3 = True
            else:
                close_socket(client_socket, client_address)
        except TimeoutError:
            close_socket_timeout(client_socket, client_address)

    if p1 and p2 and p3:
        client_socket.send(b"I'm happy to have talked to you, and I hope we can do it again!\n \
I hope you'll come back to see me my friend!\n \
In the meantime, here's the last flag: " + bytes(_FLAG_3, 'utf-8') + b"\n")
        return


# --------------------------------------------------------------------------------

def handle_client(client_socket, client_address):
    client_socket.settimeout(3)
    prev_answer = []
    start_chall(client_socket)
    client_confirmation(client_socket, client_address)
    bot_name = question1(client_socket, client_address, prev_answer)
    time.sleep(1)
    question2(client_socket, client_address, prev_answer)
    time.sleep(1)
    question3(client_socket, client_address, prev_answer)
    time.sleep(1)
    question4(client_socket, client_address, prev_answer)
    time.sleep(1)
    question5(client_socket, client_address, prev_answer)
    time.sleep(1)
    question6(client_socket, client_address, prev_answer)
    time.sleep(1)
    question7(client_socket, client_address, prev_answer)
    time.sleep(1)
    question8(client_socket, client_address, prev_answer)
    time.sleep(1)
    question9(client_socket, client_address, prev_answer)
    time.sleep(1)
    question10(client_socket, client_address, prev_answer, bot_name)
    time.sleep(1)
    close_socket(client_socket, client_address)

# --------------------------------------------------------------------------------

def main():
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection with {client_address[0]}:{client_address[1]}")

            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.daemon = True
            while len(active_threads) >= _MAX_THREADS:
                for thread in active_threads:
                    if not thread.is_alive():
                        active_threads.remove(thread)
                        break

            active_threads.append(client_thread)
            client_thread.start()
    except KeyboardInterrupt:
        server_socket.close()
        print("Server closed by master")
        sys.exit()


if __name__ == "__main__":
    main()
