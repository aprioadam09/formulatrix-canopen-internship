import canopen

node_id = 2

network = canopen.Network()
network.connect(channel='can1', bustype='socketcan')

try:
    print(f"Mencari slave dengan Node ID {node_id}")
    node = network.add_node(node_id, 'eds/my_slave.eds')
    print("Slave ditemukan!")

    print("--- Kontrol LED ---")
    print("Masukkan angka dari 0-7 untuk mengontrol 3 LED.")
    print("  1: LED1 | 2: LED2 | 4: LED3")
    print("  Contoh: 3 (1+2) menyalakan LED1 dan LED2.")
    print("  Ketik 'exit' untuk keluar.")
        
    while True:
        try:
            cmd = input("\nPerintah LED (0-7): ")
            if cmd.lower() == 'exit':
                break

            value_to_send = int(cmd)
            if 0 <= value_to_send <= 7:
                print(f"Mengirim nilai {value_to_send} ke objek 0x2000 (LED Control)...")
                node.sdo[0x2000].raw = value_to_send
                print("Perintah terkirim!")
            else:
                print("Tolong masukkan angka di antara 0 dan 7!")
        except ValueError:
            print("Input Invalid! Masukkan angka atau 'exit'.")
        except canopen.sdo.SdoAbortedError as e:
            print(f"Error SDO: {e}")

except KeyboardInterrupt:
    print("Memutuskan Koneksi...")
    network.disconnect    
    print("Koneksi Terputus.")