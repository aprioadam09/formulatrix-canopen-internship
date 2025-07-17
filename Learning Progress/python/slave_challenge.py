# File: slave_challenge.py
import canopen
import time

#---Callback untuk menerima PDO dari master---
def on_master_pdo_received(map_data):
    counter_value = map_data['Master Counter'].raw
    print(f"\nSlave: PENGUMUMAN DITERIMA! Nilai counter: {counter_value}")

network = canopen.Network()
network.connect(channel='vcan0', bustype='socketcan')

node = canopen.LocalNode(2, 'eds/challenge.eds')
network.add_node(node)

node.rpdo.read()
node.rpdo[1].cob_id = 0x182
node.rpdo[1].clear()
node.rpdo[1].add_variable('Master Counter')
node.rpdo[1].add_callback(on_master_pdo_received)
node.rpdo[1].enabled = True
node.rpdo.save()

node.tpdo.read()
node.tpdo[1].cob_id = 0x282
node.tpdo[1].clear()
node.tpdo[1].add_variable('Slave Button Press')
node.tpdo[1].enabled = True
node.tpdo.save()

print("Slave (ID=2) Siap. Menunggu Perintah NMT Start dari Master...")

button_press_timer = 0
try:
    while True:
        if node.nmt.state == 'OPERATIONAL':
            time.sleep(1)
            button_press_timer += 1
        
            if button_press_timer >= 5:
                print("\n>>> Slave: Tombol ditekan! Mengirim notifikasi ke Master...")
                node.tpdo[1]['Slave Button Press'].raw = 1
                node.tpdo[1].transmit()
                time.sleep(0.1)
                node.tpdo[1]['Slave Button Press'].raw = 0
                node.tpdo[1].transmit()
                button_press_timer = 0
except KeyboardInterrupt:
    print("Stopping the slave node...")
    network.disconnect()