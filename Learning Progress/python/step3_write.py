import canopen
import time

network = canopen.Network()
network.connect(bustype ='socketcan', channel='vcan0')

node = canopen.LocalNode(5, 'eds/dummy.eds')
network.add_node(node)

print(f"Slave node virtual (ID=5) dibuat.")
time.sleep(1)

original_time = node.sdo[0x1017].raw
print(f"Waktu heartbeat awal : {original_time} ms")

print("Mengubah waktu heartbeat menjadi 2000 ms...")
node.sdo[0x1017].raw = 2000

new_time = node.sdo[0x1017].raw
print(f"Waktu heartbeat sekarang : {new_time} ms")

network.disconnect()