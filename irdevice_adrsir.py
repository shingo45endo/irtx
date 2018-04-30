 #!/usr/bin/python3

import struct
import smbus

import irdevice

SLAVE_ADDR = 0x52
CMD_R1 = 0x15
CMD_R2 = 0x25
CMD_R3 = 0x35
CMD_W1 = 0x19
CMD_W2 = 0x29
CMD_W3 = 0x39
CMD_W4 = 0x49
CMD_T1 = 0x59

class IrDeviceAdrsir(irdevice.IrDevice):
    def __init__(self):
        try:
            self.bus = smbus.SMBus(1)
        except FileNotFoundError:
            self.bus = smbus.SMBus(0)   # For Raspberry Pi 1

    def __del__(self):
        self.bus.close()

    def send(self, usecs):
        # Makes an IR data for ADRSIR.
        irdata = IrDeviceAdrsir.make_irdata(usecs)

        # Sends the number of a pair of ON and OFF data.
        self.bus.write_i2c_block_data(SLAVE_ADDR, CMD_W2, list(struct.pack('>H', len(irdata) // 4)))

        # Sends the IR data 32 bytes at a time.
        for packet in [irdata[i:i+32] for i in range(0, len(irdata), 32)]:
            self.bus.write_i2c_block_data(SLAVE_ADDR, CMD_W3, list(packet))

        # Sends a request to transmit the IR data.
        self.bus.write_i2c_block_data(SLAVE_ADDR, CMD_T1, [0])

    @staticmethod
    def make_irdata(usecs):
        # Converts from microsecond to number of ticks in 38kHz.
        ticks = [round(usec * 38000.0 / 1000.0 / 1000.0) for usec in usecs]
        if len(ticks) % 2 != 0:
            ticks.append(3800)
        assert len(usecs) % 2 == 0

        # Makes an IR data for ADRSIR.
        return b''.join([struct.pack('<H', tick) for tick in ticks])
