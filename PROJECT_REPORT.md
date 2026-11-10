# Project Report — NexaTech Solutions Enterprise Network

**Course:** BCA Computer Networks  
**Project Title:** Two-Branch Enterprise Network Design and Implementation  
**Tools:** Cisco Packet Tracer, Python 3  

---

## 1. Introduction

This project designs and implements a complete enterprise network for NexaTech Solutions,
a fictional company with offices in Kochi (HQ) and Bengaluru (Branch). The goal is to
demonstrate core networking concepts including VLAN segmentation, inter-VLAN routing,
WAN connectivity, DHCP automation, and ACL-based security in a realistic topology.

---

## 2. Objectives

- Design a scalable two-site enterprise network
- Implement VLAN-based departmental segmentation
- Configure Router-on-a-Stick for inter-VLAN routing
- Establish WAN connectivity via static routing
- Automate DHCP address assignment per department
- Enforce security policies using Access Control Lists
- Manage switches via a dedicated Management VLAN
- Automate configuration generation using Python

---

## 3. Network Architecture

### 3.1 Physical Design

The network uses a hierarchical model:
- **Core layer**: Two Cisco 2911 routers handle inter-VLAN routing and WAN connectivity
- **Distribution layer**: SW1 at each site trunks to the router and downstream to SW2
- **Access layer**: SW2 at each site connects end-user devices

### 3.2 VLAN Design

Departmental VLANs isolate traffic and reduce broadcast domains:

| VLAN | Department | Kochi | Bengaluru |
|---|---|---|---|
| 10 | HR | 192.168.10.0/24 | 192.168.110.0/24 |
| 20 | IT | 192.168.20.0/24 | 192.168.120.0/24 |
| 30 | Finance | 192.168.30.0/24 | 192.168.130.0/24 |
| 40 | Servers | 192.168.40.0/24 | 192.168.140.0/24 |
| 99 | Management | 192.168.99.0/24 | 192.168.199.0/24 |

Separate subnet ranges per site (10.x vs 110.x, etc.) prevent IP conflicts and allow
unambiguous static routing.

### 3.3 Router-on-a-Stick

Each router uses a single physical interface (G0/0) divided into 802.1Q sub-interfaces,
one per VLAN. This reduces hardware requirements while providing full inter-VLAN routing.
The G0/1 interface connects the two routers over a /30 WAN segment (10.10.10.0/30).

### 3.4 Static Routing

Each router has 5 static routes pointing all remote branch subnets to the remote WAN IP.
This provides full reachability between sites with explicit, predictable paths.

---

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| IEEE 802.1Q VLANs | Traffic segmentation |
| Router-on-a-Stick | Inter-VLAN routing |
| Cisco IOS DHCP | Automatic IP assignment |
| Extended Named ACLs | Access control and security |
| Static Routing | Inter-branch reachability |
| Rapid PVST+ | Loop prevention on switches |
| PortFast + BPDUGuard | Fast convergence, security |
| Management VLAN 99 | Out-of-band switch management |
| Python 3 | Config generation and validation |

---

## 5. Security Implementation

### 5.1 VLAN Security
- Management VLAN 99 is separate from user VLANs
- Unused switch ports are shut down and assigned to VLAN 99
- Native VLAN set to 99 on all trunks

### 5.2 Access Control Lists

Three named extended ACLs enforce departmental separation:

**VLAN10-HR**: Applied inbound on the HR sub-interface
- Prevents HR from reaching Finance at either site
- All other HR traffic is permitted

**VLAN30-FINANCE**: Applied inbound on the Finance sub-interface
- Prevents Finance from reaching HR at either site
- All other Finance traffic is permitted

**MGMT-ACCESS**: Applied inbound on the Management sub-interface
- Only IT subnet is allowed to access management addresses
- All other departments are blocked from management

### 5.3 Device Hardening
- Enable secret password (encrypted)
- Service password-encryption enabled
- No IP domain-lookup to prevent DNS delays on console
- VTY and console timeouts (10 minutes)
- MOTD banner on all devices
- BPDUGuard on all access ports (prevents rogue switch attacks)

---

## 6. Python Automation

Two Python scripts automate the project:

**generate.py**
- Uses `ipaddress` module for mathematically correct subnet calculations
- Generates all 6 device configs from a single data structure
- Produces DHCP excluded ranges, pool configurations, and static routes automatically
- Applies ACLs and sub-interfaces via parameterized functions

**validate.py**
- Device-type-aware checks (router checks only on R1/R2, switch checks only on SW*)
- Validates hostnames, IP syntax, duplicate IPs, DHCP pools, static routes, ACLs
- Checks trunk VLAN lists, management SVIs, security hardening
- Produces PASS/FAIL/WARN report with error count

---

## 7. Packet Tracer Automation Limitations

Cisco Packet Tracer (as of version 8.x) does not expose a public API or accept `.pkt` file
import from external automation tools. Therefore:

- No `.pkt` file is generated or claimed to be generated
- The topology is built manually in Packet Tracer following the guide in NETWORK_TOPOLOGY.md
- All device configurations are ready for direct CLI paste
- The Python automation covers config generation and validation only

---

## 8. Results

After applying all configurations:
- All 6 device configs validated with 0 errors, 0 warnings
- DHCP assigns correct IPs to all departmental PCs
- Inter-VLAN routing works within each site
- Static routes provide full inter-branch connectivity
- ACLs correctly block HR-Finance cross-access
- IT administrators have unrestricted access to all segments
- Management VLAN is accessible only from IT subnet
- Servers respond to HTTP and DNS queries from all permitted VLANs

---

## 9. Conclusion

This project demonstrates a complete, production-style enterprise network design implemented
in a simulation environment. The combination of VLAN segmentation, Router-on-a-Stick, DHCP
automation, static routing, and layered ACL security represents standard real-world network
engineering practice. The Python automation scripts reduce manual errors and make the
configuration fully reproducible.
