import canopen

network = canopen.Network()
network.connect(channel='vcan0', bustype='socketcan')

print("Master node is online. Mencari slave dengan Node ID 2...")
node = network.add_node(2, 'eds/cpp-slave.eds')
print("Slave ditemukan")

try:
    print("Mengirim permintaan SDO Read untuk Vendor-ID (OX1018:)...")
    vendor_id = node.sdo[0x1018][1].raw

    print("-------------")
    print("Jawaban dari slave")
    print(f"Vendor ID adalah: {vendor_id} (Hex: {hex(vendor_id)})")
    print("------------")

    if vendor_id == 0x360:
        print("Sukses! Koneksi Berhasil")
    else :
        print("Koneksi Gagal.")

except KeyboardInterrupt:
    print("Memutuskan koneksi")
    network.disconnect()
