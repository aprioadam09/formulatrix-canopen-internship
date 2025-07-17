import canopen
import time

network = canopen.Network()
network.connect(channel='vcan0', bustype='socketcan')

node = canopen.RemoteNode(1, 'eds/example.eds')
network.add_node(node)

print("Master node is online. Waiting for commands... (Press Ctrl+C to stop)")

try:
    while True:
        print("Sending command, LED 1: ON, LED 2: OFF, LED 3: ON")
        node.sdo[0x2000][0].raw = 1
        node.sdo[0x2000][1].raw = 0
        node.sdo[0x2000][2].raw = 1
        print("Command sent")
        time.sleep(2)

        print("Sending command, LED 1: OFF, LED 2: ON, LED 3: OFF")
        node.sdo[0x2000][0].raw = 0
        node.sdo[0x2000][1].raw = 1
        node.sdo[0x2000][2].raw = 0
        print("Command sent")
        time.sleep(2)

except KeyboardInterrupt:   
    print("Stopping the node...")
    network.disconnect()

