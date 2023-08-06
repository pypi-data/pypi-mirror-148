from colorama import init
from termcolor import colored

init()


def say_hello(name: str):
    print(colored(f'Hello, {name}!', 'red', 'on_grey', attrs=['reverse', 'blink']))


if __name__ == '__main__':
    say_hello('User')
