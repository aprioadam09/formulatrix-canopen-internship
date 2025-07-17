import canopen
import time

network = canopen.Network()
network.connect(channel='vcan0', bustype='socketcan')

node = canopen.RemoteNode(1, 'eds/dummy.eds')
network.add_node(node)

print("Read RPDO mapping from slave node...")
node.rpdo[1].read()
print("RPDO mapping read successfully.")

print("Master node is online. Sending RPDO to slave...")

try:
    while True:
        node.rpdo[1]['LED Controls.LED1'].raw = 1
        node.rpdo[1]['LED Controls.LED2'].raw = 0
        node.rpdo[1]['LED Controls.LED3'].raw = 1
        node.rpdo[1].transmit()
        print("RPDO sent to slave node.")
        time.sleep(2)

        node.rpdo[1]['LED Controls.LED1'].raw = 0
        node.rpdo[1]['LED Controls.LED2'].raw = 1
        node.rpdo[1]['LED Controls.LED3'].raw = 0
        node.rpdo[1].transmit()
        print("RPDO sent to slave node.")
        time.sleep(2)  

except KeyboardInterrupt:
    print("Master node stopped.")
    network.disconnect()
