import canopen
import time

def main():
    network = canopen.Network()
    network.connect(bustype='socketcan', channel='vcan0')

    node = canopen.LocalNode(7, 'eds/dummy.eds')
    network.add_node(node)

    print("Melihat status LED pada node virtual dengan ID = 7...")
    LED1 = node.sdo[0x2001].raw
    LED2 = node.sdo[0x2002].raw
    LED3 = node.sdo[0x2003].raw
    print(f'Status LED: LED1={LED1}, LED2={LED2}, LED3={LED3}')

    time.sleep(3)
    print("Mengubah status LED...")
    node.sdo[0x2001].raw = 1 
    node.sdo[0x2002].raw = 1
    node.sdo[0x2003].raw = 0
    print("Status LED telah diubah.")

    time.sleep(3)
    print("Membaca kembali status LED...")
    LED1 = node.sdo[0x2001].raw
    LED2 = node.sdo[0x2002].raw
    LED3 = node.sdo[0x2003].raw
    print(f'Status LED: LED1={LED1}, LED2={LED2}, LED3={LED3}')

    time.sleep(3)
    network.disconnect()
    print("Terputus dari jaringan CAN.")

if __name__ == "__main__":
    main()


