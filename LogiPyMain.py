import time
import LogiPy as lp

circuit_speed = .00001 # seconds
tick_count = 100

components = []
displayable = []
tickable = []
updatable = []
def main():
    init_components()
    for element in components:
        if element.tickable:
            tickable.append(element)
        if element.updatable:
            updatable.append(element)
    run()

def init_components():
    clk = lp.clock()
    components.append(clk)

    pin = lp.pin(8, "00000001")
    components.append(pin)

    r = lp.register(8)
    components.append(r)

    a = lp.adder(8, r, pin)
    components.append(a)

    r.setObj(a)
    r.setClock(clk)

    probe = lp.probe(8, r)
    components.append(probe)

def run():
    while True:
        for element in tickable:
            element.tick()
        for element in updatable:
            element.update()
        for element in components:
            print(element)
        time.sleep(circuit_speed)




main()
