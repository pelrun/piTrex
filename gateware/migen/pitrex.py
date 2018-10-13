from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform

_ios = [

  # Vectrex signals
  ("vectrex", 0,
    Subsignal("address", Pins('P7 P6 P5 P3 P2 P1 P42 P43 P41 P40 P37 P39 P20 P21 P22 P36')),
    Subsignal("data", Pins('P8 P18 P19 P30 P31 P32 P33 P34')),
    Subsignal("clk_n", Pins('P38')),
    Subsignal("rw", Pins('P29')),
    Subsignal("nmi", Pins('P28')),
    Subsignal("pb6", Pins('P23')),
    Subsignal("irq_n", Pins('P27')),
    IOStandard("LVTTL"),
  ),

  # Pi signals
  ("pi", 0,
    Subsignal("cs_n", Pins('P12')),
    Subsignal("sck", Pins('P13')),
    Subsignal("miso", Pins('P14')),
    Subsignal("mosi", Pins('P16')),
    IOStandard("LVCMOS33"),
  ),

  ("pi_clk", 0, Pins('P44'), IOStandard("LVCMOS33")),

] # yapf: disable

class Platform(XilinxPlatform):
  default_clk_name = "pi_clk"
  default_clk_period = 125 # 8MHz

  def __init__(self):
    XilinxPlatform.__init__(self, "xc9572xl-10vqg44c", _ios, toolchain="ise")
