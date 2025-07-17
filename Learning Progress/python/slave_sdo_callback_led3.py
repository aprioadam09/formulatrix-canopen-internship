import canopen
import time

def led_change(index, value):
    print(f"LED {index} status: {'ON' if value else 'OFF'}")

network = canopen.Network()
network.connect(channel='vcan0', bustype='socketcan')

node = canopen.LocalNode(1, 'eds/example.eds')
network.add_node(node)

last_values = {
    1: node.sdo[0x2000][0].raw,
    2: node.sdo[0x2000][1].raw,
    3: node.sdo[0x2000][2].raw
}
led_change(1, last_values[1])
led_change(2, last_values[2])
led_change(3, last_values[3])

print("Waiting for LED state changes... (Press Ctrl+C to stop)")

try:
    while True:
        for i in range(1, 4):
            current_value = node.sdo[0x2000][i-1].raw
            if current_value != last_values[i]:
                led_change(i, current_value)
                last_values[i] = current_value
        time.sleep(2)
        
except KeyboardInterrupt:
    print("Stopping the node...")
    network.disconnect()

