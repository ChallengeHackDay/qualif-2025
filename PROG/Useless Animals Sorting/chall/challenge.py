import random
import os
import base64
import time

FLAG = os.getenv("FLAG", "HACKDAY{fake_flag}")

def choose_random_image() -> tuple[str, str]:
    d = random.choice(os.listdir("datasets"))
    file = random.choice(os.listdir("datasets/"+d))    
    with open("datasets/"+d+"/"+file, 'rb') as f:
        text = base64.b64encode(f.read()).decode()
        return text, d

def check_time(start):
    if time.time() - start > 100:
        print("Time's up ! Maybe next time...")
        exit(0)
  
def main():
    print("Welcome to the animal guessing game !\nYou have to guess the animal in 100 images in 100s. 5 errors allowed\nGood luck !")
    print("List of correct answers : 'dog', 'horse', 'elephant', 'butterfly', 'chicken', 'cat', 'cow', 'sheep', 'spider', 'squirrel'")
    input("Press Enter to start the game")
    errors = 0
    now = time.time()
    for i in range(100):
        img, label = choose_random_image()
        print(f"Image n°{i+1} : \n{img}\nAnimal ? ")
        answer = input()
        check_time(now)
        if answer != label:
            errors += 1
            print("Wrong ! It was a", label, ", you have", 5-errors, "errors left")
            if errors >= 5:
                print("Too many errors, you lost !")
                exit(0)
        else:
            print("Correct !")
    print("Congratulations, you won with", errors, "errors, here is your flag :", FLAG)

if __name__ == "__main__":
    main()