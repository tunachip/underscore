from _base import BaseState

class Upgrade(BaseState):

    def __init__(self):
        """
        Called on FSM Initialization.
        'game': Main Object for Data Persistence Across States.
        """
        super().__init__()
        self.title = "Underscore"

    def enter(self, **kwargs):
        """
        Called on Entry.
        Used to Initialize Instances of Scene.
        """
        pass

    def exit(self):
        """
        Called on Exit.
        Used to Clean Up for Transition to Next State.
        Saves Data, Clears Screen.
        """
        pass

    def update(self, key):
        """
        Called Each Game Loop.
        Used to for State Unique Logic.
        Sets up Variables for 'Draw'
        'key': Key Pressed by User, per Blessed Library
        """
        if key:
            pass

    def draw(self, term):
        """
        Called after Update Each Game Loop.
        Used for Drawing Content to the Terminal.
        'term': Blessed Terminal Object
        """
        term.clear()
        with term.location(x = (term.width - len(self.title)) // 2, y = term.height //2):
            print(term.bold(self.title))
