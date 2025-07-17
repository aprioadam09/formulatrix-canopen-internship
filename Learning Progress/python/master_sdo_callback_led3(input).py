import canopen
import time

network = canopen.Network()
network.connect(channel='vcan0', bustype='socketcan')

node = canopen.RemoteNode(1, 'eds/example.eds')
network.add_node(node)

print("Master is online. Control LEDs by typing 3 digits (e.g. 101), or 'q' to quit.")
print("1 = ON, 0 = OFF for each LED.")

try:
    while True:
        user_input = input("Enter LED states (3 digits, e.g. 101) or 'q' to quit: ").strip()
        if user_input.lower() == 'q':
            break
        elif len(user_input) == 3 and all(c in '01' for c in user_input):
            for i in range(3):
                node.sdo[0x2000][i].raw = int(user_input[i])
                print(f"Master: LED {i+1} {'ON' if user_input[i] == '1' else 'OFF'}")
            time.sleep(1)
        else:
            print("Invalid input. Please enter 3 digits (e.g. 101) or q.")
except KeyboardInterrupt:
    print("Stopping the master node...")
finally:
    network.disconnect()
    print("Disconnected.")