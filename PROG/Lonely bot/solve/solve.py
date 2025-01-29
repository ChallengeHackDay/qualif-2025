import sys
import socket
import time
import base64
from random import *
from deep_translator import GoogleTranslator as Translator
import hashlib
import datetime
import re

bot_name = ''

def send_answer(answer):
    print(f"Sending answer: {answer}")
    previous_answer.append(answer)
    socket.send(answer.encode())
    server_answer = socket.recv(BUFFER_SIZE).decode()
    if "See you" in server_answer:
        print("\nexit")
        socket.close()
        sys.exit(0)
    print(f"Server answer: {server_answer}")
    return server_answer


def question0():
    data = socket.recv(BUFFER_SIZE).decode()
    print(f"Question: {data}")
    send_answer("yes")


def question1():
    print("----- question 1 -----")
    global bot_name
    data = socket.recv(BUFFER_SIZE).decode()
    bot_name = data.split("Mine is ")[1].split("\n")[0].strip()
    print(f"Question: {data}")
    time.sleep(0.5)
    send_answer("isnubi")


def question2():
    print("----- question 2 -----")
    data = socket.recv(BUFFER_SIZE).decode()
    print(f"Question: {data}")
    time.sleep(0.5)
    if "Celsius" in data:
        send_answer("900")
    elif "Fahrenheit" in data:
        send_answer("1709")
    elif "Kelvin" in data:
        send_answer("1205")


def question3():
    print("----- question 3 -----")
    data = socket.recv(BUFFER_SIZE).decode()
    print(f"Question: {data}")
    time.sleep(0.5)
    if "vapor" in data:
        send_answer("1804")
    elif "diesel" in data:
        send_answer("1923")
    elif "electric" in data:
        send_answer("1879")
    elif "magnetic" in data:
        send_answer("1979")


def question4():
    print("----- question 4 -----")
    data = socket.recv(BUFFER_SIZE).decode().strip()
    if data == "":
        print("can't find the question data\n")
        socket.close()
        sys.exit(0)
    print(f"Question: {data}")
    time.sleep(0.5)
    for base in ["base85", "base32", "base64"]:
        try:
            if base == "base32":
                decoded = base64.b32decode(data)
            elif base == "base64":
                decoded = base64.b64decode(data)
            elif base == "base85":
                decoded = base64.b85decode(data)
            decoded = decoded.decode('utf-8')
        except:
            pass
        else:
            break
    send_answer(base)


def question5():
    print("----- question 5 -----")
    data = socket.recv(2048).decode()
    print(f"Question: {data}")
    time.sleep(0.5)
    total_answer = f"{previous_answer[1]},{previous_answer[2]},{previous_answer[3]},{previous_answer[4]}"
    if "md5" in data:
        send_answer(hashlib.md5(total_answer.encode()).hexdigest())
    elif "sha1" in data:
        send_answer(hashlib.sha1(total_answer.encode()).hexdigest())
    elif "sha256" in data:
        send_answer(hashlib.sha256(total_answer.encode()).hexdigest())
    elif "sha512" in data:
        send_answer(hashlib.sha512(total_answer.encode()).hexdigest())


def question6():
    print("----- question 6 -----")
    win = False
    possiblities = ["R", "P", "S"]
    data = socket.recv(BUFFER_SIZE).decode().strip()
    print(f"Question: {data}")
    time.sleep(0.5)
    game = socket.recv(BUFFER_SIZE).decode().strip()

    while win == False:
        if "R" in game:
            answer = "P," + possiblities[randint(0, 2)]
        elif "P" in game:
            answer = "S," + possiblities[randint(0, 2)]
        elif "S" in game:
            answer = "R," + possiblities[randint(0, 2)]
        else:
            answer = "R," + possiblities[randint(0, 2)]
        
        game = send_answer(answer)
        if "won" in game:
            win = True
        time.sleep(0.5)


def question7():
    print("----- question 7 -----")
    ok = False
    i = 1
    number1 = randint(1, 20)
    number2 = 0
    max = 21
    min = -1
    data = socket.recv(BUFFER_SIZE).decode()
    print(f"Question: {data}")
    data = send_answer(str(number1))
    if "found" in data:
        return

    while ok == False or i < 5:
        if i >= 5:
            print("max tries reached\n")
            socket.close()
            sys.exit(0)
        if "bigger" in data:
            number2 = randint(number1+1, max-1)
            min = number1
            i += 1
        elif "smaller" in data:
            number2 = randint(min+1, number1-1)
            max = number1
            i += 1
        data2 = send_answer(str(number2))
        if "found" in data2:
            return
        else:
            number1 = number2
            data = data2
        time.sleep(0.5)


def question8():
    print("----- question 8 -----")
    languages = [("af","afrikaans"), ("ar","arabe"), ("bn","bengali"), ("de","allemand"), ("el","grec"), ("en","anglais"), ("es","espagnol"), ("fr","francais"), ("hi","hindi"), ("it","italien"), ("ja","japonais"), ("ko","coreen"), ("mr","marathi"), ("ms","malais"), ("no","neerlandais"), ("pl", "polonais"), ("pt","portugais"), ("ro", "roumain"), ("ru","russe"), ("sv", "suedois"), ("ta","tamoul"), ("tr","turc"), ("uk", "ukrainien"), ("vi","vietnamien")]
    data = socket.recv(BUFFER_SIZE).decode()
    print(f"Question: {data}")
    word = data.split("/")[1]
    language = data.split("/")[3]
    for lang in languages:
        if lang[1] == language:
            language = lang[0]
    translator = Translator(source='en', target=language)

    send_answer(translator.translate(word))
    print(socket.recv(BUFFER_SIZE).decode())


def question9():
    print("----- question 9 -----")
    data = socket.recv(BUFFER_SIZE).decode()
    print(f"Question: {data}")
    if re.search(r".*/[a-f0-9]{32}/", data) is None:
        time.sleep(0.5)
        hash = socket.recv(BUFFER_SIZE).decode().strip().split("/")[1]
        print(f"Hash: {hash}")
    else:
        hash = data.split("/")[1]
        print(f"Hash: {hash}")
    
    # with open("/usr/share/wordlists/rockyou.txt", "r", errors='ignore') as f:
    #     list = f.readlines()[:100]

    # hashtable = {}
    # for word in list:
    #     word = word.strip()
    #     hash_object = hashlib.md5(word.encode())
    #     hash_hex = hash_object.hexdigest()
    #     hashtable[word] = hash_hex
    # print(hashtable)
    hashtable = {'123456': 'e10adc3949ba59abbe56e057f20f883e', '12345': '827ccb0eea8a706c4c34a16891f84e7b', '123456789': '25f9e794323b453885f5181f1b624d0b', 'password': '5f4dcc3b5aa765d61d8327deb882cf99', 'iloveyou': 'f25a2fc72690b780b2a14e140ef6a9e0', 'princess': '8afa847f50a716e64932d995c8e7435a', '1234567': 'fcea920f7412b5da7be0cf42b8c93759', 'rockyou': 'f806fc5a2a0d5ba2471600758452799c', '12345678': '25d55ad283aa400af464c76d713c07ad', 'abc123': 'e99a18c428cb38d5f260853678922e03', 'nicole': 'fc63f87c08d505264caba37514cd0cfd', 'daniel': 'aa47f8215c6f30a0dcdb2a36a9f4168e', 'babygirl': '67881381dbc68d4761230131ae0008f7', 'monkey': 'd0763edaa9d9bd2a9516280e9044d885', 'lovely': '061fba5bdfc076bb7362616668de87c8', 'jessica': 'aae039d6aa239cfc121357a825210fa3', '654321': 'c33367701511b4f6020ec61ded352059', 'michael': '0acf4539a14b3aa27deeb4cbdf6e989f', 'ashley': 'adff44c5102fca279fce7559abf66fee', 'qwerty': 'd8578edf8458ce06fbc5bb76a58c5ca4', '111111': '96e79218965eb72c92a549dd5a330112', 'iloveu': 'edbd0effac3fcc98e725920a512881e0', '000000': '670b14728ad9902aecba32e22fa4f6bd', 'michelle': '2345f10bb948c5665ef91f6773b3e455', 'tigger': 'f78f2477e949bee2d12a2c540fb6084f', 'sunshine': '0571749e2ac330a7455809c6b0e7af90', 'chocolate': 'c378985d629e99a4e86213db0cd5e70d', 'password1': '7c6a180b36896a0a8c02787eeafb0e4c', 'soccer': 'da443a0ad979d5530df38ca1a74e4f80', 'anthony': '65fbef05e01fac390cb3fa073fb3e8cf', 'friends': '28f20a02bf8a021fab4fcec48afb584e', 'butterfly': '9fd8301ac24fb88e65d9d7cd1dd1b1ec', 'purple': 'bb7aedfa61007447dd6efaf9f37641e3', 'angel': 'f4f068e71e0d87bf0ad51e6214ab84e9', 'jordan': 'd16d377af76c99d27093abc22244b342', 'liverpool': 'd177b4d1d9e6b6fa86521e4b3d00b029', 'justin': '53dd9c6005f3cdfc5a69c5c07388016d', 'loveme': '74d738020dca22a731e30058ac7242ee', 'fuckyou': '596a96cc7bf9108cd896f33c44aedc8a', '123123': '4297f44b13955235245b2497399d7a93', 'football': '37b4e2d82900d5e94b8da524fbeb33c0', 'secret': '5ebe2294ecd0e0f08eab7690d2a6ee69', 'andrea': '1c42f9c1ca2f65441465b43cd9339d6c', 'carlos': 'dc599a9972fde3045dab59dbd1ae170b', 'jennifer': '1660fe5c81c4ce64a2611494c439e1ba', 'joshua': 'd1133275ee2118be63a577af759fc052', 'bubbles': 'fe75bd065ff48b91c35fe8ff842f986c', '1234567890': 'e807f1fcf82d132f9bb018ca6738a19f', 'superman': '84d961568a65073a3bcf0eb216b2a576', 'hannah': 'eb09d5e396183f4b71c3c798158f7c07', 'amanda': '6209804952225ab3d14348307b5a4a27', 'loveyou': 'f74a10e1d6b2f32a47b8bcb53dac5345', 'pretty': '2f0e7ef29748dbf6dacf8381c4cc921c', 'basketball': 'd0199f51d2728db6011945145a1b607a', 'andrew': 'd914e3ecf6cc481114a3f534a5faf90b', 'angels': '82a7c395a86348dd4bfd11bb05b71cbf', 'tweety': 'c03a5a4ba81cd3d8e59840a6f0eddad7', 'flower': '608f0b988db4a96066af7dd8870de96c', 'playboy': 'cfe819bed5b34b02ccb68ab69ab2055b', 'hello': '5d41402abc4b2a76b9719d911017c592', 'elizabeth': '4af09080574089cbece43db636e2025f', 'hottie': 'c37df36db804246d74e786a92488d232', 'tinkerbell': '7f9a6871b86f40c330132c4fc42cda59', 'charlie': 'bf779e0933a882808585d19455cd7937', 'samantha': 'f01e0d7992a3b7748538d02291b0beae', 'barbie': '1aef0a62ed84bb165989ab32f0ba56c2', 'chelsea': '91cb315a6405bfcc30e2c4571ccfb8ce', 'lovers': '8dae58e3f282b974328d53f96753f4c1', 'teamo': '313437c00302021eda7b4197983f4011', 'jasmine': 'f21c0d3e564c7db5ccf73c095a0b9371', 'brandon': 'fc275ac3498d6ab0f0b4389f8e94422c', '666666': 'f379eaf3c831b04de153469d1bec345e', 'shadow': '3bf1114a986ba87ed28fc1b5884fc2f8', 'melissa': 'ff5390bde5a4cf0aa2006cf2198efd29', 'eminem': '26b637ed41273425be243e8d42e5b461', 'matthew': 'e6a5ba0842a531163425d66839569a68', 'robert': '684c851af59965b680086b7b4896ff98', 'danielle': 'd05a90b8f6326735fd07fcfc7b92e47a', 'forever': 'd7af994f1f1ef8b5e3beb9f7fb139f57', 'family': '0d3fda0bdbb9d619e09cdf3eecba7999', 'jonathan': '78842815248300fa6ae79f7776a5080a', '987654321': '6ebe76c9fb411be97b3b0d48b791a7c9', 'computer': 'df53ca268240ca76670c8566ee54568a', 'whatever': '008c5926ca861023c1d2a36653fd88e2', 'dragon': '8621ffdbc5698829397d97767ac13db3', 'vanessa': '282bbbfb69da08d03ff4bcf34a94bc53', 'cookie': '2dccd1ab3e03990aea77359831c85ca2', 'naruto': 'cf9ee5bcb36b4936dd7064ee9b2f139e', 'summer': '6b1628b016dff46e6fa35684be6acc96', 'sweety': 'de1e3b0952476aae6888f98ea0e4ac11', 'spongebob': 'e1964798cfe86e914af895f8d0291812', 'joseph': 'cb07901c53218323c4ceacdea4b23c98', 'junior': 'b03e3fd2b3d22ff6df2796c412b09311', 'softball': '92290ccb8f7b2beb4c57ef1f7a3d5947', 'taylor': '7d8bc5f1a8d3787d06ef11c97d4655df', 'yellow': 'd487dd0b55dfcacdd920ccbdaeafa351', 'daniela': '07a88e756847244f3496f63f473d6085', 'lauren': '2760c7b84d4bad6b0b12d7c1a6c5e1a4', 'mickey': '4d5257e5acc7fcac2f5dcd66c4e78f9a', 'princesa': 'ac3665f6acae8bd267ed92a71a71313b'}
    for key, value in hashtable.items():
        if value == hash:
            send_answer(key)
            break


def question10():
    print("----- question 10 -----")
    data = socket.recv(BUFFER_SIZE).decode()
    print(f"Question: {data}")
    data = socket.recv(BUFFER_SIZE).decode()
    color = data.split("Henri IV's")[1].split("horse")[0].strip()
    time.sleep(0.5)
    send_answer(color)

    data = socket.recv(BUFFER_SIZE).decode()
    print(f"Question: {data}")
    time.sleep(0.5)
    current = datetime.datetime.today()
    current = f"{current.day}/{current.month}/{current.year}"
    send_answer(current)

    data = socket.recv(BUFFER_SIZE).decode()
    print(f"Question: {data}")
    time.sleep(0.5)
    send_answer(bot_name)


def main():
    question0()
    time.sleep(1)
    question1()
    time.sleep(1)
    question2()
    time.sleep(1)
    question3()
    time.sleep(1)
    question4()
    time.sleep(1)
    question5()
    time.sleep(1)
    question6()
    time.sleep(1)
    question7()
    time.sleep(1)
    question8()
    time.sleep(1)
    question9()
    time.sleep(1)
    question10()
    time.sleep(1)
    print(socket.recv(BUFFER_SIZE).decode())
    socket.close()


if __name__ == "__main__":
    try: 
        if len(sys.argv) < 3:
            print("Usage: python solve.py <host> <port>")
            sys.exit(1)


        previous_answer = []

        TCP_IP = sys.argv[1]
        TCP_PORT = int(sys.argv[2])
        BUFFER_SIZE = 2048

        socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.connect((TCP_IP, TCP_PORT))

        main()
    except KeyboardInterrupt:
        socket.close()
        sys.exit(0)
