verilator -Wall -trace -cc top.v --exe testbench.cpp
make -j -C obj_dir -f Vtop.mk
obj_dir/Vtop
gtkwave pitrex.vcd
