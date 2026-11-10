# Testing Guide — NexaTech Solutions Network

## Pre-Test Checklist

Before running any tests, confirm:
- [ ] All 6 device configs pasted and saved (`write memory`)
- [ ] All cables connected per NETWORK_TOPOLOGY.md
- [ ] All PC interfaces set to DHCP (Desktop > IP Configuration > DHCP)
- [ ] Kochi Server set to static 192.168.40.10
- [ ] Bengaluru Server set to static 192.168.140.10
- [ ] Both servers have DNS and HTTP services ON

---

## Test 1 — Basic Connectivity (Intra-VLAN)

Verify that PCs in the same VLAN can communicate.

| From | To | Expected | Command |
|---|---|---|---|
| Kochi HR-PC1 | Kochi HR-PC2 | Success | `ping 192.168.10.11` |
| Kochi IT-PC1 | Kochi IT-PC2 | Success | `ping 192.168.20.11` |
| Bengaluru HR-PC1 | Bengaluru HR-PC2 | Success | `ping 192.168.110.11` |

How to run in Packet Tracer:
1. Click PC → Desktop → Command Prompt
2. Type: `ping <target-ip>`

---

## Test 2 — Inter-VLAN Routing (Same Site)

Verify the router forwards between VLANs locally.

| From | To | Expected |
|---|---|---|
| Kochi HR-PC | Kochi IT-PC | Success |
| Kochi IT-PC | Kochi Finance-PC | Success |
| Kochi HR-PC | Kochi Server (192.168.40.10) | Success |
| Bengaluru IT-PC | Bengaluru Finance-PC | Success |

---

## Test 3 — WAN / Inter-Branch Connectivity

Verify static routing between Kochi and Bengaluru.

| From | To IP | Expected |
|---|---|---|
| Kochi HR-PC | 10.10.10.2 (R2 WAN) | Success |
| Kochi IT-PC | 192.168.120.10 (BLR IT) | Success |
| Kochi Server | 192.168.140.10 (BLR Server) | Success |
| Bengaluru IT-PC | 192.168.20.10 (KCH IT) | Success |

Verify with extended ping on routers:
```
R1-KOCHI# ping 10.10.10.2
R1-KOCHI# ping 192.168.110.1
R2-BENGALURU# ping 10.10.10.1
R2-BENGALURU# ping 192.168.10.1
```

---

## Test 4 — DHCP Functionality

1. On any PC: Desktop > IP Configuration > select DHCP
2. IP should be assigned within the correct subnet
3. Gateway and DNS should be populated automatically

| PC | Expected IP Range | Expected Gateway |
|---|---|---|
| Kochi HR-PC | 192.168.10.10 – .253 | 192.168.10.1 |
| Kochi IT-PC | 192.168.20.10 – .253 | 192.168.20.1 |
| Kochi Finance-PC | 192.168.30.10 – .253 | 192.168.30.1 |
| Bengaluru HR-PC | 192.168.110.10 – .253 | 192.168.110.1 |

Verify on router:
```
R1-KOCHI# show ip dhcp binding
R1-KOCHI# show ip dhcp pool
```

---

## Test 5 — ACL Verification

### 5a. HR cannot access Finance

```
From: Kochi HR-PC  →  To: 192.168.30.10 (Kochi Finance)
Expected: Request timed out (BLOCKED)

From: Kochi HR-PC  →  To: 192.168.130.10 (Bengaluru Finance)
Expected: Request timed out (BLOCKED)
```

### 5b. Finance cannot access HR

```
From: Kochi Finance-PC  →  To: 192.168.10.10 (Kochi HR)
Expected: Request timed out (BLOCKED)
```

### 5c. IT has full access

```
From: Kochi IT-PC  →  To: 192.168.30.10 (Finance)  → PASS
From: Kochi IT-PC  →  To: 192.168.10.10 (HR)       → PASS
From: Kochi IT-PC  →  To: 192.168.40.10 (Server)   → PASS
From: Kochi IT-PC  →  To: 192.168.110.10 (BLR HR)  → PASS
```

### 5d. Management VLAN restricted

Only IT PCs should be able to ping the management IPs (192.168.99.x).
HR and Finance PCs should be blocked.

---

## Test 6 — DNS Resolution

On any PC, open Desktop > Web Browser and type:
```
http://kochi-server.nexatech.local
```
Expected: Cisco Packet Tracer default HTTP page loads.

Or use command prompt:
```
C:\> nslookup kochi-server.nexatech.local
```

---

## Test 7 — Management Access (Telnet)

From an IT PC, telnet to a switch management IP:
```
C:\> telnet 192.168.99.2
Password: VTY@2024
```
Expected: Switch CLI appears.

From an HR PC, the same telnet should fail (blocked by MGMT-ACCESS ACL).

---

## Verification Commands (Router CLI)

```
show ip interface brief         ! Interface status and IPs
show ip route                   ! Routing table
show ip dhcp binding            ! Active DHCP leases
show ip dhcp pool               ! Pool statistics
show access-lists               ! ACL hit counters
show vlan brief                 ! (on switches)
show interfaces trunk           ! Trunk port status
show spanning-tree              ! STP topology
```

---

## Common Issues and Fixes

| Symptom | Likely Cause | Fix |
|---|---|---|
| PC gets 0.0.0.0 from DHCP | DHCP pool not configured | Check `show ip dhcp pool` on router |
| Cannot ping across VLANs | Sub-interface down | `no shutdown` on G0/0 and sub-interfaces |
| No inter-branch ping | Static route missing | Check `show ip route` on both routers |
| ACL blocking unexpected traffic | ACL sequence error | Check `show access-lists` hit counters |
| Trunk not passing VLANs | VLAN not in allowed list | Check `show interfaces trunk` |
| Switch has no management IP | SVI VLAN 99 down | Ensure VLAN 99 exists and SVI is `no shutdown` |
