import json

class move:

    def __init__(self, name):
        # Check if Move File in Moves Dir
        filepath = "/data/moves/" + name.strip().lower() + ".json"
        
        if filepath:
            data = json.loads(filepath)
        else:
            print("Move Not Found")
            break
        
        self.name           :str    = data.name
        self.type           :str    = data.type
        self.element        :str    = data.element
        self.base_damage    :int    = data.base_damage
        self.base_iters     :int    = data.base_iters
        self.attune_action  :str    = data.attune_action
        self.attune_element :str    = data.attune_element
        self.attune_target  :str    = data.attune_target
        self.damage_action  :str    = data.damage_action
        self.damage_element :str    = data.damage_element
        self.damage_target  :str    = data.damage_target
        self.ignores        :list   = data.ignores
        #   ignores = ["sleep"]
        self.attributes     :list   = data.attributes
        #   attributes = ["has_banked_effect"]
        self.functions      :list   = data.functions
        #   functions = [
        #   [0]: {
        #           "name"  :str
        #           "args"  :list
        #       },
        #   [1]: {
        #           "name"  :str
        #           "args"  :list
        #       },
        #   [2]: ...
        self.declarations   :list   = data.declarations
        #   declarations = [
        #   [0]: {
        #           "from_move" :str =  name
        #           "trigger"   :str
        #           "type"      :str
        #       },
        #   [1]: {
        #           "from_move" :str =  name
        #           "trigger"   :str
        #           "type"      :str
        #       },
        #   [2]: {...
        self.description    :str    = data.description
