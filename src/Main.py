import random
import math
import os

# --- Load Data Files ---
# Load valid words
with open('validwords.txt') as f:
    validWords = [x.strip() for x in f.readlines()]

# Load ordinal words (first, second, etc.)
with open('ordinalwords.txt') as g:
    ordinalwords = [x.strip() for x in g.readlines()]

# Load possible answer words
with open('wordanswers.txt') as g:
    wordAnswers = [x.strip() for x in g.readlines()]

# Load recommended starting words
with open('startingWords.txt') as g:
    startingWords = [x.strip() for x in g.readlines()]

# Load reward multipliers
with open('rewards.txt') as g:
    rewards = [x.strip() for x in g.readlines()]

# --- Game State Initialization ---
guess = ""
isloan = False
money = 100
debt = 0
ogdebt = 0
rate = 0.2
missed = 0
loanlen = 0
pay = 0

# --- Main Game Loop ---
while True:
    win = False
    guesson = 999

    # Select random answer word
    wordnum = random.randint(0, len(wordAnswers) - 1)
    word = wordAnswers[wordnum]
    print(word)  # Remove or comment out for production

    # --- Game Introduction ---
    print("Welcome to:")
    print("   _____                 _                          _ _   ")
    print("  / ____|               | |                        | | |  ")
    print(" | |  __  __ _ _ __ ___ | |____      _____  _ __ __| | | ___")
    print(" | | |_ |/ _` | '_ ` _ \\| '_ \\ \\ /\\ / / _ \\| '__/ _` | |/ _ \\")
    print(" | |__| | (_| | | | | | | |_) \\ V  V / (_) | | | (_| | |  __/")
    print("  \\_____|\\__,_|_| |_| |_|_.__/ \\_/\\_/ \\___/|_|  \\__,_|_|\\___|")
    print("You have " + str(money) + " chips.")

    # --- Loan Payment Section ---
    if isloan:
        print("You still owe me " + str(debt) + " chips.")
        answer = input("Do you want to pay " + str(pay) + " this round? Or let it compound. y/n")
        if answer == "y":
            if money >= pay:
                money -= pay
                debt -= pay
                loanlen-= 1
                pay = round(debt / loanlen)
                print("You now have " + str(money) + " chips.")
                if debt <= 0:
                    print("Wow. You actually paid me back.")
                    isloan = False
            else:
                print("Get more money bro. Ur broke.")
        else:
            missed += 1
            loanlen -= 1
            debt = round(debt * ((1 + rate) ** missed))
            print("You better pay next round. Your debt has compounded to " + str(debt) + " chips.")
            pay = round(debt / loanlen)

    # --- Betting and Guess Setup ---
    print("The lower amount of guesses you request, the more money you win if you guess it and vice versa.")
    pool = input("How much money do you want to put in: ")
    while int(pool) < 1 or int(pool) > money:
        print("Bruh you're not that rich.")
        pool = input("How much money do you want to put in?")
    guesses = input("How many guesses do you want? Pick a number 1 through 10.")
    money -= int(pool)
    while not int(guesses) >= 1 or not int(guesses) <= 10:
        print("I don't think that's a number 1 through 10. Try again.")
        guesses = input("How many guesses do you want? Pick a number 1 through 10.")
    print("You get " + guesses + " chances to guess a 5-letter word.")

    # --- Guessing Loop ---
    for i in range(int(guesses)):
        if i == 0:
            guess1 = input("What is your " + ordinalwords[i] + " guess?")
            guess = guess1
        else:
            guess = input("What is your " + ordinalwords[i] + " guess?")
        if not guess.lower() in validWords:
            while not guess.lower() in validWords:
                print("Invalid Word")
                guess = input("What is your " + ordinalwords[i] + " guess?")

        if guess.lower() in validWords:
            if guess.lower() == word:
                print("You guessed it")
                guesson = i
                win = True
                break
            else:
                # Feedback for each letter
                for j in range(5):
                    if guess[j].lower() == word[j]:
                        print("🟩 ", end="")
                    elif guess[j].lower() in word:
                        print("🟨 ", end="")
                    else:
                        print("🟥 ", end="")
                print()

    # --- Win/Loss Handling ---
    if win:
        print("YOU WIN!")
        gained = int(pool) * int(rewards[int(guesses) - 1])
        print("You gained " + str(gained) + " chips.")
        money += int(gained)
        print("You now have " + str(money) + " chips.")
    else:
        print("YOU LOST!")
        print("The word was " + word)
        print("You put in " + str(pool) + " chips. Those are mine now 😈.")
        print("You now have " + str(money) + " chips.")

    # --- Out of Money / Loan Offer ---
    if money <= 0:
        print("You have no money")
        if isloan:
            input("You had a loan. Now you can't pay it back. YOU LOST (Enter to continue)")
            while True:
                print("The loan sharks are coming.")

        yn = input("Do you want a loan? y/n: ")
        if yn == "y":
            loan = input("How many chips do you want to take out? You can get up to 100 chips: ")
            while int(loan) > 100 or int(loan) < 1:
                print("I said no more than 100")
                loan = input("How many chips do you want to take out? You can get up to 100 chips: ")
            money += int(loan)
            ogdebt = int(loan)
            rate = 0.2
            missed = 0
            debt = round(ogdebt * (1 + rate))
            loanlen = math.floor(int(loan) / 10)
            print("You need to pay " + str(debt) + " by " + str(loanlen) + " rounds.")
            isloan = True
            pay = round(debt / loanlen)
        else:
            print("Well you have no money so better luck next time.")
            break

    # --- Wordle Bot Analysis (Optional) ---
    if input("Do you want a wordle bot analysis? y/n") == "y":
        print()
        print("FIRST ROUND")
        input("(Enter to continue)")
        if guess1.lower() in startingWords or guess1.lower() == word:
            print("Good job, you chose a good starting word")
            print("Other good starting words are:", end="")
            input()
        else:
            print("You chose a terrible starting word. No wonder you didn't win first guess.")
            print("A list of words you should start with are:", end="")
            input()

        for i in range(len(startingWords)):
            print(startingWords[i])

        for i in range(1, int(guesses)):
            print()
            print(ordinalwords[i].upper() + " ROUND")
            print()

            if guesson == i:
                print("You won in the " + ordinalwords[i] + " round.")
                print("Took you long enough")
                break
            elif guesson == 999:
                print("Bruh how did u not win?")
                input()
            else:
                print("You still didn't win in the " + ordinalwords[i] + "round.")
                print("Wow that's impressive!")
                input()

    # --- Play Again Prompt ---
    if input("Do you want to play again? y/n") == "n":
        break
    else:
        print("Restarting game...")
        os.system('clear')  # Clear the screen for a fresh start