#include <verilated.h>  // Defines common routines
#include <verilated_vcd_c.h>  // Defines common routines
#include "Vscheduler.h"   // From Verilating "top.v"

VerilatedVcdC *trace;
Vscheduler *top;                      // Instantiation of module

vluint64_t main_time = 0;       // Current simulation time
// This is a 64-bit integer to reduce wrap over issues and
// allow modulus.  You can also use a double, if you wish.
// I think this is in nS.

double sc_time_stamp () {       // Called by $time in Verilog
    return main_time;           // converts to double, to match
                                // what SystemC does
}

// Open/create a trace file
void opentrace(const char *vcdname) {
  if (!trace) {
    trace = new VerilatedVcdC;
    top->trace(trace, 99);
    trace->open(vcdname);
  }
}

// Close a trace file
void closetrace(void) {
  if (trace) {
    trace->close();
    trace = NULL;
  }
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);   // Remember args
  Verilated::traceEverOn(true);

  top = new Vscheduler;             // Create instance

  opentrace("pitrex.vcd");

  top->i_write_n = 0;

  //while (!Verilated::gotFinish()) {
  while (main_time < 10000) {
    // phase 2 clock (1MHz)
    top->i_e = ((main_time + 12) % 1000) < 500 ? 0 : 1;

    // main clock (8MHz, probably should be 16)
    top->i_clk = (main_time % 125) < 62 ? 0 : 1;

    top->eval();  // Evaluate model

    if (trace) trace->dump(main_time);

    main_time++;  // Time passes...
  }

  closetrace();

  top->final();  // Done simulating

  delete top;
}