# Device Configuration Reference — NexaTech Solutions

All configuration files are in `configs/`. Paste them directly into Packet Tracer CLI.

---

## Deployment Order

Configure in this exact sequence to avoid dependency errors:

```
1. SW1-KOCHI        (VLANs must exist before trunk negotiation)
2. SW2-KOCHI
3. R1-KOCHI         (Sub-interfaces, DHCP, ACLs, static routes)
4. SW1-BENGALURU
5. SW2-BENGALURU
6. R2-BENGALURU
```

---

## How to Paste Configs in Packet Tracer

1. Click on a device → click the **CLI** tab
2. Press **Enter** to get the `>` prompt
3. Type `enable` → press Enter
4. Type `conf t` → press Enter
5. Open the relevant `.txt` file from `configs/`
6. Select All (Ctrl+A) → Copy (Ctrl+C)
7. Click inside the Packet Tracer CLI window
8. Paste (Ctrl+V) — wait for all commands to process
9. Type `end` then `write memory`

> Tip: If you see `% Invalid input detected`, you are likely still in User EXEC mode.
> Type `enable` then `conf t` first.

---

## Router Configuration Summary

### R1-KOCHI

| Interface | Role | IP |
|---|---|---|
| G0/0 | Trunk to SW1-KOCHI | no IP (native) |
| G0/0.10 | VLAN 10 HR gateway | 192.168.10.1/24 |
| G0/0.20 | VLAN 20 IT gateway | 192.168.20.1/24 |
| G0/0.30 | VLAN 30 Finance gateway | 192.168.30.1/24 |
| G0/0.40 | VLAN 40 Servers gateway | 192.168.40.1/24 |
| G0/0.99 | VLAN 99 Mgmt gateway | 192.168.99.1/24 |
| G0/1 | WAN to R2 | 10.10.10.1/30 |

DHCP pools: KOCHI-VLAN10-HR, KOCHI-VLAN20-IT, KOCHI-VLAN30-Finance, KOCHI-VLAN40-Servers

Static routes: 5 routes to all Bengaluru VLANs via 10.10.10.2

ACLs: VLAN10-HR (in on G0/0.10), VLAN30-FINANCE (in on G0/0.30), MGMT-ACCESS (in on G0/0.99)

### R2-BENGALURU

| Interface | Role | IP |
|---|---|---|
| G0/0 | Trunk to SW1-BENGALURU | no IP (native) |
| G0/0.10 | VLAN 10 HR gateway | 192.168.110.1/24 |
| G0/0.20 | VLAN 20 IT gateway | 192.168.120.1/24 |
| G0/0.30 | VLAN 30 Finance gateway | 192.168.130.1/24 |
| G0/0.40 | VLAN 40 Servers gateway | 192.168.140.1/24 |
| G0/0.99 | VLAN 99 Mgmt gateway | 192.168.199.1/24 |
| G0/1 | WAN to R1 | 10.10.10.2/30 |

DHCP pools: BENGALURU-VLAN10-HR, BENGALURU-VLAN20-IT, BENGALURU-VLAN30-Finance, BENGALURU-VLAN40-Servers

Static routes: 5 routes to all Kochi VLANs via 10.10.10.1

ACLs: VLAN10-HR (in on G0/0.10), VLAN30-FINANCE (in on G0/0.30), MGMT-ACCESS (in on G0/0.99)

---

## Switch Configuration Summary

### SW1-KOCHI / SW1-BENGALURU

| Port | VLAN | Mode | Connected To |
|---|---|---|---|
| Fa0/1 | 10 (HR) | Access | HR-PC1 |
| Fa0/2 | 10 (HR) | Access | HR-PC2 |
| Fa0/3 | 20 (IT) | Access | IT-PC1 |
| Fa0/4 | 20 (IT) | Access | IT-PC2 |
| Fa0/5-24 | 99 | Access | Shutdown |
| G0/1 | 10,20,30,40,99 | Trunk | Router G0/0 |
| G0/2 | 10,20,30,40,99 | Trunk | SW2 G0/1 |

SVI: VLAN 99 management IP  
STP: Rapid PVST+, priority 4096 (acts as STP root)

### SW2-KOCHI / SW2-BENGALURU

| Port | VLAN | Mode | Connected To |
|---|---|---|---|
| Fa0/1 | 30 (Finance) | Access | Finance-PC1 |
| Fa0/2 | 30 (Finance) | Access | Finance-PC2 |
| Fa0/3 | 40 (Servers) | Access | Server |
| Fa0/4 | 40 (Servers) | Access | Printer |
| Fa0/5-24 | 99 | Access | Shutdown |
| G0/1 | 10,20,30,40,99 | Trunk | SW1 G0/2 |

SVI: VLAN 99 management IP  
STP: Rapid PVST+, priority 8192

---

## Server Configuration (Manual in Packet Tracer)

### Kochi Server — 192.168.40.10

1. Click Server → Desktop tab → IP Configuration
   - IP: 192.168.40.10
   - Mask: 255.255.255.0
   - Gateway: 192.168.40.1
   - DNS: 192.168.40.10

2. Click Services tab → DNS → Turn ON
   Add records:
   - kochi-server.nexatech.local → 192.168.40.10
   - bengaluru-server.nexatech.local → 192.168.140.10
   - r1-kochi.nexatech.local → 192.168.99.1
   - r2-bengaluru.nexatech.local → 192.168.199.1

3. Click Services tab → HTTP → Turn ON (for web testing)

### Bengaluru Server — 192.168.140.10

1. Click Server → Desktop tab → IP Configuration
   - IP: 192.168.140.10
   - Mask: 255.255.255.0
   - Gateway: 192.168.140.1
   - DNS: 192.168.140.10

2. Click Services tab → DNS → Turn ON (add same records as above)

3. Click Services tab → HTTP → Turn ON

---

## ACL Reference

### VLAN10-HR (applied inbound on G0/0.10)

```
deny ip <HR-net> <Finance-net>        ! HR cannot ping Finance (local)
deny ip <HR-net> <Remote-Finance-net> ! HR cannot ping Finance (remote)
permit ip <HR-net> any                ! HR can reach everything else
```

### VLAN30-FINANCE (applied inbound on G0/0.30)

```
deny ip <Finance-net> <HR-net>        ! Finance cannot ping HR (local)
deny ip <Finance-net> <Remote-HR-net> ! Finance cannot ping HR (remote)
permit ip <Finance-net> any           ! Finance can reach everything else
```

### MGMT-ACCESS (applied inbound on G0/0.99)

```
permit ip <IT-net> <Mgmt-net>         ! Only IT can access management
deny ip any <Mgmt-net>                ! Block all others to management
permit ip any any                     ! Allow management-originated traffic
```
