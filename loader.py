#!!!   EXPERIMENTAL, UNTESTED
from character import Character
import json
import os
import pandas as pd

class DataParser:
    def __init__(self):
        self.moves:list         = []
        self.encounters:list    = []
        self.blessings:list     = []
        self.startingbuilds:list= []

    def convert_json(self, file_path):
        with open(file_path, 'r') as f:
            return json.load(f)

    def load_json(self, file_type, name):
        file_path = os.path.join('Data', f"{file_type.lower()}s", f"{name}.json")
        return self.convert_json(file_path)

    def draft_encounter(self, level, is_elite, scope=1):
        """
        Queries the Encounter CSV File for Encounter Names
        """
        file_path = os.path.join("Data","encounters","encounters.csv")
        df = pd.read_csv(file_path)
        if is_elite:
            filtered_df = df[(df['level'] == level) & (df['is_elite'] == "True")]
        else:
            filtered_df = df[(df['level'] == level)]

        if scope == 1:
            encounter = filtered_df.sample(n=1)
            return encounter['name']
        elif scope == "all":
            self.encounters = filtered_df.tolist()
            return self.encounters
        else:
            return None

    def parse_data(self, file_type, name):
        data = self.load_json(file_type, name)
        if not data:
            return None
        match file_type:
            case 'move':
                pass
            case 'encounter':
                name            = data.name
                level           = data.level
                max_hp          = data.max_hp
                hp              = data.hp
                blessings       = data.blessings
                turn_history    = data.turn_history
                moves           = data.moves
                is_elite        = False
                if data.is_elite == "True":
                    is_elite = True
                return Character(name,level,max_hp,hp,is_elite,blessings,turn_history,moves)

            case 'blessing':
                pass
            case 'startingbuild':
                pass
