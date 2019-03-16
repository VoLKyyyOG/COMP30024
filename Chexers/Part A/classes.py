#######################
#  Class definitions  #
#######################


""" Example
v1 = [1,2]
v2 = [-1,0]
Vector.add(v1, v2) # Outputs [0, 2]
Vector.sub(v1, v2) # Outputs [2, 2]
"""

class Vector():
    """Facilitates construction and smooth use of coordinates for pythonic code!"""
    @staticmethod
    def add(list_1, list_2):
        """Allows for "vector_1 + vector_2"""
        return [list_1[0] + list_2[0], list_1[1] + list_2[1]]

    @staticmethod
    def sub(list_1, list_2):
        """Allows for "vector_1 - vector_2"""
        return [list_1[0] - list_2[0], list_1[1] - list_2[1]]
