import canopen
import time

network = canopen.Network()
network.connect(channel='vcan0', bustype='socketcan')

node = canopen.RemoteNode(1, 'eds/example.eds')
network.add_node(node)

print("Master will change LED status every 2 seconds")

try:
    while True:
        for i in range (1, 4):
            node.sdo[0x2000][i-1].raw = 1
            print(f"Master: LED {i} ON")
            time.sleep(2)

            node.sdo[0x2000][i-1].raw = 0
            print(f"Master: LED {i} OFF")
            time.sleep(2)
            
except KeyboardInterrupt:
    print("Stopping the master node...")
    network.disconnect()