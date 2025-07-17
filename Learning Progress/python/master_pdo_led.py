# File: master_pdo_led.py (VERSI BARU)
import canopen
import time

network = canopen.Network()
network.connect(channel='vcan0', bustype='socketcan')

# Cukup representasi node untuk mengirim NMT
node = canopen.RemoteNode(1, 'eds/example.eds')
network.add_node(node)

# Set slave ke state OPERATIONAL agar ia memproses PDO
node.nmt.state = 'OPERATIONAL'
print("Master: Mengirim NMT Start ke slave.")
time.sleep(0.1)

print("Master siap mengirim PDO untuk kontrol LED...")

led_state_byte = 0b000
try:
    while True:
        # Menyalakan LED 1
        led_state_byte = 0b001
        network.send_message(0x181, [led_state_byte])
        print(f"Master MENGUMUMKAN status LED: {led_state_byte:03b} ke COB-ID 0x181")
        time.sleep(1)

        # Menyalakan LED 2
        led_state_byte = 0b010
        network.send_message(0x181, [led_state_byte])
        print(f"Master MENGUMUMKAN status LED: {led_state_byte:03b} ke COB-ID 0x181")
        time.sleep(1)

        # Menyalakan LED 3
        led_state_byte = 0b100
        network.send_message(0x181, [led_state_byte])
        print(f"Master MENGUMUMKAN status LED: {led_state_byte:03b} ke COB-ID 0x181")
        time.sleep(1)

except KeyboardInterrupt:
    network.send_message(0x181, [0]) # Matikan semua LED
    print("Stopping the master node...")
    network.disconnect()