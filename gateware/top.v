module top(
  input i_clk, // Pi clock
  input i_e, // Vec clock

  input [3:0] via_addr, // write address
  inout [7:0] via_data, // data
  input via_read, // read_p/write_n operation
  input valid,

  output vec_halt_n, // vec cpu halt
  output [15:0] vec_addr, // vec address bus
  inout [7:0] vec_data, // vec data bus
  output vec_read // vec read_p/write_n signal
  );

initial vec_data = 0;
initial via_data = 0;

// Keep the 6809 halted
assign vec_halt_n = 0;

// VIA chip select
wire vec_via_cs;
assign vec_addr[12] = vec_via_cs;

// VIA bus address
// cs2_n = !a14 | !a15 | a13 (enabled if a13 low, a14 high, a15 high)
assign vec_addr[15:13] = 3'b110;

// unused address lines
assign vec_addr[11:4] = 0;

// scheduler Outputs
wire o_load;
wire o_read;

// generates the signals to write or read to the vectrex bus at the right time
scheduler u_scheduler (
  .i_clk ( i_clk ),
  .i_e ( i_e ),
  .i_write_n ( via_read ),

  .o_load ( o_load ),
  .o_read ( o_read )
);

// transfer data from fifo to VIA
always @(posedge o_load)
  if (valid)
    begin
      vec_via_cs <= 1;
      vec_addr[3:0] <= via_addr;
      vec_read <= via_read;
      if (!via_read)
        vec_data = via_data;
      else
        vec_data = 0;
    end
  else
    vec_via_cs <= 0;

// transfer data from VIA to fifo
always @(posedge o_read)
  if (valid && via_read)
    via_data = vec_data;
  else
    via_data = 0;

endmodule