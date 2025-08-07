from termcolor import colored
import json
import time
import sys
import os

ELEMENTS = ["water","stone","fire","plant","vital","force","thunder"]
STATUSES = ["burn","wound","decay","regen","slow","quick",
            "anger","stun","sleep","strong","tough","curse"]
SPECIALS = ["heat","curse_risk","ignores_damage","is_elite"]
ARG_OPTS = {
    "damage" :  ["$_base_damage","$_declared","$_calculated_damage"],
    "element":  ["$_element","$_declared","$_random","$_choice"],
    "status":   ["$_declared","$_random","$_choice",
                 "burn","wound","decay","regen","slow","quick",
                 "anger","stun","sleep","strong","tough","curse"]
}

FUNCTIONS= {
    "character": {
        "calculate_damage": {
            "args": ["damage_element","amount"],
            "returns": ["calculated_damage"]
        },
        "calculate_speed": {
            "args": [],
            "returns": ["speed"]
        },
        "take_damage": {
            "args": ["amount"],
            "returns": []
        },
        "heal": {
            "args": ["amount", "element"],
            "returns": []
        },
        "attune_to": {
            "args": ["element"],
            "returns": []
        },
        "negate_attune": {
            "args": ["element"],
            "returns": []
        },
        "spend_attune": {
            "args": ["element"],
            "returns": ["turns_spent"]
        },
        "gain_status": {
            "args": ["status","amount"],
            "returns": []
        },
        "lost_status": {
            "args": ["status","amount"],
            "returns": []
        },
        "negate_status": {
            "args": ["status"],
            "returns": []
        },
        "bank_move": {
            "args": ["move"],
            "returns": []
        },
        "unbank_move": {
            "args": ["move"],
            "returns": []
        },
        "gain_immune": {
            "args": ["status"],
            "returns": []
        },
        "negate_immune": {
            "args": ["status"],
            "returns": []
        },
        "check_wound_immunity": {
            "args": [],
            "returns": ["immunity_removed"]
        },
        "gain_ignorance": {
            "args": ["status","amount"],
            "returns": []
        },
        "lose_ignorance": {
            "args": ["status","amount"],
            "returns": []
        },
        "negate_ignorance": {
            "args": ["status"],
            "returns": []
        },
        "burn_out": {
            "args": ["amount"],
            "returns": []
        },
        "open_wounds": {
            "args": [],
            "returns": ["amount_taken"]
        },
        "thousand_cuts": {
            "args": [],
            "returns": []
        },
        "gain_heat": {
            "args": ["amount"],
            "returns": ["overheated"]
        },
        "roll_heat": {
            "args": [],
            "returns": ["overheated"]
        },
        "roll_curse": {
            "args": [],
            "returns": ["became_cursed"]
        },
        "take_curse_damage": {
            "args": [],
            "returns": []
        },
        #"": {
        #    "args": [],
        #    "returns": []
        #},
    },
    "combat": {
    }
}

def clear_lines(amount):
    for _ in range(amount):
        sys.stdout.write("[F")
        sys.stdout.write("[K")

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

class Move:
    def __init__(self):
        self.name:str       = ""
        self.element:str    = ""
        self.type:str       = ""
        self.target:str     = ""
        self.description:str= ""
        self.base_damage:int= 0
        self.base_iters:int = 1
        self.effects:dict = {
            "pre-iter": [],
            "iterable": [],
            "post-iter":[]
        }

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def set_element(self):
        print(colored("Define Element:", "cyan"))
        for i, element in enumerate(ELEMENTS):
            print(colored(f"{i+1}: ", "yellow"),end = f"{element}")
        while True:
            choice = (input("> ").strip().lower())
            if choice in ELEMENTS:
                self.element = choice
                break
            elif choice.isdigit() and int(choice) in range(1, len(ELEMENTS) + 1):
                self.element = ELEMENTS[int(choice)-1]
                break
            else:
                print(colored("Invalid Choice", "red"))
                time.sleep(2)
                clear_lines(4)

    def set_type(self):
        print(colored("Define Type:", "cyan"))
        for i, value in enumerate(['attack','utility']):
            print(colored(f"{i+1}: ", "yellow"),end = f"{value}")
        while True:
            choice = (input("> ").strip().lower())
            if choice in (['attack','utility']):
                self.type = choice
                break
            elif choice == "1":
                self.type = "attack"
                break
            elif choice == "2":
                self.type = "utility"
                break
            else:
                print(colored("Invalid Choice", "red"))
                time.sleep(2)
                clear_lines(4)

    def set_target(self):
        print(colored("Define Target:", "cyan"))
        for i, value in enumerate(['caster','opponent','declared']):
            print(colored(f"{i+1}: ", "yellow"),end = f"{value}")
        while True:
            choice = (input("> ").strip().lower())
            if choice in (['caster','opponent','declared']):
                self.target = choice
                break
            elif choice == "1":
                self.target = "caster"
                break
            elif choice == "2":
                self.target = "opponent"
                break
            elif choice == "3":
                self.target = "declared"
                break
            else:
                print(colored("Invalid Choice", "red"))
                time.sleep(2)
                clear_lines(4)

    def set_base_damage(self):
        print(colored("Define Base Damage:", "cyan"))
        while True:
            choice = input("> ").strip()
            if choice.isdigit():
                self.base_damage = int(choice)
                break
            else:
                print(colored("Invalid Choice", "red"))
                time.sleep(2)
                clear_lines(3)

    def set_base_iters(self):
        print(colored("Define Base Iterations:", "cyan"))
        while True:
            choice = input("> ").strip()
            if choice.isdigit():
                self.base_iters = int(choice)
                break
            else:
                print(colored("Invalid Choice", "red"))
                time.sleep(2)
                clear_lines(3)

    def add_function(self):
        # Define Host
        print(colored("Choose Function Host:", "cyan"))
        hosts = list(FUNCTIONS.keys())
        for i, host in enumerate(hosts):
            print(colored(f"{i+1}: ", "yellow"),end= f"{host}")
        while True:
            choice = (input("> ").strip().lower())
            if choice in hosts:
                func_host = choice
                break
            elif choice.isdigit() and int(choice) in range(1, len(hosts) + 1):
                func_host = hosts[int(choice)-1]
                break
            else:
                print(colored("Invalid Choice.", "red"))
                time.sleep(2)
                clear_lines(4)
        # Define Function
        print(colored("Choose Function:", "cyan"))
        functions = list(FUNCTIONS[func_host].keys())
        for i, func_name in enumerate(functions):
            function = FUNCTIONS[func_host][func_name]
            print(colored(f"{i+1}: ", "yellow"),end = f"{func_name}")
            print(colored("args: ", "cyan"),end="")
            for arg in function['args']:
                print(f"{arg}", end= colored(", ", "cyan"))
            print(colored("returns: ", "green"),end="")
            for item in function['returns']:
                print(f"{item}", end= colored(", ", "green"))
            print("")
        while True:
            choice = (input("> ").strip().lower())
            if choice in functions:
                func_func = choice
                break
            elif choice.isdigit() and int(choice) in range(1, len(functions) + 1):
                func_func = functions[int(choice)-1]
                break
            else:
                print(colored("Invalid Choice", "red"))
                time.sleep(2)
                clear_lines(4)

        new_effect = Effect(func_host, func_func)
        new_effect.define_args()
        new_effect.define_returns()

        while True:
            if new_effect.host == "character":
                print(colored("1: ", "cyan") + "caster\n" +
                      colored("2: ", "cyan") + "opponent\n")
                choice = (input("> ").strip().lower())
                if choice in ["caster", "1"]:
                    new_effect.host = "caster"
                    break
                elif choice in ["opponent", "2"]:
                    new_effect.host = "opponent"
                    break
                else:
                    print(colored("Invalid Choice", "red"))
                    time.sleep(2)
                    clear_lines(5)

        while True:
            locations = ['pre-iter','iterable','post-iter']
            for i, location in enumerate(locations):
                print(colored(f"{i+1}: ", "yellow"),end = f"{location}")
            choice = (input("> ").strip().lower())
            if choice in locations:
                self.effects[choice].append(new_effect.__dict__)
                break
            elif choice.isdigit() and int(choice) in range(1, len(locations) + 1):
                self.effects[locations[int(choice)-1]].append(new_effect.__dict__)
                break
            else:
                print(colored("Invalid Choice", "red"))
                time.sleep(2)
                clear_lines(4)

    def save_to_json(self):
        """Saves the move to a JSON file in the 'moves' directory."""
        if not os.path.exists("moves"):
            os.makedirs("moves")
        file_path = os.path.join("moves", f"{self.name.lower().replace(' ', '_')}.json")
        with open(file_path, 'w') as f:
            json.dump(self, f, default=lambda o: o.__dict__, indent=4)
        print(colored(f"Move saved to {file_path}", "green"))

class Effect:
    def __init__(self, func_host, func_func):
        self.host:str       = func_host
        self.function:str   = func_func
        self.args:dict      = {}
        self.returns:dict   = {}

        for arg in FUNCTIONS[func_host][func_func]['args']:
            self.args[arg] = None

        for item in FUNCTIONS[func_host][func_func]['returns']:
            self.returns[item] = None

    def define_args(self):
        if not self.args:
            return
        while True:
            print("Current Arg Values: ")
            i = 1
            for arg, data in self.args.items():
                print(f"{i}: " + colored(f"{arg}:", "magenta"), end=f"{data}")
                i += 1

            print("Choose Arg to Define (or type 'done' to finish):")
            choice = (input("> ").strip().lower())
            if choice == 'done':
                break
            arg_to_define = None
            if choice in self.args:
                arg_to_define = choice
            elif choice.isdigit() and int(choice) in range(1, len(self.args) + 1):
                arg_to_define = list(self.args.keys())[int(choice)-1]
            else:
                print(colored("Invalid Choice", "red"))
                time.sleep(2)
                clear_lines(4)
                continue

            print(f"Defining argument: {arg_to_define}")
            if arg_to_define in ARG_OPTS:
                for i, option in enumerate(ARG_OPTS[arg_to_define]):
                    print(colored(f"{i+1}: ", "yellow"),end = f"{option}")
                while True:
                    choice = (input("> ").strip().lower())
                    if choice in ARG_OPTS[arg_to_define]:
                        self.args[arg_to_define] = choice
                        break
                    elif choice.isdigit() and int(choice) in range(1, len(ARG_OPTS[arg_to_define]) + 1):
                        self.args[arg_to_define] = ARG_OPTS[arg_to_define][int(choice)-1]
                        break
                    else:
                        print(colored("Invalid Choice", "red"))
                        time.sleep(2)
                        clear_lines(4)
            else:
                print("Enter value:")
                self.args[arg_to_define] = input("> ").strip()


    def define_returns(self):
        if not self.returns:
            return
        while True:
            print("Current Return Values: ")
            i = 1
            for item, data in self.returns.items():
                print(f"{i}: " + colored(f"{item}:", "magenta"), end=f"{data}")
                i += 1
            print("Choose Return to Define (or type 'done' to finish):")
            choice = (input("> ").strip().lower())
            if choice == 'done':
                break

            return_to_define = None
            if choice in self.returns:
                return_to_define = choice
            elif choice.isdigit() and int(choice) in range(1, len(self.returns) + 1):
                return_to_define = list(self.returns.keys())[int(choice)-1]
            else:
                print(colored("Invalid Choice", "red"))
                time.sleep(2)
                clear_lines(4)
                continue

            print("Enter Return Name:")
            choice = (input("> ").strip())
            self.returns[return_to_define] = choice


def main():
    while True:
        clear_screen()
        move = Move()
        print(colored("Let's create a new move!", "cyan"))

        print(colored("Enter Move Name:", "cyan"))
        move.name = input("> ").strip()

        move.set_element()
        clear_screen()
        move.set_type()
        clear_screen()
        move.set_target()
        clear_screen()
        move.set_base_damage()
        clear_screen()
        move.set_base_iters()
        clear_screen()

        while True:
            print(colored("Current Move:", "cyan"))
            print(move)
            print(colored("What would you like to do?", "cyan"))
            print(colored("1: ", "yellow"), "Add Function")
            print(colored("2: ", "yellow"), "Save and Finish")
            print(colored("3: ", "yellow"), "Exit without Saving")

            choice = input("> ").strip()
            if choice == '1':
                clear_screen()
                move.add_function()
            elif choice == '2':
                move.save_to_json()
                break
            elif choice == '3':
                break
            else:
                print(colored("Invalid Choice", "red"))
                time.sleep(2)
        print("Create another move? (y/n)")
        choice = input("> ").strip().lower()
        if choice not in ['y', 'yes']:
            break

if __name__ == "__main__":
    main()
