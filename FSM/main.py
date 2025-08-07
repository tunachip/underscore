from fsm import FSM
from states._title import Title
from states._menu import Menu
from states._loading import Loading
from states._combat import Combat
from states._upgrade import Upgrade
from states._gameover import GameOver

STATES = {
    'TITLE':    Title,
    'MENU':     Menu,
    'LOADING':  Loading,
    'COMBAT':   Combat,
    'UPGRADE':  Upgrade,
    'GAMEOVER': GameOver 
}

EXITS = ['quit', 'q', 'exit',  'close']

def main():
    fsm = FSM()
    for state, data in STATES:
        fsm.register(f"{state}", data)
    
    fsm.change('title')

    while True:
        fsm.render()
        user_input = (input("> ").strip().lower())
        if user_input in EXITS:
            break
        next_state = fsm.handle_input(user_input)
        # Debug
        print(f" [DEBUG-MAIN] handle_input() returns: {next_state}")

        if str(next_state) in EXITS:
            break
        elif str(next_state) in fsm.states:
            fsm.change(next_state)
        fsm.update()

if __name__ == '__main__':
    main()
