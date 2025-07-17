import canopen
import time

network = canopen.Network()
network.connect(channel='vcan0', bustype='socketcan')

node = canopen.LocalNode(0x01, 'eds/example.eds')
network.add_node(node)

suhu = 20
try:
    while True:
        node.sdo[0x2002].raw = suhu
        print(f"Nilai suhu telah diatur ke: {suhu} °C")
        suhu += 1
        if suhu > 30:
            suhu = 20
        time.sleep(2)  # Delay for 2 seconds before the next update

except KeyboardInterrupt:
    print("berhenti")
    network.disconnect()