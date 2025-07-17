import canopen
import time

def led_change(new_value):
    if new_value:
        print("LED is ON")
    else:
        print("LED is OFF")

network = canopen.Network()
network.connect(channel='vcan0', bustype='socketcan')

node = canopen.LocalNode(1, 'eds/dummy.eds')
network.add_node(node)

last_value = node.sdo[0x2000].raw
led_change(last_value)

print("Monitoring LED state changes... (Press Ctrl+C to stop)")

try:
    while True:
        current = node.sdo[0x2000].raw
        if current != last_value:
            led_change(current)
            last_value = current
        time.sleep(2)

except KeyboardInterrupt:
    print("Stopping the slave node...")
    network.disconnect()
