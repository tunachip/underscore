from globals        import ELEMENTS
from character      import Character
from upgrade        import Upgrade
from utils          import clear_screen, clear_lines
from loader         import DataParser
from termcolor      import colored
import random
import time
import json
import copy

class Combat:
    """
    The scene where players engage in combat.
    Combat Character is initialized,
    An Enemy Encounter is drafted and initialized,
    Priority is Assigned at random, and then the loop begins.
    """
    def __init__(self, meta_player):
        self.turn: int = 1
        self.parser = DataParser()
        self.player = copy.deepcopy(meta_player)    # Creates a Perfect Copy of the Pre-Combat Player
        self.enemy  = self.draft_enemy(meta_player.level, meta_player.elite_risk)
        self.characters = [self.player, self.enemy]

    def draft_enemy(self, level, elite_risk) -> Character:
        is_elite = (elite_risk >= random.randint(1,10))
        encounter_name = self.parser.draft_encounter(level, is_elite)
        return self.parser.parse_data('encounter', encounter_name)



    def loop(self):
        while self.player.hp and self.enemy.hp:
        
            # 1. Decision Phase
            '''Characters Choose their Moves for Turn.'''



            for i, move in enumerate(self.player.active_moves):
                print(f"{i+1})" + 
                      colored(f" {move['name']}", 
                              f"{ELEMENTS[move['element']]['termcolor']}"))

            while True:
                move = int(input("\n> ").strip())

                if not move < len(self.player.active_moves):
                    self.player.chosen_move = self.player.active_moves[move-1]
                    clear_lines(len(self.player.active_moves) + 4)
                    break
                else:
                    print(colored("\nERROR: ", "red") +
                          f"'{move}' is not a Valid Choice")
                    time.sleep(3)
                    clear_lines(4)

            # 2. Choose Target (If Applicable)
            self.enemy.chosen_move['target'] = "opponent"
            enemy_target = self.enemy
            
            print(colored(f"Chosen Move:\n\n", "cyan") +
                f"{self.player.chosen_move['name']}  |  " +
                f"({self.player.chosen_move['type']})  |  " + 
                colored(f"{self.player.chosen_move['element']}\n", 
                f"{ELEMENTS[self.player.chosen_move['element']]['termcolor']}") +
                f"{self.player.chosen_move['description']}\n")
            
            if self.player.chosen_move['target'] == 'either':
                print(colored("Choose Target: \n", "yellow") +
                      f"1. {self.player.name} (player)\n" +
                      f"2. {self.enemy.name} (enemy)")

                while True:
                    target = int(input("\n> ").strip())

                    
                    if target == 1:
                        player_target = self.player
                        clear_lines(10)
                        break
                    elif target == 2:
                        player_target = self.enemy
                        clear_lines(10)
                        break
                    else:
                        print(colored("\nERROR: ", "red"),
                              end=f"'{target}' in not a Valid Choice")
                        time.sleep(3)
                        clear_lines(4)
            else:
                if self.player.chosen_move['target'] == 'caster':
                    player_target = self.player
                else:
                    player_target = self.enemy

            # 3. Turn Order Calculation
            print(colored(f"Calculating Turn Order...\n", "yellow"))
            if self.player.calculate_speed() > enemy.calculate_speed():
                turn_order = [self.player, self.enemy]
            else:
                turn_order = [self.enemy, self.player]

            # 4. Turn Execution
            for i, character in enumerate(turn_order):
                if i == 0:
                    print(colored("First Turn: ","green"),end = f"{character.name}\n\n")
                else:
                    print(colored("Second Turn: ","green"),end = f"{character.name}\n\n")

                # Pre-Action Damage-Based Status-Effects
                if character.statuses['regen']['turns']:
                    if character.statuses['regen']['ignores']:
                        print(f"{character.name} ignored the effects of Regen")
                    else:
                        amount = character.statuses['regen']['turns']
                        self.game_engine.heal_damage(amount, character, 'plant')
                        print(f"{character.name} healed '{amount}' from Regen")
                        if self.game_engine.check_wound_immunity(character):
                            print(f"{character.name} has lost Wound Immunity")
                
                if character.statuses['burn']['turns']:
                    if character.statuses['burn']['ignores']:
                        print(f"{character.name} ignored the effects of Burn")
                    else:
                        amount = self.game_engine.take_burn(1, character)
                        print(f"{character.name} took {amount} damage from Burn")
                        if self.game_engine.check_wound_immunity(character):
                            print(f"{character.name} has lost Wound Immunity")

                if character.statuses['decay']['turns']:
                    if character.statuses['decay']['ignores']:
                        print(f"{character.name} ignored the effects of Decay")
                    else:
                        amount = self.game_engine.take_decay(1, character)
                        if amount > 0:
                            character.curse_chance += 1
                            print(f"A curtain of inky mist surrounds {character.name}...")
                            print(self.game_engine.attempt_curse(character))

                if character.statuses['curse']['turns']:
                    if character.statuses['curse']['ignores']:
                        print(f"{character.name} ignored the effects of Curse")
                    else:
                        self.game_engine.deal_curse(character)
                        print(f"Tears of ash pour from {character.name}'s eye sockets...")
                        print(f"{character.name}'s Max HP has been Reduced by 1")

                if character.statuses['wound']['turns']:
                    if character.statuses['wound']['ignores']:
                        print(f"{character.name} ignored the effects of Wound")
                    else:
                        if character.hp < character.max_hp / 2:
                            print(f"{character.name}'s body convulses with vital growth...")
                            taken = self.game_engine.open_wounds(character)
                            if taken > 0:
                                if character.attunements['plant']['is_attuned']:
                                    print(f"Vine-wrapped bones lunge out from {character.name}'s Body")
                                else:
                                    print(f"Ribbons of flesh rupture across {character.name}'s Body")
                                print(f"{character.name} took {taken} damage from their wounds")

                # Action-Disqualifying Status Effects
                skips_execution = False

                if character.statuses['stun']['turns'] and character.chosen_move['type'] == 'attack':
                    if 'stun' in character.chosen_move.get('ignores', []):
                        print(f"{character.name} cast a Stun-Proof Attack!")
                    elif character.statuses['stun']['ignores']:
                        print(f"{character.name} ignored the effects of Stun")
                    else:
                        print(f"{character.name} is Stunned and cannot Attack")
                        skips_execution = True
            
                if character.statuses['anger']['turns'] and character.chosen_move['type'] == 'utility':
                    if 'anger' in character.chosen_move.get('ignores', []):
                        print(f"{character.name} cast an Anger-Proof Utility!")
                    elif character.statuses['anger']['ignores']:
                        print(f"{character.name} ignored the effects of Anger")
                    else:
                        print(f"{character.name} loses focus to their Anger")
                        skips_execution = True
            
                if character.statuses['sleep']['turns']:
                    if 'sleep' in character.chosen_move.get('ignores', []):
                        print(f"{character.name} cast a Sleep-Proof Move!")
                    elif character.statuses['sleep']['ignores']:
                        print(f"{character.name} ignored the effects of Sleep")
                    else:
                        print(f"{character.name} is fast asleep...")
                        skips_execution = True

                if skips_execution:
                    print(f"{character.name}'s Turn was Skipped per Status-Based Disqualification!!")
                    continue

                # Move Logic Execution
                if character.char_type == 'enemy':
                    target = enemy_target
                else:
                    target = player_target

                print(f"{character.name} is casting '{character.chosen_move['name']}'",end="")
                if character.chosen_move['target'] in ['caster', 'opponent']:
                    print(f" targeting '{character.chosen_move['target']}'")
                else:
                    print(".")
                
                self.move_executor.execute_move(character.chosen_move, character, target)

            # Adjust Variables
            self.turn += 1
            for i, character in enumerate(turn_order):
                for element in character.attunements:
                    if element['is_attuned']:
                        character.attunements[element]['turns'] += 1
                for status in character.statuses:
                    if status['turns'] > 0:
                        character.statuses[status]['turns'] -= 1
                    if status['ignores'] > 0:
                        character.statuses[status]['ignores'] -= 1
                if character.has_priority:
                    character.has_priority = False
                else:
                    character.has_priority = True

        victory = False
        if self.player.hp > 1:
            victory = True

        if not victory:
            print(f"{self.enemy.name} defeated {self.player.name}!")
            input("\n\nThrow another body on the stockpile of history...")
            return f"Player Died at Level {self.player.level}"
        else:
            print(f"{self.player.name} defeated {self.enemy.name}!")
            time.sleep(2)
            print("\n\n\nThat's You! Be Happy!\n")
            time.sleep(5)
            
            clear_screen()
            upgrade = Upgrade(self.meta_player, self.enemy)
            print("Your Eyes Linger towards your Foe's Fresh Corpse...\n")
            time.sleep(3)

