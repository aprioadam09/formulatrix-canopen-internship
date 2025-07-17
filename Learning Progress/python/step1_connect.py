import canopen
import time

def main():
    network = canopen.Network()
    network.connect(bustype ='socketcan', channel='vcan0')

    print("Connected to CAN network in vcan0")

    time.sleep(2)

    network.disconnect()
    print("Disconnected from CAN network")

if __name__ == "__main__":
    main()