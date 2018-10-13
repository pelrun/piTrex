from migen import *

import pitrex


class PhaseShift(Module):
    def __init__(self, size, reset):
        self.count = Signal(size)
        self.reset = Signal()

        self.odomain = ClockDomain()

        ###

        self.comb += self.odomain.clk.eq(self.count[2])
        self.sync += self.reset.eq(reset)
        self.sync += self.count.eq(self.count + 1)
        self.sync += If(~self.reset & reset, self.count.eq(0))


class StateCounter(Module):
    """Counter with synchronous reset"""
    def __init__(self, size, reset):
        self.count = Signal(size)
        self.reset = Signal()

        ###

        #    self.comb += self.reset.eq(reset)
        self.sync += self.reset.eq(reset)
        self.sync += self.count.eq(self.count + 1)
        self.sync += If(~self.reset & reset, self.count.eq(0))

class Thingy(Module):
    def __init__(self, size, reset):
        self.state = StateCounter(size, reset)
        self.out = Signal()

        ###

        self.sync += If(self.state.count == 4, self.out.eq(True))
        self.sync += If(self.state.count == 12, self.out.eq(False))
        self.submodules += self.state


def counter_test(dut, reset):
    for cycle in range(40):
        # Only assert CE every second cycle.
        # => each counter value is held for two cycles.
        blup = not ((cycle) % 16) < 8
        if blup:
            yield reset.eq(True)
        else:
            yield reset.eq(False)
        print("Cycle: {} Count: {} Blup: {}".format(cycle, (yield dut.count), blup))
        yield

if __name__ == "__main__":
    plat = pitrex.Platform()
    vec_clk = Signal()
    dut = PhaseShift(5, vec_clk)
    run_simulation(dut, counter_test(dut, vec_clk), vcd_name="basic2.vcd")
