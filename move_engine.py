from character import Character
from combat import Combat

class MoveEngine:
    """
    This is the Engine for Processing and Executing Move Logic.
    It has yet to be tested and is an experimental feature.
    """
    def __init__(self, caster, target, combat, move_data):
        self.caster:Character   = caster    # 
        self.target:Character   = target    # 
        self.combat:Combat      = combat    # 
        self.move_data: dict    = move_data # 
        self.variables: dict = {}           # 

    def execute(self):
        self._execute_phase('pre-iter')
        iters = self.move_data['base_iters'] + self.caster.iter_mod
        while iters > 0:
            self._execute_phase('iterable')
            iters -= 1
        self._execute_phase('post-iter')

    def _execute_phase(self, phase):
        for effect in self.move_data.get('effects', {}).get(phase, []):
            self._execute_effect(effect)

    def _execute_effect(self, effect):
        host = self._get_host(effect.get('host'))
        function_name = effect.get('function')
        args = self._resolve_args(effect.get('args', {}))        
        if hasattr(host, function_name):
            function = getattr(host, function_name)
            result = function(**args)
            self._store_return_values(effect.get('returns', {}), result)

    def _get_host(self, host_name):
        if host_name == 'caster':
            return self.caster
        elif host_name == 'target':
            return self.target
        elif host_name == 'combat':
            return self.combat
        return None

    def _resolve_args(self, args):
        resolved_args = {}
        for key, value in args.items():
            if isinstance(value, str) and value.startswith('$_'):
                resolved_args[key] = self._get_variable(value[2:])
            else:
                resolved_args[key] = value
        return resolved_args

    def _get_variable(self, variable_name):
        if variable_name in self.variables:
            return self.variables[variable_name]
        elif variable_name in self.move_data:
            return self.move_data[variable_name]
        return None

    def _store_return_values(self, returns, result):
        if returns and result is not None:
            for var_name, _ in returns.items():
                if var_name.startswith('$_'):
                    self.variables[var_name[2:]] = result

