import canopen
import time

def on_pdo_message(msg):
    print("*** PDO MESSAGE RECEIVED ***")
    try:
        # msg should be a list of data bytes
        if len(msg) >= 3:
            led1 = msg[0]
            led2 = msg[1] 
            led3 = msg[2]
            print(f"  LED 1: {'ON' if led1 else 'OFF'}")
            print(f"  LED 2: {'ON' if led2 else 'OFF'}")
            print(f"  LED 3: {'ON' if led3 else 'OFF'}")
        else:
            print(f"  Raw data: {msg}")
        print("-" * 30)
    except Exception as e:
        print(f"Error processing PDO: {e}")
        print(f"Raw message: {msg}")

network = canopen.Network() 
network.connect(channel='vcan0', bustype='socketcan')

node = canopen.LocalNode(1, 'eds/train.eds')
network.add_node(node)

print("=== SLAVE INITIALIZATION ===")
print(f"Slave Node ID: {node.id}")

# Set node to operational
node.nmt.state = 'OPERATIONAL'
print(f"Slave Node state: {node.nmt.state}")

# Configure RPDO manually
try:
    # Create RPDO with COB-ID 0x200 to receive from master
    rpdo = node.rpdo.add(1, 0x200, 3)  # COB-ID 0x200, 3 bytes
    
    # Add variables to RPDO
    rpdo.add_variable('LED1', 0x2000, 1)  # LED 1
    rpdo.add_variable('LED2', 0x2000, 2)  # LED 2  
    rpdo.add_variable('LED3', 0x2000, 3)  # LED 3
    
    print(f"RPDO configured with COB-ID: 0x{rpdo.cob_id:03X}")
    print("RPDO mapping:")
    for i, var in enumerate(rpdo.map):
        print(f"  [{i}] {var.name}")
    
    # Add callback and enable
    rpdo.add_callback(on_pdo_message)
    rpdo.enabled = True
    print("RPDO callback added and enabled")
    
except Exception as e:
    print(f"Error configuring RPDO: {e}")
    print("Using alternative callback approach...")
    
    # Alternative: Listen to all CAN messages and filter
    def on_can_message(msg_id, data, timestamp):
        if msg_id == 0x200:  # Filter for our PDO
            print(f"*** CAN MESSAGE RECEIVED (ID: 0x{msg_id:03X}) ***")
            on_pdo_message(data)
    
    network.subscribe(0x200, on_can_message)
    print("Subscribed to CAN messages with ID 0x200")

print("\n=== SLAVE READY ===")
print("Waiting for PDO messages...")
print("Press Ctrl+C to exit.")

try:
    counter = 0
    while True:
        time.sleep(1)
        counter += 1
        if counter % 10 == 0:
            print(f"Still waiting... ({counter}s)")
        
except KeyboardInterrupt:
    print("\nStopping the node...")
    network.disconnect()
    print("Node stopped.")