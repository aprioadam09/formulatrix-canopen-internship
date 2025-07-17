import canopen
import time

network = canopen.Network()
network.connect(channel='vcan0', bustype='socketcan')

# Create a simple local node for master (not remote)
node = canopen.LocalNode(2, 'eds/train.eds')  # Use different node ID
network.add_node(node)

print("=== MASTER INITIALIZATION ===")
print(f"Master Node ID: {node.id}")

# Set node to operational
node.nmt.state = 'OPERATIONAL'
print(f"Master Node state: {node.nmt.state}")

# Configure TPDO manually
try:
    # Create TPDO with COB-ID 0x200 (which matches slave RPDO)
    tpdo = node.tpdo.add(1, 0x200, 3)  # COB-ID 0x200, 3 bytes
    
    # Add variables to TPDO
    tpdo.add_variable('LED1', 0x2000, 1)  # LED 1
    tpdo.add_variable('LED2', 0x2000, 2)  # LED 2  
    tpdo.add_variable('LED3', 0x2000, 3)  # LED 3
    
    print(f"TPDO configured with COB-ID: 0x{tpdo.cob_id:03X}")
    print("TPDO mapping:")
    for i, var in enumerate(tpdo.map):
        print(f"  [{i}] {var.name}")
    
except Exception as e:
    print(f"Error configuring TPDO: {e}")
    # Fallback: use raw CAN message
    print("Using raw CAN message approach...")
    
    try:
        message_counter = 0
        while True:
            message_counter += 1
            print(f"\n--- Cycle {message_counter} ---")
            
            # Pattern 1: LED1=ON, LED2=OFF, LED3=ON
            data1 = [1, 0, 1]  # LED states
            network.send_message(0x200, data1)
            print(f"Sent raw CAN: COB-ID=0x200, Data={data1}")
            time.sleep(2)
            
            # Pattern 2: LED1=OFF, LED2=ON, LED3=OFF  
            data2 = [0, 1, 0]  # LED states
            network.send_message(0x200, data2)
            print(f"Sent raw CAN: COB-ID=0x200, Data={data2}")
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nStopping...")
        network.disconnect()
        print("Stopped.")
    exit()

print("\n=== STARTING PDO TRANSMISSION ===")
print("Press Ctrl+C to exit.")

try:
    cycle = 0
    while True:
        cycle += 1
        print(f"\n--- Cycle {cycle} ---")
        
        # Pattern 1: LED1=ON, LED2=OFF, LED3=ON
        try:
            tpdo['LED1'].raw = 1
            tpdo['LED2'].raw = 0
            tpdo['LED3'].raw = 1
            
            print(f"Setting: LED1={tpdo['LED1'].raw}, LED2={tpdo['LED2'].raw}, LED3={tpdo['LED3'].raw}")
            tpdo.transmit()
            print(f"Transmitted PDO with COB-ID: 0x{tpdo.cob_id:03X}")
            
        except Exception as e:
            print(f"Error in cycle {cycle}, pattern 1: {e}")
            
        time.sleep(3)
        
        # Pattern 2: LED1=OFF, LED2=ON, LED3=OFF
        try:
            tpdo['LED1'].raw = 0
            tpdo['LED2'].raw = 1
            tpdo['LED3'].raw = 0
            
            print(f"Setting: LED1={tpdo['LED1'].raw}, LED2={tpdo['LED2'].raw}, LED3={tpdo['LED3'].raw}")
            tpdo.transmit()
            print(f"Transmitted PDO with COB-ID: 0x{tpdo.cob_id:03X}")
            
        except Exception as e:
            print(f"Error in cycle {cycle}, pattern 2: {e}")
            
        time.sleep(3)

except KeyboardInterrupt:
    print("\nStopping the node...")
    network.disconnect()
    print("Node stopped.")