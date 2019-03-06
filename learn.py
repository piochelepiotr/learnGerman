#! /usr/local/bin/python3

import pandas as pd
from random import randint
import tty
import sys
import termios
import os

book_name = 'book.csv'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Commands:
    IKNOWIT = 'y'
    DONTKNOW = 'n'
    LETSTRY = 'i'
    SAYPREVIOUS = 'p'
    EXIT = 'e'

def load_existing_learning_book():
    try:
        df = pd.read_csv(book_name)
    except FileNotFoundError:
        return None
    return df

def create_new_learning_book():
    try:
        df = pd.read_csv('translation.csv')
        n = df.shape[0]
        # tries you again on this word after remind is bellow 0
        df['remind'] = [0 for i in range(n)]
        df['attempts'] = [0 for i in range(n)]
        df['fails'] = [0 for i in range(n)]
    except FileNotFoundError:
        print("Can't find translation. Exiting")
        exit(1)
    return df

def isCommand(x):
    return x in [Commands.IKNOWIT, Commands.DONTKNOW, Commands.LETSTRY, Commands.SAYPREVIOUS, Commands.EXIT]

def get_command():
    orig_settings = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin)
    x = ''
    while not isCommand(x):
        x=sys.stdin.read(1)[0]
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
    return x

def choose_word(book):
    current_min = 0
    current_max = 400
    n = book.shape[0]
    while True:
        i = randint(max(0, current_min), min(n-1, current_max))
        book.loc[i,'remind'] = book['remind'][i] - 1
        if book['remind'][i] < 0:
            return i

def exercice(book, previous, i = -1):
    if i == -1:
        i = choose_word(book)
    attempts = book['attempts'][i]
    fails = book['fails'][i]
    print("({}/{}) {}".format(attempts - fails, attempts, book['english'][i]))
    translation = book['german'][i]
    r = get_command()
    if r == Commands.IKNOWIT:
        book.loc[i,'attempts'] = book['attempts'][i] + 1
        book.loc[i,'remind'] = 10
        print(bcolors.OKBLUE + translation + bcolors.ENDC)
    elif r == Commands.DONTKNOW:
        book.loc[i,'attempts'] = book['attempts'][i] + 1
        book.loc[i,'fails'] = book['fails'][i] + 1
        print(bcolors.WARNING + translation + bcolors.ENDC)
        os.system("say -v Anna \"{}\"".format(translation))
    elif r == Commands.LETSTRY:
        r = input('>')
        book.loc[i,'attempts'] = book['attempts'][i] + 1
        if r.lower() != translation.lower():
            print(bcolors.FAIL + translation + bcolors.ENDC)
            book.loc[i,'fails'] = book['fails'][i] + 1
            os.system("say -v Anna \"{}\"".format(translation))
        else:
            book.loc[i,'remind'] = 10
    elif r == Commands.SAYPREVIOUS:
        #print("say {}".format(previous))
        os.system("say -v Anna \"{}\"".format(previous))
        return exercice(book, previous, i)
    elif r == Commands.EXIT:
        return None
    return translation

def save_learning_book(book):
    book.to_csv(book_name)

def main():
    book = load_existing_learning_book()
    if book is None:
        book = create_new_learning_book()
    previous = 'first'
    while previous != None:
        previous = exercice(book, previous)
    save_learning_book(book)

if __name__ == '__main__':
    main()
    
