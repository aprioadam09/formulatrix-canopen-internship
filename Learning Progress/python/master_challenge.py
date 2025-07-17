# File: master_challenge.py
import canopen
import time

def on_slave_pdo_received(can_id, data, timestamp):
    if data[0] != 0:
        print("\n<<< Master: NOTIFIKASI DITERIMA! Tombol pada Slave ditekan.")

network = canopen.Network()
network.connect(channel='vcan0', bustype='socketcan')

slave_node = canopen.RemoteNode(2, 'eds/challenge.eds')
network.add_node(slave_node)

network.subscribe(0x282, on_slave_pdo_received)

print("Master (ID=1) Siap. Mengirim NMT Start ke Slave...")
slave_node.nmt.state = 'OPERATIONAL'
time.sleep(0.1)

counter = 0
try:
    while True:
        print(f"Master: MENGIRIM counter: {counter}")
        # kirim counter ke slave
        network.send_message(0x182, counter.to_bytes(4,'little'))
        counter += 1
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping the master node...")
    slave_node.nmt.state = 'STOPPED'
    network.disconnect()
    print("Master node stopped.")