# File: slave_pdo_led.py
import canopen
import time

network = canopen.Network()
network.connect(channel='vcan0', bustype='socketcan')

# Buat node lokal kita
node = canopen.LocalNode(1, 'eds/example.eds')
network.add_node(node)

# --- KONFIGURASI DIRI SENDIRI ---
print("Slave: Mengkonfigurasi RPDO1 untuk mendengarkan di COB-ID 0x181...")
# 1. Baca konfigurasi default dari EDS
node.rpdo.read()
# 2. Ubah COB-ID untuk RPDO 1 menjadi 0x181
node.rpdo[1].cob_id = 0x181
node.rpdo[1].enabled = True
# 3. Simpan perubahan ini ke Object Dictionary internal
node.rpdo.save()

# --- PASANG LISTENER SETELAH KONFIGURASI SELESAI ---
def on_led_pdo_received(map):
    led_state_byte = map[0].raw
    print(f"\nSlave: PENGUMUMAN DITERIMA! Nilai baru: {led_state_byte:03b}")
    
    led1_on = (led_state_byte & 0b001) > 0
    led2_on = (led_state_byte & 0b010) > 0
    led3_on = (led_state_byte & 0b100) > 0
    
    print(f"  -> LED 1: {'ON' if led1_on else 'OFF'}")
    print(f"  -> LED 2: {'ON' if led2_on else 'OFF'}")
    print(f"  -> LED 3: {'ON' if led3_on else 'OFF'}")

# Daftarkan callback SEKARANG, setelah COB-ID sudah benar
node.rpdo[1].add_callback(on_led_pdo_received)

print("Slave siap menerima perintah LED via PDO... (Press Ctrl+C to stop)")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping the slave node...")
    network.disconnect()