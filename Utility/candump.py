import at_serial_can
import sys

bus = at_serial_can.ATSerialBus(channel=sys.argv[1], bitrate=250000)

while True:
    msg = bus.recv()
    #print(f'From: 0x{msg.arbitration_id:02X} Data: {msg.data[0]:02X} {msg.data[1]:02X} {msg.data[2]:02X}')
    if msg:
        print(f'From: 0x{msg.arbitration_id:02X} Hexadecimal:', end=" ")
        for i in range(msg.dlc):
            print(f'{msg.data[i]:02X}', end=" ")
        print(f'Integer:', end=" ")
        for i in range(msg.dlc):
            print(f'{int(msg.data[i])}', end=" ")
        print(end=" \n")