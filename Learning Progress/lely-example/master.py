# File: basic_master_test.py

import canopen
import time

# Nama interface dan file EDS harus sesuai dengan yang digunakan oleh slave C++
CAN_INTERFACE = 'vcan0'
EDS_FILE = 'eds/cpp-slave.eds' # Pastikan file ini ada di direktori yg sama dgn skrip ini, atau beri path lengkap
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

except Exception as e:
    print(f"\nTerjadi error: {e}")
    print("Pastikan slave C++ sudah berjalan dan semua konfigurasi (Node ID, interface CAN) sudah benar.")

finally:
    # 4. Putuskan koneksi
    print("Memutuskan koneksi.")
    network.disconnect()