import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestFailure


@cocotb.test()
async def mixed_language_test(dut):
    """Try accessing handles and setting values in a mixed language environment."""
    await Timer(100, units='ns')

    verilog = dut.i_swapper_sv
    dut._log.info("Got: %s" % repr(verilog._name))

    vhdl = dut.i_swapper_vhdl
    dut._log.info("Got: %s" % repr(vhdl._name))

    verilog.reset_n <= 1
    await Timer(100, units='ns')

    vhdl.reset_n <= 1
    await Timer(100, units='ns')

    if int(verilog.reset_n) == int(vhdl.reset_n):
        dut._log.info("Both signals read as %d" % int(vhdl.reset_n))
    else:
        raise TestFailure("reset_n signals were different")

    # Try accessing an object other than a port...
    verilog_flush = str(verilog.flush_pipe)
    vhdl_flush = str(vhdl.flush_pipe)
