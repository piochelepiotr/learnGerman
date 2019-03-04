#! /usr/local/bin/python3

import pandas as pd
from random import randint
import tty
import sys
import termios
import os

def build_translations():
    try:
        d = {}
        df = pd.read_csv('french_english.csv')
        for i, english in enumerate(df['english']):
            french = df['french'][i]
            d[str(english).lower()] = str(french).lower()
            #print("English is: {}".format(english))
            #print("French is: {}".format(french))
        return d
    except FileNotFoundError:
        return None

def translate(translations):
    try:
        df = pd.read_csv('words.csv')
        french = []
        english = []
        for i, w in enumerate(df['Word']):
            print(w)
            print("HELLO")
            try:
                french.append(translations[w])
                english.append(w)
            except KeyError:
                print("Can't find translation for {}".format(w))
        l = pd.DataFrame(
            {
                "english": english,
                "french": french,
            })
        l.to_csv('list.csv')
        return True
    except FileNotFoundError:
        return False


def main():
    translations = build_translations()
    if translations is None:
        print("Impossible to build translations, exiting")
        return
    print(translations['car'])
    print(translations['climb'])
    print(translations['power'])
    translate(translations)

if __name__ == '__main__':
    main()
    
