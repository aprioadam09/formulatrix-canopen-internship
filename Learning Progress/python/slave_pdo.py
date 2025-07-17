import canopen
import time

network = canopen.Network()
network.connect(channel='vcan0', bustype='socketcan')

node = canopen.LocalNode(0x01, 'eds/dummy.eds')
network.add_node(node)

print("Slave node is online. Waiting for commands... (Press Ctrl+C to stop)")

try:
    while True:
        node.rpdo[1].read()
        led1 = node.rpdo[1]['LED Controls.LED1'].raw
        led2 = node.rpdo[1]['LED Controls.LED2'].raw
        led3 = node.rpdo[1]['LED Controls.LED3'].raw
        print(f"Slave LED states: LED1={ 'ON' if led1 else 'OFF' }, LED2={ 'ON' if led2 else 'OFF' }, LED3={ 'ON' if led3 else 'OFF' }")
        time.sleep(2)

except KeyboardInterrupt:
    network.disconnect()
    print("Stopping the node...")
