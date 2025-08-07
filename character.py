import globals
import random
from termcolor import colored
from tabulate import tabulate

class Character:
    """
    Fleshed Out Character Class
    This will need to be broken up into the following:
    1. Base Class
    2. Player Class
    3. Enemy Class
    """
    def __init__(self,name, level= 1, max_hp= 10, hp = 10, 
                 is_elite = False, blessings = [None], turn_history = {None},
                 moves = {"active" : [None], "banked" : [None]} ):
        self.name:str               = name
        self.level:int              = level
        self.max_hp:int             = max_hp
        self.hp:int                 = hp
        self.speed: int             = 3 # For Turn Order Calculation
        self.last_damage_taken: int = 0 # For Revenge Effects
        self.total_damage_taken:int = 0 # For 'Flesh Flood'
        self.heat:int               = 0 # Max: 6
        self.curse_risk:int         = 0 # Max: 10
        self.bless_burden:int       = 0 # For Elite Calc + Bless Permission
        self.elites_slain:int       = 0 # For Bless Permission
        self.iter_mod:int           = 0 # Adds to Move Logic Base_Iters
        self.has_priority: bool     = False # For Turn Order Calculation
        self.ignores_damage:bool    = False # For 'Dripped Out'
        self.is_elite:bool          = is_elite # For Random Encounters
        self.blessings:list         = blessings
        self.chosen_move:dict       = {}
        self.turn_history:dict      = turn_history
        self.moves:dict             = moves
        self.attunements:dict = {
            element: {
                'turns': 0,
                'is_attuned': False,# Flag for End-Of-Turn Uptick
                'is_public': False  # Whether Info Known by Opp
            } for element in globals.ELEMENTS
        }
        self.statuses:dict = {
            status: {
                'turns': 0,
                'ignores': 0,       # Ignores Effects, Can Gain More Turns
                'is_immune': False, # Effects Happen, Cannot Gain More Turns
                'max': globals.STATUSES[status]['max'],
            } for status in globals.STATUSES
        }

    





    def __str__(self) -> str:
        char_data = [
            [colored("NAME:",  "yellow"), self.name, "",
             colored("LEVEL:", "yellow"), self.level],
            [colored("HP:",    "yellow"), self.hp, "",
             colored("MAX_HP:","yellow"), self.max_hp],
            [colored("ATTUNEMENTS:", "yellow"),
             colored("Element", "cyan"),
             colored("Turns", "cyan"),
             colored("Is Attuned", "cyan"),
             colored("Is Public", "cyan")
             ],
        ]
        for element, data in self.attunements.items():
            char_data.append([
                "",
                colored(element.upper(), "green"),
                data['turns'],
                data['is_attuned'],
                data['is_public']
            ])
        char_data.append([
            colored("ATTUNEMENTS:", "yellow"),
            colored("Status", "cyan"),
            colored("Turns", "cyan"),
            colored("Ignores", "cyan"),
            colored("Is Immune", "cyan"),
        ])
        for status, data in self.statuses.items():
            char_data.append([
                "",
                colored(status.upper(), "green"),
                data['turns'],
                data['ignores'], 
                data['is_immune']
            ])
        char_data.extend([
            [colored("PRIORITY:",    "yellow"), self.has_priority, "",
             colored("SPEED:",       "yellow"), self.speed],
            [colored("HEAT:",        "yellow"), self.heat, "", 
             colored("CURSE RISK:",  "yellow"), self.curse_risk],
            [colored("IS ELITE:",    "yellow"), self.is_elite, "", 
             colored("ELITES SLAIN:","yellow"), self.elites_slain],
            [colored("ITER MOD:",    "yellow"), self.iter_mod, "",
             colored("LASTDMGTAKEN:","yellow"), self.last_damage_taken],
            #[colored("MOVES:",       "yellow")],
            #[colored("  ACTIVE:",    "green"),
            # "Move","Type","Element"]
        ])
        #for move in self.moves['active']:
        #    char_data.append(
        #    ["", colored(move.name.upper(), "green"),
        #     move.type,
        #     move.element
        #    ])
        return(tabulate(char_data, tablefmt = "fancy_grid"))

    #--- Basic Functions

    # Calculation
    def calculate_damage(self, damage_element, amount) -> int:
        matches = [
            { "key": "weak_to",  "value": 0 },
            { "key": "resists",  "value": 0 },
            { "key": "immune_to","value": 0 },
            { "key": "absorbs",  "value": 0 }]
        for element in self.attunements:
            if element['is_attuned']:
                for match in matches:
                    if damage_element in globals.ELEMENTS[element['name']][match['key']]:
                        match['value'] += 1
        # Absorbs
        if matches[-1]['value'] > 0:
            amount = matches[-1]['value']
            self.heal(amount, element='none')
            return 0
        # Immune_To
        elif matches[-2]['value'] > 0:
            return 0
        # Standard
        else:
            damage = amount 
            damage += matches[-3]['value']
            damage -= matches[-4]['value']
            return max(0, damage)

    def calculate_speed(self) -> int:
        speed = self.speed + self.chosen_move['speed']
        if self.statuses['quick']['turns']:
            speed += 1
        if self.statuses['slow']['turns']:
            speed -= 1
        return speed

    # Damage
    def take_damage(self, amount) -> int:
        if self.ignores_damage:
            return 0
        else:
            self.last_damage_taken = amount
            self.total_damage_taken += amount
            self.hp = max(0, self.hp - amount)
            return self.hp

    def heal(self, amount, element) -> int:
        if element == "plant" and self.attunements['fire']['is_attuned']:
            amount += 1
        self.hp = max(self.max_hp, self.hp + amount)
        return self.hp

    # Attunement
    def attune_to(self, element):
        if not self.attunements[element]['is_attuned']:
            self.attunements[element]['is_attuned'] = True
        if not self.attunements[element]['is_public']:
            self.attunements[element]['is_public'] = True

    def negate_attune(self, element):
        if self.attunements[element]['is_attuned']:
            self.attunements[element]['is_attuned'] = False
        if not self.attunements[element]['is_public']:
            self.attunements[element]['turns'] = 0
            self.attunements[element]['is_public'] = True

    def spend_attune(self, element) -> int:
        spent = 0
        if not self.attunements[element]['is_public']:
            self.attunements[element]['is_public'] = True
        if self.attunements[element]['is_attuned']:
            spent += self.attunements[element]['turns']
            self.attunements[element]['turns'] = 0
            self.attunements[element]['is_attuned'] = False
        return spent

    # Status Effects
    def gain_status(self, status, amount):
        if self.statuses[status]['immune_to']:
            print(f"{self.name} is immune to {status}. No Turns Added.")
        else:
            self.statuses[status]['turns'] += amount
            if self.statuses[status]['turns'] > self.statuses[status]['max']:
                if status == 'burn':
                    over = self.statuses[status]['turns'] 
                    over -= self.statuses[status]['max']
                    self.burn_out(over)
                elif status == 'wound':
                    self.thousand_cuts()
                else:
                    self.statuses[status]['turns'] = self.statuses[status]['max']

    def lose_status(self, status, amount):
        self.statuses[status]['turns'] = max(self.statuses[status]['turns'] - amount, 0)

    def negate_status(self, status):
        if self.statuses[status]['turns'] > 0:
            self.statuses[status]['turns'] = 0

    # Change Move Location
    def bank_move(self, move):
        if move in self.moves['active']:
            self.moves['banked'].append(move)
            self.moves['active'].remove(move)
        else:
            print(f"{move} is already banked. Skipping Banking Effect.")

    def unbank_move(self, move):
        if move in self.moves['banked']:
            self.moves['active'].append(move)
            self.moves['banked'].remove(move)
        else:
            print(f"{move} is already active. Skipping Unbank Effect.")

    # Status Immunity
    def gain_immune(self, status):
        self.statuses[status]['immune_to'] = True
        self.statuses[status]['turns'] = 0

    def negate_immune(self, status):
        self.statuses[status]['immune_to'] = False

    def check_wound_immunity(self):
        if self.hp == self.max_hp and self.statuses['wound']['is_immune']:
            self.statuses['wound']['is_immune'] = False
            return True
        else:
            return False

    # Status Ignorance
    def gain_ignorance(self, status, amount):
        if amount == 'max':
            self.statuses[status]['ignores'] = self.statuses[status]['max']
        elif isinstance(amount, int):
            self.statuses[status]['ignores'] += amount

    def lose_ignorance(self, status, amount):
        self.statuses[status]['ignores'] -= amount

    def negate_ignorance(self, status):
        self.statuses[status]['ignores'] = 0

    # Elemental Specials
    def burn_out(self, amount):
        damage = self.calculate_damage('fire', amount)
        if not self.statuses['burn']['ignores']:
            self.take_damage(damage)
        self.statuses['burn']['turns'] = 0
        self.statuses['anger']['turns'] += 1

    def open_wounds(self) -> int:
        i = self.statuses['wound']['turns']
        taken = 0
        while i != 0:
            if not self.statuses['wound']['ignores']:
                damage = self.calculate_damage('vital', 1)
                self.take_damage(damage)
                taken += damage
            i -= 1
        self.statuses['wound']['turns'] = 0
        self.statuses['wound']['is_immune'] = True
        return taken

    def thousand_cuts(self):
        if not self.statuses['wound']['ignores']:
            self.hp = 0

    # Heat
    def gain_heat(self, amount) -> bool:
        if self.heat == 6:
            self.heat = amount
            return True
        elif self.heat + amount > 6:
            self.heat += amount - 6
            return True
        else:
            self.heat += amount
            return False

    def roll_heat(self) -> bool:
        check = random.randint(1,6)
        if self.heat < check:
            return False
        else:
            return True

    # Cooldown
    def apply_cooldown(self, move_name, location):
        for move in self.moves[location]:
            if (move['name']).strip().lower() == move_name.strip().lower():
                move['on_cooldown'] = move['cooldown']

    def reduce_cooldown(self, amount, move_name, location):
        for move in self.moves[location]:
            if (move['name']).strip().lower() == move_name.strip().lower():
                move['on_cooldown'] -= amount

    def negate_cooldown(self, move_name, location):
        for move in self.moves[location]:
            if (move['name']).strip().lower() == move_name.strip().lower():
                move['on_cooldown'] = 0

    # Charge
    def restore_charge(self, move_name, location):
        for move in self.moves[location]:
            if (move['name']).strip().lower() == move_name.strip().lower():
                move['on_charge'] = move['charge']

    def apply_charge(self, amount, move_name, location):
        for move in self.moves[location]:
            if (move['name']).strip().lower() == move_name.strip().lower():
                move['charge'] = amount
                move['on_charge'] = amount

    def reduce_charge(self, amount, move_name, location):
        for move in self.moves[location]:
            if (move['name']).strip().lower() == move_name.strip().lower():
                move['on_charge'] -= amount

    def negate_charge(self, move_name, location):
        for move in self.moves[location]:
            if (move['name']).strip().lower() == move_name.strip().lower():
                move['on_charge'] = 0

    # Curse
    def roll_curse(self):
        check = random.randint(1,10)
        if self.curse_risk < check:
            return False
        else:
            self.statuses['curse']['turns'] = min(
                self.statuses['curse']['turns'] + 3,
                self.statuses['curse']['max'])
            return True

    def take_curse(self):
        self.max_hp -= 1
        self.hp = min(self.hp, self.max_hp)

    #--- Variable Requests

    def check_turns_attuned_to(self, element) -> int:
        return self.attunements[element]['turns']

    def check_attunements(self) -> tuple:
        value = 0
        elements = []
        for element, data in self.attunements.items():
            if data['is_attuned']:
                value += 1
                elements.append(element)
        return value, elements

    def check_statuses(self) -> tuple:
        value = 0
        statuses = []
        for status, data in self.statuses.items():
            if data['turns'] > 0:
                value += 1
                statuses.append(status)
        return value, statuses








#--- Debug Prompt ---
player = Character("test character")
print(player)
