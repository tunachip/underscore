class BaseState:

    def __init__(self):
        """
        Called on FSM Initialization.
        'game': Main Object for Data Persistence Across States.
        """
        self.game = None

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
        pass

    def draw(self, term):
        """
        Called after Update Each Game Loop.
        Used for Drawing Content to the Terminal.
        'term': Blessed Terminal Object
        """
        pass
