import os
import sys
import time

error_wait = 3

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def clear_lines(amount):
    for _ in range(amount):
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")

def invalid_msg(message):
    print(message)
    time.sleep(error_wait)
