import canopen
import time

network = canopen.Network()
network.connect(channel='vcan0', bustype='socketcan')

node = canopen.LocalNode(1, 'eds/example.eds')
network.add_node(node)

print("Slave node is online. Waiting for commands... (Press Ctrl+C to stop)")

try:
    while True:
        led1= node.sdo[0x2000][0].raw
        led2 = node.sdo[0x2000][1].raw
        led3 = node.sdo[0x2000][2].raw
        print(f"Current State: LED 1: { 'ON' if led1 else 'OFF' }, LED 2: { 'ON' if led2 else 'OFF' }, LED 3: { 'ON' if led3 else 'OFF' }")
        time.sleep(2)

except KeyboardInterrupt:
    print("Stopping the node...")
    network.disconnect()