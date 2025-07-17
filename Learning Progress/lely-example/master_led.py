# File: basic_master_test.py

import canopen
import time

# Nama interface dan file EDS harus sesuai dengan yang digunakan oleh slave C++
CAN_INTERFACE = 'vcan0'
EDS_FILE = 'eds/my_slave.eds' # Pastikan file ini ada di direktori yg sama dgn skrip ini, atau beri path lengkap
SLAVE_NODE_ID = 2

print("Mencoba menghubungkan ke jaringan CAN...")
network = canopen.Network()
network.connect(bustype='socketcan', channel=CAN_INTERFACE)

try:
    # 1. Tambahkan slave ke network kita agar bisa diajak bicara
    #    Library python-canopen akan membaca file EDS ini untuk 'mengenal' si slave.
    print(f"Mencari slave dengan Node ID {SLAVE_NODE_ID}...")
    node = network.add_node(SLAVE_NODE_ID, EDS_FILE)
    print("Slave ditemukan!")

    # 2. Kirim SDO Read ke Index 0x1018, Sub-index 1 ('Vendor-ID')
    print("Mengirim permintaan SDO Read untuk Vendor-ID (0x1018:1)...")
    
    # .sdo adalah 'pustakawan' kita
    # [0x1018] adalah rak buku
    # [1] adalah buku ke-1 di rak itu
    # .raw mengambil nilainya
    vendor_id = node.sdo[0x1018][1].raw
    
    # 3. Cetak hasilnya
    # Nilai 0x360 (hex) adalah 864 (decimal). Library akan menampilkannya sebagai decimal.
    print("-----------------------------------------")
    print(f"Jawaban dari slave diterima!")
    print(f"Vendor-ID adalah: {vendor_id} (Hex: {hex(vendor_id)})")
    print("-----------------------------------------")
    
    # Verifikasi
    if vendor_id == 0x360:
      print("SUKSES! Koneksi antara Master Python dan Slave C++ berhasil!")
    else:
      print("GAGAL! Nilai yang diterima tidak sesuai dengan yang diharapkan.")
      exit()
    
    # === TAMBAHKAN BLOK INI ===
    # 2. Logika untuk mengontrol LED
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
                # Menggunakan SDO Write untuk mengirim nilai
                node.sdo[0x2000].raw = value_to_send
                print("Perintah terkirim!")
            else:
                print("Angka harus di antara 0 dan 7.")
        except ValueError:
            print("Input tidak valid, masukkan angka atau 'exit'.")
        except canopen.sdo.SdoAbortedError as e:
            print(f"Error SDO: {e}. Pastikan objek 0x2000 ada di file EDS.")

    # === AKHIR BLOK TAMBAHAN ===

except Exception as e:
    print(f"\nTerjadi error: {e}")
    print("Pastikan slave C++ sudah berjalan dan semua konfigurasi (Node ID, interface CAN) sudah benar.")

finally:
    # 4. Putuskan koneksi
    print("Memutuskan koneksi.")
    network.disconnect()