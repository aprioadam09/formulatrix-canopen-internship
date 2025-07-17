# Simple test without EDS file
import canopen
import time

def on_pdo_message(msg):
    print(f"Raw PDO received: {msg}")

# Create network
network = canopen.Network()
network.connect(channel='vcan0', bustype='socketcan')

# Create simple local node
node = canopen.LocalNode(1)
network.add_node(node)

# Manually configure RPDO
rpdo = node.rpdo.add(1, 0x200, 8)  # COB-ID 0x200, 8 bytes
rpdo.add_callback(on_pdo_message)
rpdo.enabled = True

print("Simple PDO test - waiting for messages on COB-ID 0x200")
print("Press Ctrl+C to exit.")

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nStopping...")
    network.disconnect()
    print("Stopped.")