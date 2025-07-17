import canopen
import time

# Nama antarmuka CAN
can_interface = 'vcan0'

# Create CANopen network
network = canopen.Network()

try:
    print(f"Mencoba menghubungkan ke {can_interface}...")
    network.connect(bustype='socketcan', channel=can_interface)
    print(f"Berhasil terhubung ke {can_interface}.")

    # ---- PERUBAHAN UTAMA DI SINI ----
    # Periode SYNC dalam detik
    sync_period_seconds = 0.1
    
    # Mulai SYNC producer menggunakan objek network.sync
    network.sync.start(sync_period_seconds)
    # ---------------------------------

    print(f"SYNC Producer dimulai di {can_interface} setiap {sync_period_seconds} detik.")
    print(f"COB-ID SYNC: 0x{network.sync.cob_id:02X}") # Untuk melihat COB-ID SYNC
    print(f"Tekan Ctrl+C untuk berhenti.")

    # Biarkan program berjalan
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nKeyboard interrupt diterima, menghentikan SYNC producer...")
except Exception as e:
    print(f"Terjadi error: {e}")
    if isinstance(e, canopen.CanError): # Atau can.CanError tergantung namespace
         print("Pastikan antarmuka vcan0 sudah ada dan aktif ('sudo ip link set up vcan0').")
         print("Juga, pastikan modul vcan sudah dimuat ('sudo modprobe vcan').")
finally:
    # Hentikan SYNC producer jika sedang berjalan
    if hasattr(network, 'sync') and network.sync.is_running: # Periksa apakah sync sudah diinisialisasi dan berjalan
        network.sync.stop()
        print("SYNC producer dihentikan.")
    
    # Putuskan koneksi jaringan
    if network.is_connected:
        network.disconnect()
        print(f"Koneksi ke {can_interface} diputus.")
    print("Program selesai.")
