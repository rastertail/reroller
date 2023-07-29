"""
Conversion routines
"""

from py65.devices import mpu6502
from tqdm import trange

from sid2reroller.record import SidRecorder


class ConvertException(Exception):
    """
    Generic error during the conversion process
    """


def convert(sid_file: bytes, n_frames: int) -> bytes:
    """
    Convert an input PSID file to Reroller streams
    """

    if not sid_file.startswith(b"PSID"):
        raise ConvertException("Input file is not a PSID")

    data = int.from_bytes(sid_file[6:8], "big")
    load = int.from_bytes(sid_file[8:10], "big")
    init = int.from_bytes(sid_file[10:12], "big")
    play = int.from_bytes(sid_file[12:14], "big")

    if load == 0:
        load = int.from_bytes(sid_file[data : data + 2], "little")
        data += 2

    sid_data = sid_file[data:]

    cpu = mpu6502.MPU(memory=SidRecorder())
    cpu.memory[load : load + len(sid_data)] = sid_data
    cpu.pc = init

    # TODO Select subtune if necessary
    while cpu.memory[cpu.pc] != 0x60 or cpu.sp < 0xFF:
        cpu.step()

    for _ in trange(0, n_frames, desc="Rendering", unit="frames"):
        cpu.pc = play
        cpu.memory.new_frame()
        while cpu.memory[cpu.pc] != 0x60 or cpu.sp < 0xFF:
            cpu.step()

    return cpu.memory.finish()
