module scheduler(input i_clk, input i_e, input i_write_n, output o_load, output o_read);

reg [4:0] q;
initial q = 8;

reg [1:0] s_reset;
reg r_pipe;

// synchronise the phase 2 clock
always @(posedge i_clk)
  {s_reset, r_pipe} <= {s_reset[0], r_pipe, i_e};

always @(posedge i_clk)
begin
  q <= q + 1;
  if (s_reset[1] && !s_reset[0]) // falling edge
    q <= 0;
end

assign o_load = (q == 7);
assign o_read = (q == 5) && !i_write_n;

endmodule