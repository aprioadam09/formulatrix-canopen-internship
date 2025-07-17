import canopen
import time

network = canopen.Network()
network.connect(channel='vcan0', bustype='socketcan')

node = canopen.LocalNode(0x01, 'eds/example.eds')
network.add_node(node)

value = node.sdo[0x2000].raw
print(f"Nilai awal: {value}")

print("Mengubah nilai ke 30...")
node.sdo[0x2000].raw = 30

new_value = node.sdo[0x2000].raw
print(f"Nilai sekarang: {new_value}")

network.disconnect()