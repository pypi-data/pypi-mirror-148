from ....structure import NoneAttribute

class NodeAttribute(NoneAttribute):

    def __init__(self, name, type) -> None:
        super().__init__()
        self.name = name
        self.type = type
