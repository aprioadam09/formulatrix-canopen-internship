import canopen
import time

network = canopen.Network()
network.connect(channel='vcan0', bustype='socketcan')

node = canopen.RemoteNode(1, 'eds/dummy.eds')
network.add_node(node)

print("Master: Control LED by typing 1 (ON), 0 (OFF), or 'q' to quit.")

try:
    while True:
        user_input = input("Enter LED state (1=ON, 0=OFF, q=quit): ").strip()
        if user_input.lower() == 'q':
            break
        elif user_input in ('0', '1'):
            node.sdo[0x2000].raw = int(user_input)
            print(f"Master: LED {'ON' if user_input == '1' else 'OFF'}")
        else:
            print("Invalid input. Please enter 1, 0, or q.")
except KeyboardInterrupt:
    print("Stopping the master node...")
finally:
    network.disconnect()
    print("Disconnected.")