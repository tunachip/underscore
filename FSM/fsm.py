class State:
    def enter(self, **kwargs):
        pass

    def exit(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

    def handle_input(self, user_input):
        pass

class FSM:
    def __init__(self):
        self.states = {}
        self.current_state = None

    def register(self, new_state_name, new_state_object):
        self.states[new_state_name] = new_state_object

    def change(self, state_name, **kwargs):
        if self.current_state:
            self.current_state.exit()
        self.current_state = self.states.get(state_name)
        if self.current_state:
            self.current_state.enter(**kwargs)

    def update(self):
        if self.current_state:
            self.current_state.update()

    def render(self):
        if self.current_state:
            self.current_state.render()

    def handle_input(self, user_input):
        if self.current_state:
            return self.current_state.handle_input(user_input)
