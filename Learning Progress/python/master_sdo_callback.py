import canopen
import time

network = canopen.Network()
network.connect(channel='vcan0', bustype='socketcan')

node = canopen.RemoteNode(1, 'eds/dummy.eds')
network.add_node(node)

print("Master will change LED state every 2 seconds... (Press Ctrl+C to stop)")

try:
    while True:
        node.sdo[0x2000].raw = 1
        print("Master: LED ON")
        time.sleep(2)

        node.sdo[0x2000].raw = 0
        print("Master: LED OFF")
        time.sleep(2)

except KeyboardInterrupt:
    print("Stopping the master node...")
    network.disconnect()