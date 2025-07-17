import canopen
import time

def print_led_status_update(message):
    """Callback function untuk menangani TPDO yang diterima dari slave."""
    print("\n--- [LAPORAN DITERIMA DARI SLAVE] ---")
    # 'message' adalah representasi dari PDO yang diterima.
    # Kita bisa mengakses variabel di dalamnya.
    for var in message:
        # var.name diambil dari file EDS, var.raw adalah nilainya
        print(f"Status LED saat ini ({var.name}): {var.raw}")
    print("--------------------------------------")

network = canopen.Network()
network.connect(channel='can1', bustype='socketcan')

node_id = 2
led_control_cob_id = 0x200 + node_id

print(f"Master node is online. Siap mengirim PDO ke COB-ID {hex(led_control_cob_id)}...")

try:
    node = network.add_node(node_id, 'my_slave.eds')
    node.tpdo.read()
    node.tpdo[1].add_callback(print_led_status_update)

    print(f"Master node is online. Siap mengirim perintah ke COB-ID {hex(led_control_cob_id)}...")
    print("Juga mendengarkan laporan balik dari slave di COB-ID " + hex(node.tpdo[1].cob_id))
    print("----------------------------------------------------------------------")

    while True:
        try:
            # Minta input dari pengguna
            led_value = int(input("Masukkan nilai LED (0-7), atau 99 untuk keluar: "))

            if led_value == 99:
                break
            
            if 0 <= led_value <= 7:
                print(f"Mengirim PDO dengan nilai: {led_value}")
                network.send_message(led_control_cob_id, [led_value])
            else:
                print("Nilai tidak valid. Harap masukkan angka antara 0 dan 7.")

        except ValueError:
            print("Input tidak valid. Harap masukkan angka.")
        
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

print("Memutuskan koneksi...")
network.disconnect()