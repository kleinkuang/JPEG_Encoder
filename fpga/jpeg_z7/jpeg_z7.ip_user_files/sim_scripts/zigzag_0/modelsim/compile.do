vlib modelsim_lib/work
vlib modelsim_lib/msim

vlib modelsim_lib/msim/xil_defaultlib
vlib modelsim_lib/msim/xpm

vmap xil_defaultlib modelsim_lib/msim/xil_defaultlib
vmap xpm modelsim_lib/msim/xpm

vlog -work xil_defaultlib -64 -incr -sv \
"D:/Xilinx/Vivado/2019.1/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv" \
"D:/Xilinx/Vivado/2019.1/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv" \

vcom -work xpm -64 -93 \
"D:/Xilinx/Vivado/2019.1/data/ip/xpm/xpm_VCOMP.vhd" \

vlog -work xil_defaultlib -64 -incr -sv \
"../../../../jpeg_z7.srcs/sources_1/ip/zigzag_0/src/ram_8bx64.sv" \
"../../../../jpeg_z7.srcs/sources_1/ip/zigzag_0/src/zigzag.sv" \
"../../../../jpeg_z7.srcs/sources_1/ip/zigzag_0/sim/zigzag_0.sv" \

vlog -work xil_defaultlib \
"glbl.v"

