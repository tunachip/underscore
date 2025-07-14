import os
import csv
import random
from termcolor import colored, cprint

#--- Global Variables
ELEMENT_REF: dict = {
    'water': { 
        'color':   4, 'icon': '🌊',
        'weak_to':   ['thunder', 'plant'],
        'resists':   ['stone'],
        'immune_to': [],
        'absorbs':   ['fire'],
    },
    'stone': { 
        'color': 136, 'icon': '🪨',
        'weak_to':   ['water', 'force'],
        'resists':   ['fire'],
        'immune_to': ['thunder'],
        'absorbs':   [],
    },
    'fire': {
        'color': 196, 'icon': '🔥',
        'weak_to':   ['water', 'stone'],
        'resists':   [],
        'immune_to': [],
        'absorbs':   ['plant'],
    },
    'plant': { 
        'color': 112, 'icon': '🌿',
        'weak_to':   ['fire', 'vital'],
        'resists':   [],
        'immune_to': [],
        'absorbs':   ['water'],
    },
    'vital': { 
        'color': 198, 'icon': '❤️',
        'weak_to':   ['vital', 'force'],
        'resists':   [],
        'immune_to': [],
        'absorbs':   [],
    },
    'force': {
        'color':  36, 'icon': '💨',
        'weak_to':   ['thunder'],
        'resists':   ['vital'],
        'immune_to': ['stone'],
        'absorbs':   [],
    },
    'thunder':  { 
'color': 184, 'icon': '⚡',
        'weak_to':   ['stone'],
        'resists':   ['water'],
        'immune_to': ['force'],
        'absorbs':   [],
    },
}


STATUS_REF: dict = {
    'burn': {
        'color': 167, 'icon': '🔥',
        'deals': 'fire',
        'max_amount': 3,
        'at_max': 'burn_out',
    },
    'wound': {
        'color': 168, 'icon': '🩸',
        'deals': 'vital',
        'max_amount': 100,
        'at_max': 'flesh_flood',
    },
    'decay': {
        'color':  30, 'icon': '💀',
        'deals': 'force',
        'max_amount': 5,
        'at_max': 'ignore',
    },
    'regen': {
        'color':  70, 'icon': '✨',
        'deals': 'plant',
        'max_amount': 5,
        'at_max': 'ignore',
    },
    'slow': {
        'color': 172, 'icon': '🐌',
        'deals': 'none',
        'max_amount': 1,
        'at_max': 'ignore',
    },
    'quick': {
        'color': 229, 'icon': '⚡',
        'deals': 'none',
        'max_amount': 1,
        'at_max': 'ignore',
    },
    'angry': {
        'color': 174, 'icon': '😡',
        'deals': 'none',
        'max_amount': 3,
        'at_max': 'ignore',
    },
    'curse': {
        'color':  56, 'icon': '😈',
        'deals': 'none',
        'max_amount': 3,
        'at_max': 'ignore',
    },
    'stun': {
        'color': 184, 'icon': '😵',
        'deals': 'thunder',
        'max_amount': 3,
        'at_max': 'ignore',
    },
    'sleep': {
        'color': 107, 'icon': '💤',
        'deals': 'none',
        'max_amount': 3,
        'at_max': 'ignore',
    },
    'tough': {
        'color':  94, 'icon': '🛡️',
        'deals': 'none',
        'max_amount': 3,
        'at_max': 'ignore',
    },
    'strong': {
        'color':   1, 'icon': '💪',
        'deals': 'none',
        'max_amount': 3,
        'at_max': 'ignore',
    }
}


DECLARATIONS = {
    'element': [],
    'status': [],
    'move': []
}

for element in ELEMENTS:
    DECLARATIONS['element'].append(element)
for status in STATUSES:
    DECLARATIONS['status'].append(status)
for move in MOVES:
    DECLARATIONS['move'].append(move)


STARTING_BUILDS = {
    "mason": {
        "name": "mason",
        "elements": ["water", "stone"],
        "description": "Castaways of The Torrential Sea. Scalers of Coral Pillars. Vagrant Muts."
    },
    "cultivist": {
        "name": "cultivist",
        "elements": ["fire", "plant"],
        "description": "Kindlers of The Emberwald. Famished Husks wrapped in Pitch Stained Flesh."
    },
    "itinerant": {
        "name": "itinerant",
        "elements": ["force", "thunder"],
        "description": "Couriers of Cursed Relics. Barefoot Travelers of The Glassed Desert."
    },
    "bastard": {
        "name": "bastard",
        "elements": ["vital", "???"],
        "description": "Blood Dusted Devils. Orphans of God. Children of The Rupture."
    }
}

CONTINUE_PROMPTS = {
    "general": [
        "You take a deep breath. The reek of iron and rot fills your mouth as you push onward.",
        "Each step grinds bone underfoot, producing a fine dust what sticks to your blood soaked boots.",
        "Continuing your climb, The Mountain groans beneath. A low, tectonic shifting of settling flesh.",
        "Leaning into restless legs, you continue your ascent. The Black Sun stares down above, Drawing your hesitant gaze.",
        "The air grows thin, your throat clenches. A wave of suffocation renders everything motionless.",
        "A figure appears in the distance, a twisted shadow cast across the rippling mass of viscera.",
        "Black. Nothing more, Nothing less. You venture forward, a stillborn vessel scraping itself out of the worlds womb.",
        "A Breeze strikes your back, follwed by a harsh squeel. The sound of a thousand bones whistling, death's chorus",
        "As you face the march ahead, your heart grows restless. Echoing in the halls of your chest, footsteps of approaching death.",
    ],
    "mason": [],
    "cultivist": [],
    "itinerant": [],
    "bastard": [],
}

ENEMY_BARKS = {
    "general": [],
    "mason": [],
    "cultivist": [],
    "itinerant": [],
    "bastard": [],
}

#--- Objects ---

class MetaCharacter:

    def __init__(self, name, max_hp, level=1):
        self.name               = name
        self.max_hp             = max_hp
        self.hp                 = max_hp
        self.level              = level
        self.elites_slain       = 0
        self.blessing_burden    = 0
        self.curse_threat       = 0
        self.is_elite           = False

        self.attunements = {
            'water':    { 'turns': 0, 'public': False },
            'stone':    { 'turns': 0, 'public': False },
            'fire':     { 'turns': 0, 'public': False },
            'plant':    { 'turns': 0, 'public': False },
            'vital':    { 'turns': 0, 'public': False },
            'force':    { 'turns': 0, 'public': False },
            'thunder':  { 'turns': 0, 'public': False },
        }

        self.statuses = {
            'quick':    { 'turns': 0, 'immune_to': False, 'ignores': 0 }
            'slow':     { 'turns': 0, 'immune_to': False, 'ignores': 0 }
            'regen':    { 'turns': 0, 'immune_to': False, 'ignores': 0 }
            'burn':     { 'turns': 0, 'immune_to': False, 'ignores': 0 }
            'decay':    { 'turns': 0, 'immune_to': False, 'ignores': 0 }
            'wound':    { 'turns': 0, 'immune_to': False, 'ignores': 0 }
            'stun':     { 'turns': 0, 'immune_to': False, 'ignores': 0 }
            'anger':    { 'turns': 0, 'immune_to': False, 'ignores': 0 }
            'sleep':    { 'turns': 0, 'immune_to': False, 'ignores': 0 }
            'strong':   { 'turns': 0, 'immune_to': False, 'ignores': 0 }
            'tough':    { 'turns': 0, 'immune_to': False, 'ignores': 0 }
            'curse':    { 'turns': 0, 'immune_to': False, 'ignores': 0 }
        }

        self.active_moves = []
        self.banked_moves = []
        self.bound_moves  = []
        self.turn_history = []

class CombatCharacter:

    def __init__(self, MetaCharacter):
        self.name               = MetaCharacter.name
        self.max_hp             = MetaCharacter.max_hp
        self.hp                 = MetaCharacter.max_hp
        self.level              = MetaCharacter.level
        self.elites_slain       = MetaCharacter.elites_slain
        self.blessing_burden    = MetaCharacter.blessing_burden
        self.curse_threat       = MetaCharacter.curse_threat
        self.is_elite           = MetaCharacter.is_elite
        self.priority           = False
        self.speed              = 3

        self.attunements        = MetaCharacter.attunements
        self.statuses           = MetaCharacter.statuses
        self.active_moves       = MetaCharacter.active_moves
        self.banked_moves       = MetaCharacter.banked_moves
        self.bound_moves        = MetaCharacter.bound_moves
        self.turn_history       = MetaCharacter.turn_history

class Combat:

    def __init__(self, with_elite=False):
        self.turn               = 0
        self.declared           = {}
        self.with_elite         = with_elite

#--- Screens ---








#--- Game Logic ---

def calculate_damage(base_damage, element, target):
    damage = base_damage
    damage_type = ELEMENTS[element]
    if damage > 0:
        for element in target.attuned:
            attuned_element = ELEMENTS[element]
            if element['turns'] > 0 and damage_type in attuned_element['weak_to']:
                damage += 1
         for element in target.attuned:
            attuned_element = ELEMENTS[element]
            if element['turns'] > 0 and damage_type in attuned_element['resists']:
                damage -= 1   
        for element in target.attuned:
            attuned_element = ELEMENTS[element]
            if element['turns'] > 0 and damage_type in attuned_element['immune_to']:
                damage = 0
        for element in target.attuned:
            attuned_element = ELEMENTS[element]
            if element['turns'] > 0 and damage_type in attuned_element['absorbs']:
                damage = -1
    return damage

def check_wound(character):
    if character.hp == character.max_hp and character.statuses['wound']['immune'] == True:
        character.statuses['wound']['immune'] = False
        wound_restored = True
    else:
        wound_restored = False
    return wound_restored

def combat(meta_player):

    # Load Enemy Data
    encounter_data = load_encounter(player.level, player.blessing_burden)
    with open('data/encounters.csv', 'r') as f:
        reader = csv.reader(f)
        encounters = list(reader)

    elite_risk = random.randint(1,10)

    if player.blessing_burden < elite_risk:
        possible_encounters = [e for e in encounters[1:] if int(e['level']) == player_level and not bool(e['is_elite'])]
    
    elif player.blessing_burden == elite_risk:
        # Fallen Player Encounter logic
    
    elif player.blessing_burden > elite_risk:
        possible_encounters = [e for e in encounters[1:] if int(e['level']) == player_level and bool(e['is_elite'])]

    encounter_data = random.choice(possible_encounters)

    if not encounter_data:
        print(colored("ERROR: ", "red"),end= "No Encounter Data Found")
        return

    # Init Player Combat-Character
    player = Character(meta_player['name'])

    # Init Enemy
    enemy = Character(encounter_data['name'], int(encounter_data['max_hp']))
    enemy.active_moves = encounter_data['move_1', 'move_2', 'move_3', 'move_4']
    enemy.banked_moves = encounter_data['banked_move_1', 'banked_move_2']

    # Init Combat
    with_elite = enemy['is_elite']
    combat = Combat(with_elite)
    gains_priority = random.choice['player', 'enemy']

    # Players always have priority during 'Elite' Combats
    if combat['with_elite']:
        gains_priority = 'player'

    gains_priority['has_priority'] = True

    # Black Screen
    # Print ENEMY BARK
    # Start Printing Combat Screen

    while player.hp > 0 and enemy.hp > 0:
        combat['turn'] += 1

        # DECISION PHASE
        print("Choose Move: ")
        for i, move_name in enumerate(player.active_moves):
            print(f"{i+1}) {move_name}")
        chosen = False
        while not chosen:
            choice = input("> ")
            player.chosen_move = player.active_moves[int(choice)-1]
            print(f"{player.chosen_move['description']}")
            if player.chosen_move['target'] == "choose":
                print("Choose Target:")
                print(f"1) {player.name}  (self)")
                print(f"2) {enemy.name}  (enemy)")
                target = int(input("> ").strip())
                player.chosen_move['target'] = "enemy"
                if target == 1:
                    player.chosen_move['target'] = "player"

        enemy.chosen_move = enemy.move_history[turn]

        # TURN ORDER CALCULATION
        turn_order = [player, enemy]
        speeds = []
        for character in turn_order:
            speed = character.speed + int(character.chosen_move['speed'])
            if character.statuses['quick']['turns'] > 1:
                speed += 1
            if character.statuses['slow']['turns'] > 1:
                speed -= 1
            speeds.append(speed)

        if speeds[0] < speeds[1]:
            turn_order = [enemy, player]


        # EXECUTION
        for character in turn_order:
            regen = character.statuses['regen']
            if regen['turns'] > 0:
                if not regen['ignores']:
                    heal = regen['turns']
                    if character.attunements['fire']['turns'] > 0:
                        heal += 1
                    if character.hp + heal > character.max_hp:
                        heal = character.max_hp - character.hp
                    character.hp += heal
                    print(f"{character.name} healed '{heal}' from regen")
                    wound_restored = check_wound_immunity(character)
                    if wound_restored:
                        print(f"{character.name} lost wound immunity.")
                else:
                    print(f"{character.name} ignored the effects of regen.")

            if character['burn']['turns'] > 0:
                if not character['burn']['ignores']:
                    if character['burn']['turns'] > 2:
                        base_damage = 3
                        character.statuses['burn']['turns'] = 0
                        character.statuses['anger']['turns'] += 1
                        burnt_out = True
                    else:
                        base_damage = 1
                    burn_damage = calculate_damage(base_damage, 'fire', character)
                    character.hp -= burn_damage
                    print(f"{character.name} took '{burn_damage}' damage from their burns")
                    if burnt_out:
                        print(f"{character.name} gained 1 anger from burn-out.")
                    wound_restored = check_wound_immunity(character)
                    if wound_restored:
                        print(f"{character.name} lost wound immunity.")
                else:
                    print(f"{character.name} ignored the effects of their burns.")

            if character['decay']['turns'] > 0:
                if not character['decay']['ignores']:
                    character.curse_threat += 1
                    if character.curse_threat > 10:
                        character.curse_threat = 10
                    base_damage = 1
                    decay_damage = calculate_damage(base_damage, 'force', character)
                    character.hp -= decay_damage
                    print(f"{character.name} took '{decay_damage}' damage from their decay")
                    wound_restored = check_wound_immunity(character)
                    if wound_restored:
                        print(f"{character.name} lost wound immunity.")
                else:
                    print(f"{character.name} ignored the effects of their decay.")

            if character['wound']['turns'] > 0:
                if not character['wound']['ignores']:
                    if character.hp < character.max_hp / 2:
                        base_damage = 1
                        iterations = wound['turns']
                        wound_damage = 0
                        while iterations > 0:
                            wound_damage += calculate_damage(base_damage, 'vital', character)
                            iterations -= 1
                        character.hp -= wound_damage
                        character.statuses['wound']['turns'] = 0
                        character.statuses['wound']['immune_to'] = True
                        print(f"{character.name} took '{wound_damage}' damage from their wounds")
                    wound_restored = check_wound_immunity(character)
                    if wound_restored:
                        print(f"{character.name} lost wound immunity.")
                else:
                    print(f"{character.name} ignored the effect of their wounds.")


            if character.hp < 0:
                print(f"{character.name} has fallen to Damage-Based Status Effects")
                break

            skip_to_variable_adjustment = False
            while not skip_to_variable_adjustment:

                if character['stun']['turns'] > 0 and character.chosen_move['type'] == 'attack':
                    if character['stun']['ignores']:
                        print(f"{character.name} ignored the effects of their stun.")
                    else:
                        print(f"{character.name} is stunned and cannot attack.")
                        skip_to_variable_adjustment = True

                if character['anger']['turns'] > 0 andcharacter.chosen_move['type'] == 'utility':
                    if character['anger']['ignores']:
                        print(f"{character.name} ignored the effects of their anger.")
                    else:
                        print(f"{character.name} is angry and cannot use utility moves.")
                        skip_to_variable_adjustment = True

                if character['sleep']['turns'] > 0:    
                    if not character.chosen_move['ignores'] == 'sleep':
                        if character['sleep']['ignores']:
                            print(f"{character.name} ignored the effects of their sleep.")
                        else:
                            print(f"{character.name} is angry and cannot use utility moves.")
                            skip_to_variable_adjustment = True
                    else:
                        print(f"{character.name} used the Sleep-Proof Move '{character.chosen_move}'.")

                # If no skips, continue to declarations
                continue

            if character['chosen_move']['declarations']:
                for declaration in character['chosen_move']['declarations']:
                    if character == player:
                        declared = ""
                        while declared not in DECLARATIONS[declaration['type']]:
                            print(f"Declare a {declaration['type']}: ")
                            declared = input("> ")  # Ideally we could use a fuzzy-finder here
                            declared = declared.strip()
                            print(f"'{declared}' does not belong to the '{declaration['type']}' type list.")
                    else:
                        for historical_declaration in character['chosen_move']['declarations']:
                            declaration = historical_declaraction
                    new_declaration = {
                        'move_name':    move_name,
                        'type':         declaration['type'],
                        'trigger':      DECLARATIONS['type']['trigger'],
                    }
                    combat.declarations.append(new_declaration)

            # Trim the Move Name to get the function name
            move_function = character.chosen_move['name'].strip()
            # Define Moves Library
            moves_lib = sys.modules{__moves__]
            # Call the function from the Moves Library using name
            function_call = getattr(moves_lib, move_function)
            
            if callable(function_call):
                function_call(character) 
            # Needs Full Character for Damage Modifiers + Iters Value
            # chosen_move dict on character passes the target info

            # ADJUST VARIABLES
            for element in character.attunements.items():
                if element['turns'] > 0:
                    character.attunements[element]['turns'] += 1
            for status in character.statuses.items():
                if status['turns'] > 0 and status != "wound":
                    character.statuses[status]['turns'] -= 1
                if status['ignores'] > 0:
                    character.statuses[status]['ignores'] -= 1

        
        # END OF EXECUTIONS
        if player.priority:
            player.priority = False
            enemy.priority = True
        else:
            player.priority = True
            enemy.priority = False

    # end of combat loop
