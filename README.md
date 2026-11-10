# NexaTech Solutions — Enterprise Network Project

## Overview

This project designs and implements a two-branch enterprise network for NexaTech Solutions
using Cisco Packet Tracer. The network connects the Headquarters in **Kochi, Kerala** with
a Branch Office in **Bengaluru, Karnataka**.

## Project Structure

```
NexaTech-Network/
├── generate.py          # Generates all device configurations
├── validate.py          # Validates configs for errors
├── configs/
│   ├── R1-KOCHI.txt
│   ├── R2-BENGALURU.txt
│   ├── SW1-KOCHI.txt
│   ├── SW2-KOCHI.txt
│   ├── SW1-BENGALURU.txt
│   └── SW2-BENGALURU.txt
├── docs/
│   ├── README.md
│   ├── NETWORK_TOPOLOGY.md
│   ├── IP_ADDRESSING.md
│   ├── DEVICE_CONFIGURATIONS.md
│   ├── TESTING_GUIDE.md
│   └── PROJECT_REPORT.md
└── tests/
```

## Quick Start

```bash
# Generate configs
python generate.py

# Validate configs
python validate.py
```

## Devices

| Device | Role | Site |
|---|---|---|
| R1-KOCHI | Router (2911) | Kochi HQ |
| R2-BENGALURU | Router (2911) | Bengaluru Branch |
| SW1-KOCHI | Distribution Switch (2960) | Kochi HQ |
| SW2-KOCHI | Access Switch (2960) | Kochi HQ |
| SW1-BENGALURU | Distribution Switch (2960) | Bengaluru Branch |
| SW2-BENGALURU | Access Switch (2960) | Bengaluru Branch |

## Credentials

| Purpose | Value |
|---|---|
| Enable Secret | NexaTech@2024 |
| Console Password | Console@2024 |
| VTY Password | VTY@2024 |

## Key Technologies

- Router-on-a-Stick inter-VLAN routing
- IEEE 802.1Q VLAN trunking
- DHCP per departmental VLAN
- Static routing between branches
- Extended Named ACLs for security
- Rapid PVST+ spanning tree
- PortFast + BPDUGuard on access ports
