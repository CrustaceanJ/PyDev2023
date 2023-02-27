import os

import typing as tp
import argparse

from collections import Counter
from random import choice

import requests
import cowsay


def ask(prompt: str, valid: tp.List[str]) -> str:
    guess = None
    while True:
        if guess is not None:
            prompt_temp =  f'Слова {guess:^9s} нет в словаре.\n' + prompt
            print(cowsay.cowsay(prompt_temp, cow=cowsay.get_random_cow()))
        else:
            print(cowsay.cowsay(prompt, cow=cowsay.get_random_cow()))
        guess = input().strip()
        if guess not in valid:
            continue
        else:
            return guess



def inform(format_string: str, bulls: int, cows: int) -> None:
    print(cowsay.cowsay(format_string.format(bulls, cows), cow=cowsay.get_random_cow()))


def bullscows(guess: str, secret: str) -> tp.Tuple[int, int]:
    bulls = sum(g == s for g, s in zip(guess, secret))
    common = Counter(guess) & Counter(secret)
    cows = sum(common.values())

    return bulls, cows


def gameplay(ask: tp.Callable, inform: tp.Callable, words: tp.List[int]) -> int:
    secret = choice(words)
    trials = 0
    while True:
        trials += 1
        guess = ask("Введите слово: ", words)
        bulls, cows = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", bulls, cows)
        if bulls == len(secret):
            break
    
    return trials


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('vocab', help='URL or path to file with list of valid words')
    parser.add_argument('length', nargs='?', type=int, default=5, help='Allowed words length')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    if os.path.isfile(args.vocab):
        with open(args.vocab, 'r') as f:
            vocab = [line.strip() for line in f]
    else:
        with requests.get(args.vocab) as r:
            vocab = [word.strip() for word in r.text.split()]

    if args.length:
        vocab = [word for word in vocab if len(word) == args.length]
    
    trials = gameplay(ask, inform, vocab)
    print(f'Game ends with {trials} trials')
