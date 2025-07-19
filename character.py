import polars as pl
from termcolor import cprint

class MetaCharacter:

    def __init__(self, name):
        self.name:          str = name
        self.max_hp:        int = 10
        self.level:         int = 1
        self.elites_slain:  int = 0
        self.bless_burden:  int = 0
        self.attunements:   dict = {} # contains dicts
        self.statuses:      dict = {} # contains dicts
        self.active_moves:  list = [] # contains dicts
        self.banked_moves:  list = [] # contains dicts
        self.blessings:     list = [] # contains dicts

        for element in ELEMENTS:
            self.attunements[element] = {
                'turns': 0,
                'is_public': False,
                'is_attuned': False
            }

        for status in STATUSES:
            self.statuses[status] = {
                'turns': 0,
                'immune_to': False,
                'ignores': 0,
                'max_amount': STATUSES[status]['max_amount']
                }

        for blessing in self.blessings:
            if blessing['inits_attune'] in ELEMENTS:
                element = blessing['inits_attune']
                self.attunements[element]['turns'] = 1
            if blessing['inits_status'] in STATUSES:
                status = blessing['inits_status']
                status = int(blessing['inits_status_value'])
                self.statuses[status]['turns'] = sta

    def __str__(self):
        details = f"""
NAME:          {self.name}
LEVEL:         {self.level}
ELITES_SLAIN:  {self.elites_slain}
BLESS_BURDEN:  {self.bless_burden}

MAX_HP:        {self.max_hp}

ATTUNEMENTS:
    WATER:   {self.attunements['water']['turns']}
    STONE:   {self.attunements['stone']['turns']}
    FIRE:    {self.attunements['fire']['turns']}
    PLANT:   {self.attunements['plant']['turns']}
    VITAL:   {self.attunements['vital']['turns']}
    FORCE:   {self.attunements['force']['turns']}
    THUNDER: {self.attunements['thunder']['turns']}

STATUSES:
    QUICK:   {self.statuses['quick']['turns']}
    SLOW:    {self.statuses['slow']['turns']}
    REGEN:   {self.statuses['regen']['turns']}
    BURN:    {self.statuses['burn']['turns']}
    DECAY:   {self.statuses['decay']['turns']}
    WOUND:   {self.statuses['wound']['turns']}
    STUN:    {self.statuses['stun']['turns']}
    ANGER:   {self.statuses['anger']['turns']}
    SLEEP:   {self.statuses['sleep']['turns']}
    STRONG:  {self.statuses['strong']['turns']}
    TOUGH:   {self.statuses['tough']['turns']}
    CURSE:   {self.statuses['curse']['turns']}

ACTIVE_MOVES:
    1 )  {self.active_moves[0]['name']}\t|  {self.active_moves[0]['type']}  |  {self.active_moves[0]['element']}
    2 )  {self.active_moves[1]['name']}\t|  {self.active_moves[1]['type']}  |  {self.active_moves[1]['element']}
    3 )  {self.active_moves[2]['name']}\t|  {self.active_moves[2]['type']}  |  {self.active_moves[2]['element']}
    4 )  {self.active_moves[3]['name']}\t|  {self.active_moves[3]['type']}  |  {self.active_moves[3]['element']}

BANKED_MOVES:
    5 )  {self.banked_moves[0]['name']}\t|  {self.banked_moves[0]['type']}  |  {self.banked_moves[0]['element']}
    6 )  {self.banked_moves[1]['name']}\t|  {self.banked_moves[1]['type']}  |  {self.banked_moves[1]['element']}
"""
        return details


class CombatCharacter:

    def __init__(self, MetaCharacter):
        self.name: str          = MetaCharacter.name
        self.max_hp: int        = MetaCharacter.max_hp
        self.hp: int            = MetaCharacter.max_hp
        self.level: int         = MetaCharacter.level
        self.elites_slain: int  = MetaCharacter.elites_slain
        self.bless_burden: int  = MetaCharacter.bless_burden
        self.curse_chance: int  = 0
        self.has_priority: bool = False
        self.speed: int         = 3

        self.attunements: dict  = MetaCharacter.attunements
        self.statuses: dict     = MetaCharacter.statuses
        self.active_moves: list = MetaCharacter.active_moves
        self.banked_moves: list = MetaCharacter.banked_moves
        self.turn_history: list = []

class Enemy:

    def __init__(self, level, is_elite):

        enemy_csv_path = "data/csv/encounters.csv"
        enemy_df = pl.read_csv(enemy_csv_path)
        enemy_pool = enemy_df.filter(pl.col("level") == level)
        if not enemy_pool.is_empty():
            i = random.randint(0, len(enemy_pool) -1)
            enemy_data = enemy_pool.row(i, named=True)
        else:
            print("DEBUG: Enemy Pool Empty")

        self.name: str          = enemy_data['name']
        self.max_hp: int        = 1
        self.hp: int            = 1
        self.level: int         = level
        self.curse_threat: int  = 0
        self.has_priority: bool = False
        self.speed: int         = 3
        self.is_elite           = is_elite

        self.attunements: dict  = enemy_data['attunements']
        self.statuses: dict     = enemy_data['statuses']
        self.active_moves: list = enemy_data['active_moves']
        self.banked_moves: list = enemy_data['banked_moves']
        self.turn_history: list = enemy_data['turn_history']


