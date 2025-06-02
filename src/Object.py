from OBJ import OBJ


class Object(OBJ):
    def __init__(self, filename, position, swapyz=False):
        super().__init__(filename, swapyz)
        self.position = position
