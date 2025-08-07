#===============
#
#    COMBAT
#   FUNCTIONS
#
#===============

#---DAMAGE
def deal_damage(amount, target):
    if target.statuses['curse']['turns']: 
        deal_curse(target)
    target.hp -= amount
    if target.hp < target.max_hp / 2 and target.statuses['wound']['turns']:
        open_wounds(target)
    if target.hp > target.max_hp:
        target.hp = target.max_hp

def heal_damage(amount, target, element="none"):
    if element == "plant" and target.attunements['fire']['turns']:
        amount += 1
    target.hp += amount
    if target.hp > target.max_hp:
        target.hp = target.max_hp

#---ATTUNEMENTS
def make_attune(element, target):
    if not target.attunements[element]['is_public']:
        target.attunements[element]['is_public'] = True
    if not target.attunements[element]['is_attuned']:
         target.attunements[element]['is_attuned'] = True

def negate_attune(element, target):
    if not target.attunements[element]['is_public']:
        target.attunements[element]['is_public'] = True
    if target.attunements[element]['is_attuned']:
         target.attunements[element]['is_attuned'] = False
         target.attunements[element]['turns'] = 0

#---STATUSES
def apply_status(status, amount, target):
    if not target.statuses[status]['immune_to']:
        target.statuses[status]['turns'] += amount
        if target.statuses[status]['turns'] > target.statuses[status]['max_amount']:
            if status == "burn":
                over = target.statuses[status]['turns'] - target.statuses[status]['max_amount']
                burn_out(over, target)
            elif status == "wound"
                thousand_cuts(target)
            else:
                target.statuses[status]['turns'] = target.statuses[status]['max_amount']

def negate_status(status, target):
    if target.statuses[status]['turns']:
        target.statuses[status]['turns'] = 0

def reduce_status(status, amount, target):
    if target.statuses[status]['turns']:
        target.statuses[status]['turns'] -= amount

#---DECLARATIONS
def make_declare():
    pass

def negate_declare():
    pass

#---BINDING
def bind_move():
    pass

def unbind_move():
    pass

#---PUBLICITY
def make_public():
    pass

def make_secret():
    pass

#---BANKING
def bank_move(move, target):
    target.banked_moves.append(move)
    target.active_moves.remove(move)

def unbank_move(move, target):
    if len(target.active_moves) > 3:
        return    
    target.active_moves.append(move)
    target.banked_moves.remove(move)

#---IMMUNITY
def make_immune(status, target):
    target.statuses[status]['immune_to'] = True
    target.statuses[status]['turns'] = 0

def negate_immune(status, target):
    target.statuses[status]['immune_to'] = False

#---IGNORANCE
def make_ignorant(status, amount, target):
    if amount == "max":
        target.statuses[status]['ignores'] = target.statuses[status]['max_amount'] 
    elif isinstance(amount, int):
        target.statuses[status]['ignores'] += amount

def negate_ignorant(status, amount, target):
    if amount == "all":
        target.statuses[status]['ignores'] = 0
    elif isinstance(amount, int):
        target.statuses[status]['ignores'] -= amount

#---CALCULATIONS
def calculate_speed(character):
    # I could be stupid, but this looks like the correct method?
    if character.statuses['sleep']['turns'] or \
            character.statuses['stun']['turns'] and \
            character.chosen_move['type'] == "attack":
                return 0
    speed = character.speed
    if character.statuses['quick']['turns']:
        speed += 1
    if character.statuses['slow']['turns']:
        speed -= 1
    if "quick_move" in character.chosen_move.attributes:
        speed += 1
    if "slow_move" in character.chosen_move.attributes:
        speed -= 1 
    return speed

def calculate_damage(damage_element, base_damage, target):
    matches = {
            "weak_to": 0,
            "resists": 0,
            "immune_to": 0,
            "absorbs": 0,
        }
    for element in target.attunements:
        if element['is_attuned']:
            if damage_element in ELEMENTS[element]['weak_to']:
                matches['weak_to'] += 1
            elif damage_element in ELEMENTS[element]['resists']:
                matches['resists'] += 1
            elif damage_element in ELEMENTS[element]['immune_to']:
                matches['immune_to'] += 1
            elif damage_element in ELEMENTS[element]['absorbs']:
                matches['absorbs'] += 1

    if matches['absorbs']:
        base_heal = matches['absorbs']
        heal_damage(base_heal, target, element="none")
        return 0
    elif matches['immune_to']:
        return 0
    else:
        output = base_damage + matches['weak_to'] - matches['resists']
        if output > 0:
            return output

#---DISQUALIFIERS
def check_disqualifiers(character):
    move = character.chosen_move
    disqualifiers = {
        "sleep": "none", 
        "anger": "attack",
        "stun":  "utility",
    }
    for status, allowed in disqualifiers:
        if move['type'] != allowed:
            if character.statuses[status]['turns'] and \
                not character.statuses[status]['ignores'] and \
                status not in move["ignores"]:
                    return True
    return False

#---ELEMENTAL SPECIALS
def burn_out(amount, target):
    damage = calculate_damage('fire', amount, target)
    if not target.statuses['burn']['ignores']:
        deal_damage(damage, target)
    target.statuses['burn']['turns'] = 0
    target.statuses['anger']['turns'] += 1

def open_wounds(target):
    for target.statuses['wound']['turns']:
        damage = calculate_damage('vital', 1, target)
        if not target.statuses['wound']['ignores']:
            deal_damage(damage, target)
    target.statuses['wound']['turns'] = 0
    target.statuses['wound']['immune_to'] = True

def thousand_cuts(target):
    if not target.statuses['wound']['ignores']:
        target.hp = 0

def attempt_curse(target):
    curse_roll = random.randint(1,10)
    if not target.curse_chance < curse_roll:
        target.statuses['curse']['turns'] += 3
        if target.statuses['curse']['turns'] > target.statuses['curse']['max_amount']:
            target.statuses['curse']['turns'] = target.statuses['curse']['max_amount']

def deal_curse(target):
    target.max_hp -= 1
    if target.hp > target.max_hp:
        target.hp = target.max_hp

#===================
