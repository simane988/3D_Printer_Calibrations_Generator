import os

class GCodeProgram:



    def __init__(self):
        pass

    def linear_move(x: float, y: float, z: float, f: float):
        return f"G01 X{x} Y{y} Z{z} F{f}"
