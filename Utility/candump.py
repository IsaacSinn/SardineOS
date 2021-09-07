import at_serial_can
import sys

bus = at_serial_can.ATSerialBus(channel=sys.argv[1], bitrate=250000)

while True:
    msg = bus.recv()
    print(f'From: 0x{msg.arbitration_id:02X}, {msg}')