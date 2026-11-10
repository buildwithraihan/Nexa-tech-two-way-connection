# Packet Tracer Build Guide — NexaTech Solutions
# Step-by-Step Manual Topology Construction

Packet Tracer Version: 9.0.0
Format Investigation Result: .pkt files use a proprietary encrypted/compressed
binary format (magic bytes 0x61 0xFD — not ZIP, not XML, not JSON). Cisco has
never published a topology import API or CLI automation interface for this format.
No legitimate external tool can write a valid .pkt file without reverse-engineering
Cisco's closed binary codec. Therefore this guide provides the exact GUI procedure.

Estimated time to complete: 45–60 minutes.

---

## PHASE 1 — Open Packet Tracer and Set Up Workspace

1. Launch Cisco Packet Tracer 9.0.0
2. Close any open files: File > New
3. Make sure you are in Logical View (bottom-left tab, default)
4. Zoom the workspace out slightly using Ctrl+Scroll or the magnifier so you have
   space for two groups of devices (left = Kochi, right = Bengaluru)

---

## PHASE 2 — Add All Devices

Use the Device Toolbar at the bottom of the screen.

### 2.1 — Add Kochi HQ Devices (place on LEFT side of workspace)

#### R1-KOCHI (Router)
1. Click "Network Devices" (first icon, looks like a router)
2. Click "Routers" subcategory
3. Find "2911" — drag it onto the canvas, left side
4. Double-click the device label and rename it: R1-KOCHI

#### SW1-KOCHI (Switch)
1. Click "Network Devices" > "Switches"
2. Find "2960-24TT" — drag it below and right of R1-KOCHI
3. Rename it: SW1-KOCHI

#### SW2-KOCHI (Switch)
1. Same as above — drag a second 2960-24TT below SW1-KOCHI
2. Rename it: SW2-KOCHI

#### Kochi End Devices (place around the switches)
Add these from "End Devices" category:

| Device Type | Qty | Labels |
|---|---|---|
| PC (generic) | 4 | HR-PC1-K, HR-PC2-K, IT-PC1-K, IT-PC2-K |
| PC (generic) | 2 | FIN-PC1-K, FIN-PC2-K |
| Server-PT | 1 | SERVER-KOCHI |
| Printer (generic) | 1 | PRINTER-KOCHI |

To rename: double-click the label under each device and type the new name.

### 2.2 — Add Bengaluru Branch Devices (place on RIGHT side of workspace)

#### R2-BENGALURU (Router)
1. Routers > 2911 — drag to right side
2. Rename: R2-BENGALURU

#### SW1-BENGALURU and SW2-BENGALURU
1. Two more 2960-24TT switches
2. Rename them: SW1-BENGALURU and SW2-BENGALURU

#### Bengaluru End Devices

| Device Type | Qty | Labels |
|---|---|---|
| PC (generic) | 4 | HR-PC1-B, HR-PC2-B, IT-PC1-B, IT-PC2-B |
| PC (generic) | 2 | FIN-PC1-B, FIN-PC2-B |
| Server-PT | 1 | SERVER-BENGALURU |
| Printer (generic) | 1 | PRINTER-BENGALURU |

Total devices placed: 2 routers + 4 switches + 16 end devices = 22 objects

---

## PHASE 3 — Cable All Connections

Use the Connections toolbar (lightning bolt icon at bottom).
Select "Copper Straight-Through" for all links EXCEPT the WAN link.

### 3.1 — Kochi HQ Cabling

| Cable | From | Port | To | Port |
|---|---|---|---|---|
| Straight | R1-KOCHI | GigabitEthernet0/0 | SW1-KOCHI | GigabitEthernet0/1 |
| Straight | SW1-KOCHI | GigabitEthernet0/2 | SW2-KOCHI | GigabitEthernet0/1 |
| Straight | SW1-KOCHI | FastEthernet0/1 | HR-PC1-K | FastEthernet0 |
| Straight | SW1-KOCHI | FastEthernet0/2 | HR-PC2-K | FastEthernet0 |
| Straight | SW1-KOCHI | FastEthernet0/3 | IT-PC1-K | FastEthernet0 |
| Straight | SW1-KOCHI | FastEthernet0/4 | IT-PC2-K | FastEthernet0 |
| Straight | SW2-KOCHI | FastEthernet0/1 | FIN-PC1-K | FastEthernet0 |
| Straight | SW2-KOCHI | FastEthernet0/2 | FIN-PC2-K | FastEthernet0 |
| Straight | SW2-KOCHI | FastEthernet0/3 | SERVER-KOCHI | FastEthernet0 |
| Straight | SW2-KOCHI | FastEthernet0/4 | PRINTER-KOCHI | FastEthernet0 |

### 3.2 — WAN Link

| Cable | From | Port | To | Port |
|---|---|---|---|---|
| Copper Cross-Over | R1-KOCHI | GigabitEthernet0/1 | R2-BENGALURU | GigabitEthernet0/1 |

Note: PT 9 auto-detects MDI/MDI-X. If you see an amber link after using straight-through
for this connection, switch to crossover. If it comes up green with straight-through, leave it.

### 3.3 — Bengaluru Branch Cabling

| Cable | From | Port | To | Port |
|---|---|---|---|---|
| Straight | R2-BENGALURU | GigabitEthernet0/0 | SW1-BENGALURU | GigabitEthernet0/1 |
| Straight | SW1-BENGALURU | GigabitEthernet0/2 | SW2-BENGALURU | GigabitEthernet0/1 |
| Straight | SW1-BENGALURU | FastEthernet0/1 | HR-PC1-B | FastEthernet0 |
| Straight | SW1-BENGALURU | FastEthernet0/2 | HR-PC2-B | FastEthernet0 |
| Straight | SW1-BENGALURU | FastEthernet0/3 | IT-PC1-B | FastEthernet0 |
| Straight | SW1-BENGALURU | FastEthernet0/4 | IT-PC2-B | FastEthernet0 |
| Straight | SW2-BENGALURU | FastEthernet0/1 | FIN-PC1-B | FastEthernet0 |
| Straight | SW2-BENGALURU | FastEthernet0/2 | FIN-PC2-B | FastEthernet0 |
| Straight | SW2-BENGALURU | FastEthernet0/3 | SERVER-BENGALURU | FastEthernet0 |
| Straight | SW2-BENGALURU | FastEthernet0/4 | PRINTER-BENGALURU | FastEthernet0 |

All cables should show green indicator lights within a few seconds. If a link stays amber:
- Check you selected the correct port on each device
- Amber on trunk links is normal until VLANs are configured
- Amber on PC ports resolves after DHCP is configured

---

## PHASE 4 — Apply Device Configurations

Configure devices in this exact order. Apply the switch configs BEFORE router configs
so VLANs exist before the router sends traffic.

### Configuration Order
```
1. SW1-KOCHI
2. SW2-KOCHI
3. SW1-BENGALURU
4. SW2-BENGALURU
5. R1-KOCHI
6. R2-BENGALURU
```

### How to Paste a Config

1. Click the device in the canvas
2. Click the "CLI" tab in the panel that opens
3. Press Enter to activate the prompt
4. If you see `Switch>` or `Router>`, type:
   ```
   enable
   ```
5. Type:
   ```
   conf t
   ```
6. Open the corresponding file from `configs/` in a text editor (Notepad, VS Code, etc.)
7. Select All (Ctrl+A) and Copy (Ctrl+C)
8. Click inside the Packet Tracer CLI window
9. Paste with Ctrl+V
10. Wait for all lines to process (PT pastes about 5-10 lines per second)
11. When the prompt returns, type:
    ```
    end
    write memory
    ```

> Important: Do NOT paste the `enable` line or `conf t` line from the config file
> if you already typed them. The config files include those lines, so PT will handle
> them correctly either way — duplicate commands are harmless.

---

## PHASE 5 — Configure Server Static IPs

### SERVER-KOCHI — 192.168.40.10

1. Click SERVER-KOCHI
2. Click "Desktop" tab
3. Click "IP Configuration"
4. Select "Static"
5. Enter:
   - IP Address: 192.168.40.10
   - Subnet Mask: 255.255.255.0
   - Default Gateway: 192.168.40.1
   - DNS Server: 192.168.40.10
6. Close the IP Configuration window

### SERVER-BENGALURU — 192.168.140.10

1. Click SERVER-BENGALURU > Desktop > IP Configuration
2. Select Static, enter:
   - IP Address: 192.168.140.10
   - Subnet Mask: 255.255.255.0
   - Default Gateway: 192.168.140.1
   - DNS Server: 192.168.140.10
3. Close

---

## PHASE 6 — Enable DNS Service on Both Servers

### SERVER-KOCHI DNS Setup

1. Click SERVER-KOCHI
2. Click the "Services" tab
3. Click "DNS" in the left panel
4. Click the "On" toggle to enable DNS
5. Add the following DNS records (type each and click "Add"):

   | Name | Type | Address |
   |---|---|---|
   | kochi-server.nexatech.local | A Record | 192.168.40.10 |
   | bengaluru-server.nexatech.local | A Record | 192.168.140.10 |
   | r1-kochi.nexatech.local | A Record | 192.168.99.1 |
   | r2-bengaluru.nexatech.local | A Record | 192.168.199.1 |

6. Click "HTTP" in the left panel > make sure it is "On"

### SERVER-BENGALURU DNS Setup

1. Click SERVER-BENGALURU > Services > DNS > On
2. Add the same 4 DNS records as above
3. Services > HTTP > On

---

## PHASE 7 — Configure PC Static/DHCP Settings

### Departmental PCs (DHCP)

For each PC (HR, IT, Finance):
1. Click the PC > Desktop > IP Configuration
2. Select "DHCP"
3. Wait 10-15 seconds — the PC will receive:
   - An IP in the correct subnet
   - The gateway (.1 of its VLAN)
   - The DNS server IP

### Printers (Static recommended)

For PRINTER-KOCHI:
- IP: 192.168.40.11
- Mask: 255.255.255.0
- Gateway: 192.168.40.1
- DNS: 192.168.40.10

For PRINTER-BENGALURU:
- IP: 192.168.140.11
- Mask: 255.255.255.0
- Gateway: 192.168.140.1
- DNS: 192.168.140.10

---

## PHASE 8 — Save the Project

1. File > Save As
2. Navigate to your project folder:
   `NexaTech-Network\` (or wherever you want to save it)
3. File name: `NexaTech_Two_Branch_Network`
4. File type is automatically .pkt
5. Click Save

The file `NexaTech_Two_Branch_Network.pkt` is now saved and can be opened
by any Packet Tracer 9.x installation.

---

## PHASE 9 — Verification

Run these commands to confirm the network is working:

### On R1-KOCHI (CLI tab):
```
show ip interface brief
show ip route
show ip dhcp binding
show access-lists
```

### On SW1-KOCHI (CLI tab):
```
show vlan brief
show interfaces trunk
show spanning-tree vlan 10
```

### On any HR-PC (Desktop > Command Prompt):
```
ping 192.168.20.10    (should SUCCEED — HR to IT)
ping 192.168.30.10    (should FAIL — HR to Finance, ACL blocked)
ping 192.168.40.10    (should SUCCEED — HR to Server)
ping 192.168.110.10   (should SUCCEED — Kochi HR to Bengaluru HR)
ping 192.168.130.10   (should FAIL — Kochi HR to Bengaluru Finance)
```

### On any IT-PC:
```
ping 192.168.10.10    (SUCCEED — IT to HR)
ping 192.168.30.10    (SUCCEED — IT to Finance)
ping 192.168.40.10    (SUCCEED — IT to Server)
ping 192.168.140.10   (SUCCEED — IT to Bengaluru Server)
```

See TESTING_GUIDE.md for the full test suite.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| All switch ports stay amber | Paste SW config again; confirm VLANs with `show vlan brief` |
| PCs not getting DHCP | Check R1/R2 CLI: `show ip dhcp pool` and `show ip dhcp binding` |
| Inter-VLAN ping fails | Run `show ip interface brief` on router — all sub-interfaces must be UP |
| Inter-branch ping fails | Run `show ip route` on both routers — all 5 remote routes must be present |
| ACL not blocking | Confirm `show access-lists` shows the ACL; check `ip access-group` with `show run` |
| DNS not resolving | Confirm server DNS service is ON and PC DNS server field has the server IP |
| Config paste stops mid-way | PT may scroll past banner; just wait, or break the config into sections |

---

## Why a .pkt File Cannot Be Generated Externally

The investigation of the installed Packet Tracer 9.0.0 binary confirmed:

1. `.pkt` files start with bytes 0x61 0xFD — a proprietary compression/encryption
   header, NOT a standard ZIP (0x50 0x4B) or XML/JSON text format.
2. The `bin/` directory contains only Qt runtime DLLs and the main executable.
   There is no topology import CLI, no REST API, no Python binding.
3. The `extensions/` folder contains IoT device scripts (.pts) and activity
   sequencers — none of these expose topology creation capabilities.
4. The `templates/` folder contains device definition files (.ptd) for device
   appearance only, not topology instantiation.
5. Cisco's published Packet Tracer documentation confirms there is no
   supported programmatic topology import mechanism as of version 9.x.

Any tool claiming to generate a valid .pkt from outside Packet Tracer is either
reverse-engineering the binary format without Cisco's authorization, or producing
a file that will fail to open or silently corrupt your project.
