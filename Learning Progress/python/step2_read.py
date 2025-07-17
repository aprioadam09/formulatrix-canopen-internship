import canopen
import time

def main():
    network = canopen.Network()
    network.connect(bustype='socketcan', channel='vcan0')

    node = canopen.LocalNode(4, 'eds/dummy.eds')
    network.add_node(node)

    print("Slave node virtual with ID = 4 has made.")
    time.sleep(1)

    try :
        print("Trying to read 'Device Name' (index 0x1008)...")
        
        device_name = node.sdo[0x1008].raw
        print(f"SDO Read Sucess! Device name is '{device_name}'")

    except canopen.sdo.SdoAbortedError as e:
        print(f"Failed to read SDO : {e}")

    network.disconnect()

if __name__ == "__main__":
    main()