# CANopen Internship Project - Formulatrix

This repository contains the progress of the development and implementation of the CANopen protocol during the internship program at Formulatrix Bandung.

**Project Objective:** Integrate CANopen into one of existing firmware

---

## Main Application (Showcase)

This application demonstrates two-way CANopen communication through physical hardware, where a Python Master controls a C++ Slave.

### Architecture

*   **Master (Python):** Runs in `master_pdo.py`, connected to the `can1` interface (Kvaser).
*   **Slave (C++):** Runs in `slave_pdo.cpp`, connected to the `can0` interface (MKS CANable).
*   **Protocol:**
*   *   **SDO:** Used by the library for initialization.
    *   **PDO:** Used for real-time LED control command transmission.

### Prerequisites

- Linux (tested on Ubuntu 22.04)
- Lely CANopen library
- Python 3
- `python-canopen` library (`pip install python-canopen`)
- `can-utils`

### How to Compile the Slave (C++)

```bash
# From the project root directory
g++ -std=c++14 -Wall -Wextra -pedantic -g -O2     $(pkg-config --cflags liblely-coapp)     slave_pdo.cpp -o slave_pdo     $(pkg-config --libs liblely-coapp)
```

### How to Run

1.  **Hardware Setup:** Connect both CAN adapters, ensuring the resistor termination is installed.
2.  **Enable CAN Interface:**
```bash
    sudo ip link set can0 up type can bitrate 500000
    sudo ip link set can1 up type can bitrate 500000
```
3.  **Run Slave (Terminal 1):**
```bash
    # sudo may be required if udev rules are not yet perfect
    sudo ./slave_pdo
```
4.  **Run Master (Terminal 2):**
```bash
    # Ensure the virtual environment is active if used
    python master_pdo.py
```

## Learning Progress (Sandbox)

The `learning_progress/` folder contains a collection of scripts and code from various stages of experimentation, ranging from basic SDO connection tests to initial PDO implementation in the `vcan` environment.
