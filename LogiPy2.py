str0 = "00000000000000000000000000000000"

class element(object):
    """docstring for element"""
    def __init__(self):
        super(element, self).__init__()
################################################################################
################################################################################
################################################################################
class wiring(element):
    """docstring for element"""
    def __init__(self, width = 32):
        super(wiring, self).__init__()
        self.width = width
###
class pin(wiring):
    """docstring for element"""
    def __init__(self, width = 32, value = str0):
        super(pin, self).__init__(width)
        self.setValue(value)

    # 1 for output, 0 for input
    def setIO_State(self, state):
        self.IO_State = state

    def setValue(self, value):
        assert isinstance(value, str) or isinstance(value, list)
        assert len(value) == width
        if isinstance(value, str):
            self.value = list(value)
        else:
            self.value = value

    def solve(self):
        return self.value
###
class probe(wiring):
    """docstring for probe"""
    def __init__(self, width = 32, obj = None):
        super(probe, self).__init__(width)
        self.setProbedObj(obj)

    def setProbedObj(self, obj):
        self.obj = obj

    def probedObj(self):
        return self.obj.solve()

    def solve(self):
        return self.probedObj()

    def display(self):
        print("".join(self.probedObj()))
###
class clock(wiring):
    """docstring for clock"""
    def __init__(self):
        super(clock, self).__init__(1)
        self.value = 0

    def tick(self):
        self.value = 1 - self.value

    def solve(self):
        return self.value

    def display(self):
        print(self.value)
###
class constant(wiring):
    """docstring for constant"""
    def __init__(self, width = 32, value = str0):
        super(constant, self).__init__(width)
        self.setWidth(width)
        self.setValue(value)

    def setWidth(self, width):
        assert isinstance(width, int)
        self.width = width

    def setValue(self, value):
        assert isinstance(value, str) or isinstance(value, list)
        if isinstance(value, str):
            self.value = list(value)
        else:
            self.value = value

    def solve(self):
        return self.value


################################################################################
class gates(element):
    """docstring for element"""
    def __init__(self, width = 32, *inputs):
        super(gates, self).__init__()
        self.width = width
        self.inputs = inputs
        self.value = None

    def setInputs(*inputs):
        self.inputs = inputs

class AND(gates):
    """docstring for AND"""
    def __init__(self, width = 32, *inputs):
        super(AND, self).__init__(width, inputs)

    def andop(self, and_in):
        if self.value == None:
            self.value = and_in
        else:
            temp = []
            for i in range(len(and_in)):
                if and_in[i] == self.value[i] and and_in == 1:
                    temp.append("1")
                else:
                    temp.append("0")
            self.value = temp
        return self.value

    def solve(self):
        if isinstance(self.inputs, str):
            self.inputs = list(self.inputs)
        for item in self.inputs:
            self.andop(item)

        return self.value




################################################################################
class plexers(element):
    """docstring for plexers"""
    def __init__(self):
        super(plexers, self).__init__()
################################################################################
class arithmetic(element):
    """docstring for plexers"""
    def __init__(self):
        super(arithmetic, self).__init__()
