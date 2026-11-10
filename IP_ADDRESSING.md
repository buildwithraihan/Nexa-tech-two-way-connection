# IP Addressing Plan — NexaTech Solutions

## WAN Segment

| Device | Interface | IP Address | Subnet Mask | Network |
|---|---|---|---|---|
| R1-KOCHI | G0/1 | 10.10.10.1 | 255.255.255.252 | 10.10.10.0/30 |
| R2-BENGALURU | G0/1 | 10.10.10.2 | 255.255.255.252 | 10.10.10.0/30 |

## Kochi HQ — Sub-interface Gateways (R1 G0/0)

| VLAN | Department | Network | Gateway (R1) | Subnet Mask |
|---|---|---|---|---|
| 10 | HR | 192.168.10.0/24 | 192.168.10.1 | 255.255.255.0 |
| 20 | IT | 192.168.20.0/24 | 192.168.20.1 | 255.255.255.0 |
| 30 | Finance | 192.168.30.0/24 | 192.168.30.1 | 255.255.255.0 |
| 40 | Servers | 192.168.40.0/24 | 192.168.40.1 | 255.255.255.0 |
| 99 | Management | 192.168.99.0/24 | 192.168.99.1 | 255.255.255.0 |

## Kochi — DHCP Pools

| VLAN | Pool Range | Excluded (Static) |
|---|---|---|
| 10 HR | 192.168.10.10 – 192.168.10.253 | .1 (GW), .2–.9 |
| 20 IT | 192.168.20.10 – 192.168.20.253 | .1 (GW), .2–.9 |
| 30 Finance | 192.168.30.10 – 192.168.30.253 | .1 (GW), .2–.9 |
| 40 Servers | 192.168.40.10 – 192.168.40.253 | .1 (GW), .2–.9 |

## Kochi — Static Addresses

| Device | IP Address | VLAN | Gateway |
|---|---|---|---|
| Server (Kochi) | 192.168.40.10 | 40 | 192.168.40.1 |
| Printer (Kochi) | 192.168.40.11 | 40 | 192.168.40.1 |
| SW1-KOCHI (Mgmt) | 192.168.99.2 | 99 | 192.168.99.1 |
| SW2-KOCHI (Mgmt) | 192.168.99.3 | 99 | 192.168.99.1 |

## Bengaluru Branch — Sub-interface Gateways (R2 G0/0)

| VLAN | Department | Network | Gateway (R2) | Subnet Mask |
|---|---|---|---|---|
| 10 | HR | 192.168.110.0/24 | 192.168.110.1 | 255.255.255.0 |
| 20 | IT | 192.168.120.0/24 | 192.168.120.1 | 255.255.255.0 |
| 30 | Finance | 192.168.130.0/24 | 192.168.130.1 | 255.255.255.0 |
| 40 | Servers | 192.168.140.0/24 | 192.168.140.1 | 255.255.255.0 |
| 99 | Management | 192.168.199.0/24 | 192.168.199.1 | 255.255.255.0 |

## Bengaluru — DHCP Pools

| VLAN | Pool Range | Excluded (Static) |
|---|---|---|
| 10 HR | 192.168.110.10 – 192.168.110.253 | .1 (GW), .2–.9 |
| 20 IT | 192.168.120.10 – 192.168.120.253 | .1 (GW), .2–.9 |
| 30 Finance | 192.168.130.10 – 192.168.130.253 | .1 (GW), .2–.9 |
| 40 Servers | 192.168.140.10 – 192.168.140.253 | .1 (GW), .2–.9 |

## Bengaluru — Static Addresses

| Device | IP Address | VLAN | Gateway |
|---|---|---|---|
| Server (Bengaluru) | 192.168.140.10 | 40 | 192.168.140.1 |
| Printer (Bengaluru) | 192.168.140.11 | 40 | 192.168.140.1 |
| SW1-BENGALURU (Mgmt) | 192.168.199.2 | 99 | 192.168.199.1 |
| SW2-BENGALURU (Mgmt) | 192.168.199.3 | 99 | 192.168.199.1 |

## DNS Records (Internal — nexatech.local)

| Hostname | IP Address | Purpose |
|---|---|---|
| kochi-server.nexatech.local | 192.168.40.10 | Kochi file/web server |
| bengaluru-server.nexatech.local | 192.168.140.10 | Bengaluru file/web server |
| r1-kochi.nexatech.local | 192.168.99.1 | Kochi router |
| r2-bengaluru.nexatech.local | 192.168.199.1 | Bengaluru router |
