zero_str = "00000000000000000000000000000000"

class element(object):
    """docstring for element"""

    def __init__(self, width):
        assert isinstance(width, int), "Width must be an integer"
        self.width = width
        self.displayable = True
        self.tickable = False
        self.updatable = False
    def solve(self): # OVERLOADED WHEN NEEDED
        return None
    def __str__(self):
        return str(bin(self.solve()))
################################################################################
################################################################################
################################################################################
class memory(element):
    """docstring for memory"""
    def __init__(self, width = 32):
        super(memory, self).__init__(width)
###
class register(memory):
    """docstring for register"""
    def __init__(self, width, obj = None, clk = None):
        super(register, self).__init__(width)
        self.value = 0
        self.obj = obj
        self.clk = clk
        self.updatable = True
    def setObj(self, obj):
        self.obj = obj
    def setClock(self, clock):
        self.clk = clock
    def update(self):
        if self.clk.solve() == 1:
            if isinstance(self.obj, element):
                self.value = self.obj.solve()
            else:
                self.value = self.obj
    def solve(self):
        return self.value

class wiring(element):
    """docstring for element"""
    def __init__(self, width = 32):
        super(wiring, self).__init__(width)
###
class pin(wiring):
    """docstring for element"""
    def __init__(self, width, value = zero_str):
        super(pin, self).__init__(width)
        self.setValue(value)
    # 1 for output, 0 for input
    def setIO_State(self, state):
        self.IO_State = state
    def setValue(self, value):
        assert isinstance(value, str), "value must be a binary string"
        self.value = int(value, 2)
    def solve(self):
        return self.value
###
class probe(wiring):
    """docstring for probe"""
    def __init__(self, width, obj = None):
        super(probe, self).__init__(width)
        assert width == obj.width, "width of probe probedObj must be equal"
        self.setProbedObj(obj)
    def setProbedObj(self, obj):
        self.obj = obj
    def __probedObj(self):
        return self.obj.solve()
    def solve(self):
        return self.__probedObj()
###
class clock(wiring):
    """docstring for clock"""
    def __init__(self):
        super(clock, self).__init__(1)
        self.value = 0
        self.tickable = True
    def tick(self):
        self.value = 1 - self.value
    def solve(self):
        return self.value
###
class constant(wiring):
    """docstring for constant"""
    def __init__(self, width, value = zero_str):
        super(constant, self).__init__(width)
        self.setValue(value)
    def setValue(self, value):
        assert isinstance(value, str), "value must be a binary string"
        self.value = int(value, 2)
    def solve(self):
        return self.value
################################################################################
class gates(element):
    """docstring for element"""
    def __init__(self, inputs, width = 32):
        super(gates, self).__init__(width)
        self.inputs = inputs
        self.value = None
    def setInputs(self, *inputs):
        self.inputs = inputs
    def solve(self, op):
        if self.value == None:
            if isinstance(self.inputs[0], element):
                self.value = self.inputs[0].solve()
            else:
                self.value = int(self.inputs[0], 2)
        for item in self.inputs:
            if isinstance(item, element):
                toAnd = item.solve()
            else:
                toAnd = int(item, 2)
            self.value = op(self.value, toAnd)
        return self.value
###
class AND(gates):
    """docstring for AND"""
    def __init__(self, width, *inputs):
        super(AND, self).__init__(inputs, width)
    def solve(self):
        return super(AND, self).solve(lambda x, y: x & y)
###
class OR(gates):
    """docstring for AND"""
    def __init__(self, width, *inputs):
        super(OR, self).__init__(inputs, width)
    def solve(self):
        return super(OR, self).solve(lambda x, y: x | y)
###
class XOR(gates):
    """docstring for AND"""
    def __init__(self, width, *inputs):
        super(XOR, self).__init__(inputs, width)
    def solve(self):
        return super(XOR, self).solve(lambda x, y: x ^ y)
###
class NAND(gates):
    """docstring for AND"""
    def __init__(self, width, *inputs):
        super(NAND, self).__init__(inputs, width)
    def solve(self):
        return ~super(NAND, self).solve(lambda x, y: x & y)
###
class NOR(gates):
    """docstring for AND"""
    def __init__(self, width, *inputs):
        super(NOR, self).__init__(inputs, width)
    def solve(self):
        return ~super(NOR, self).solve(lambda x, y: x | y)
###
class NXOR(gates):
    """docstring for AND"""
    def __init__(self, width, *inputs):
        super(NXOR, self).__init__(inputs, width)
    def solve(self):
        return ~super(NXOR, self).solve(lambda x, y: x ^ y)
###
class NOT(gates):
    """docstring for AND"""
    def __init__(self, width, inputs):
        super(NOT, self).__init__(inputs, width)
        assert len(inputs) == 1, "Can only not a single input"
    def solve(self):
        if isinstance(self.inputs[0], element):
            super(NOT, self).value = ~self.inputs[0].solve()
        else:
            super(NOT, self).value = ~int(self.inputs[0], 2)
        return super(NOT, self).value
################################################################################
class plexers(element):
    """docstring for plexers"""
    def __init__(self):
        super(plexers, self).__init__()
################################################################################
class arithmetic(element):
    """docstring for plexers"""
    def __init__(self, op, inputs, width = 32):
        super(arithmetic, self).__init__(width)
        assert len(inputs) == 2, "only two inputs on arithmetic at a time"
        self.op = op
        self.inputs = inputs

    def solve(self):
        x = self.inputs[0]
        y = self.inputs[1]
        if isinstance(x, element):
            x = x.solve()
        if isinstance(y, element):
            y = y.solve()
        return self.op(x,y)
###
class adder(arithmetic):
    """docstring for adder"""
    def __init__(self, width, *inputs ):
        super(adder, self).__init__(lambda x, y: x + y, inputs, width)
    def solve(self):
        return super(adder, self).solve()
###
class subtracter(arithmetic):
    """docstring for adder"""
    def __init__(self, width, *inputs ):
        super(subtracter, self).__init__(lambda x, y: x - y, inputs, width)
    def solve(self):
        return super(subtracter, self).solve()
###
class multiplier(arithmetic):
    """docstring for adder"""
    def __init__(multiplier, width, *inputs ):
        super(multiplier, self).__init__(lambda x, y: x * y, inputs, width)
    def solve(self):
        return super(multiplier, self).solve()
###
class divider(arithmetic):
    """docstring for adder"""
    def __init__(self, width, *inputs ):
        super(divider, self).__init__(lambda x, y: x / y, inputs, width)
    def solve(self):
        return super(divider, self).solve()
###
class shift_left_logical(arithmetic):
    """docstring for adder"""
    def __init__(self, width, *inputs ):
        super(shift_left_logical, self).__init__(lambda x, y: x << y, inputs, width)
    def solve(self):
        return super(shift_left_logical, self).solve()
###
class shift_right_logical(arithmetic):
    """docstring for adder"""
    def __init__(self, width, *inputs ):
        super(shift_right_logical, self).__init__(lambda x, y: x >> y, inputs, width)
    def solve(self):
        return super(shift_right_logical, self).solve()
