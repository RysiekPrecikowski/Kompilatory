class Memory:

    def __init__(self, parent=None):  # memory name
        self.dict = dict()
        self.parent = parent

    def has_key(self, name):  # variable name
        if name in self.dict:
            return True
        if self.parent == None:
            return False
        return self.parent.has_key(name)

    def get(self, name):  # gets from memory current value of variable <name>
        if name in self.dict:
            return self.dict[name]
        if self.parent == None:
            return None
        return self.parent.get(name)

    def put(self, name, value):  # puts into memory current value of variable <name>
        if self.parent and self.parent.has_key(name):
            self.parent.put(name, value)
        else:
            self.dict[name] = value


class MemoryStack:

    def __init__(self, memory=None):  # initialize memory stack with memory <memory>
        self.stack = []

    def push(self, memory):  # pushes memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):  # pops the top memory from the stack
        return self.stack.pop()
