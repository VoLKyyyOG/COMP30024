""" class.py

Implements a state class for missionary/cannibal problem

"""

POSSIBLE_ACTIONS = {
    False: [(0,-1),(-1,0),(-1,-1),(0,-2),(-2,0)], # On the left
    True: [(0,1),(1,0),(1,1),(0,2),(2,0)] # On the right
}

class State:
    def __init__(self, missionary, cannibal, side=False):
        self.missionary = missionary
        self.cannibal = cannibal
        self.side = side
        self.children = list()

    def __add__(self, other):
        """Allows addition of a state with a missionary/cannibal vector"""
        return State(self.missionary + other.missionary, \
                    self.cannibal + other.cannibal, \
                    not self.side)

    def __iadd__(self, other):
        """Allows state_inst += another_inst"""
        self = self.__add__(self, other)

    def  __str__(self):
        """String representation"""
        return f"{self.missionary}, {self.cannibal}, {self.side}"

    def __hash__(self):
        """Implements hash functionality for use in TT"""
        return hash((self.missionary, self.cannibal, self.side))

    def get_children(self, debug =  False):
        """Gets children for a given state"""
        for missionary, cannibal in POSSIBLE_ACTIONS[self.side]:
            child = self + State(missionary, cannibal)
            if debug:
                print("Evaluating: ", child)
            # Check valid numbers
            if (3 >= child.cannibal >= 0 and 3 >= child.missionary >= 0):
                # missionary are alone - this is ok
                if (child.missionary in (0,3)) or \
                (self.side == False and child.missionary >= child.cannibal) or \
                (self.side == True and child.missionary <= child.cannibal):
                    self.children.append(child)
        if debug:
            print("{self} >> Chosen moves: ", [str(i) for i in self.children])
        return self.children

    def evaluate(self):
        """Checks if goal has been reached"""
        return (self.missionary == self.cannibal == 0)
