#!/usr/bin/env python3
"""
NexaTech Solutions - Network Configuration Generator
Generates Cisco IOS configurations for all six network devices.
Two-branch enterprise network: Kochi (HQ) and Bengaluru (Branch).
"""

import os
import ipaddress

# ─────────────────────────────────────────────
# Network Design Constants
# ─────────────────────────────────────────────

VLANS = {
    10: "HR",
    20: "IT",
    30: "Finance",
    40: "Servers",
    99: "Management",
}

KOCHI = {
    "site": "KOCHI",
    "router": "R1-KOCHI",
    "sw1": "SW1-KOCHI",
    "sw2": "SW2-KOCHI",
    "router_hostname": "R1-KOCHI",
    "sw1_hostname": "SW1-KOCHI",
    "sw2_hostname": "SW2-KOCHI",
    "vlans": {
        10: "192.168.10.0/24",
        20: "192.168.20.0/24",
        30: "192.168.30.0/24",
        40: "192.168.40.0/24",
        99: "192.168.99.0/24",
    },
    "wan_ip": "10.10.10.1",
    "wan_prefix": "30",
    "server_ip": "192.168.40.10",
    "server_gateway": "192.168.40.1",
    "dns_ip": "192.168.40.10",
    "mgmt_ip": "192.168.99.2",   # SW1 management
    "mgmt_ip_sw2": "192.168.99.3",
    "mgmt_gateway": "192.168.99.1",
}

BENGALURU = {
    "site": "BENGALURU",
    "router": "R2-BENGALURU",
    "sw1": "SW1-BENGALURU",
    "sw2": "SW2-BENGALURU",
    "router_hostname": "R2-BENGALURU",
    "sw1_hostname": "SW1-BENGALURU",
    "sw2_hostname": "SW2-BENGALURU",
    "vlans": {
        10: "192.168.110.0/24",
        20: "192.168.120.0/24",
        30: "192.168.130.0/24",
        40: "192.168.140.0/24",
        99: "192.168.199.0/24",
    },
    "wan_ip": "10.10.10.2",
    "wan_prefix": "30",
    "server_ip": "192.168.140.10",
    "server_gateway": "192.168.140.1",
    "dns_ip": "192.168.140.10",
    "mgmt_ip": "192.168.199.2",  # SW1 management
    "mgmt_ip_sw2": "192.168.199.3",
    "mgmt_gateway": "192.168.199.1",
}

WAN_NETWORK = "10.10.10.0/30"

ENABLE_SECRET = "NexaTech@2024"
CONSOLE_PASSWORD = "Console@2024"
VTY_PASSWORD = "VTY@2024"


# ─────────────────────────────────────────────
# Helper Functions
# ─────────────────────────────────────────────

def gateway(network_cidr: str) -> str:
    """Return the first usable host (.1) as a gateway address."""
    net = ipaddress.IPv4Network(network_cidr, strict=False)
    return str(net.network_address + 1)


def netmask(network_cidr: str) -> str:
    """Return subnet mask string."""
    return str(ipaddress.IPv4Network(network_cidr, strict=False).netmask)


def dhcp_start(network_cidr: str) -> str:
    """Return DHCP pool start (.10)."""
    net = ipaddress.IPv4Network(network_cidr, strict=False)
    return str(net.network_address + 10)


def dhcp_end(network_cidr: str) -> str:
    """Return DHCP pool end (second-to-last usable)."""
    net = ipaddress.IPv4Network(network_cidr, strict=False)
    return str(net.broadcast_address - 2)


def network_addr(network_cidr: str) -> str:
    return str(ipaddress.IPv4Network(network_cidr, strict=False).network_address)


def common_header(hostname: str, site: str) -> str:
    return f"""\
! ============================================================
! Device  : {hostname}
! Site    : {site}
! Project : NexaTech Solutions - Enterprise Network
! ============================================================
!
! --- Global Configuration ---
hostname {hostname}
no ip domain-lookup
enable secret {ENABLE_SECRET}
service password-encryption
!
banner motd #
  *******************************************
  * NexaTech Solutions - Authorised Access  *
  * Unauthorised access is strictly prohibited *
  *******************************************
#
!
! --- Console Security ---
line console 0
 password {CONSOLE_PASSWORD}
 login
 logging synchronous
 exec-timeout 10 0
!
! --- VTY (SSH/Telnet) Security ---
line vty 0 4
 password {VTY_PASSWORD}
 login
 transport input telnet
 exec-timeout 10 0
!
"""


def vlan_block(vlans: dict = VLANS) -> str:
    """VLAN creation commands (switch global config)."""
    lines = ["! --- VLAN Definitions ---"]
    for vid, name in vlans.items():
        lines.append(f"vlan {vid}")
        lines.append(f" name {name}")
        lines.append("!")
    return "\n".join(lines) + "\n"


def save_config(filename: str, content: str):
    os.makedirs("configs", exist_ok=True)
    path = os.path.join("configs", filename)
    with open(path, "w", newline="\n", encoding="utf-8") as f:
        f.write(content)
    print(f"  [OK] configs/{filename}")


# ─────────────────────────────────────────────
# Router Generator
# ─────────────────────────────────────────────

def gen_router(site: dict, remote_site: dict) -> str:
    """Generate full Router-on-a-Stick + DHCP + Static Routing + ACL config."""
    hostname = site["router_hostname"]
    vlans_cfg = site["vlans"]
    dns = site["dns_ip"]

    lines = [common_header(hostname, site["site"])]

    # ── Sub-interfaces for Router-on-a-Stick ──────────────────────────────
    lines.append("! --- Router-on-a-Stick: Sub-interfaces on G0/0 ---")
    lines.append("interface GigabitEthernet0/0")
    lines.append(" description Trunk-to-SW1-" + site["site"])
    lines.append(" no shutdown")
    lines.append("!")
    for vid, cidr in vlans_cfg.items():
        gw = gateway(cidr)
        nm = netmask(cidr)
        vlan_name = VLANS[vid]
        lines.append(f"! Sub-interface for VLAN {vid} ({vlan_name})")
        lines.append(f"interface GigabitEthernet0/0.{vid}")
        lines.append(f" description VLAN{vid}-{vlan_name}")
        lines.append(f" encapsulation dot1Q {vid}")
        lines.append(f" ip address {gw} {nm}")
        if vid == 99:
            lines.append(" ip access-group MGMT-ACCESS in")
        elif vid == 10:
            lines.append(f" ip helper-address {dns}")
            lines.append(" ip access-group VLAN10-HR in")
        elif vid == 30:
            lines.append(f" ip helper-address {dns}")
            lines.append(" ip access-group VLAN30-FINANCE in")
        else:
            lines.append(f" ip helper-address {dns}")
        lines.append(" no shutdown")
        lines.append("!")

    # ── WAN Interface ──────────────────────────────────────────────────────
    lines.append("! --- WAN Interface (Ethernet to remote router) ---")
    lines.append("interface GigabitEthernet0/1")
    lines.append(f" description WAN-Link-to-{remote_site['router_hostname']}")
    lines.append(f" ip address {site['wan_ip']} 255.255.255.252")
    lines.append(" no shutdown")
    lines.append("!")

    # ── DHCP Pools ────────────────────────────────────────────────────────
    lines.append("! --- DHCP Pools (one per departmental VLAN) ---")
    # Excluded addresses: .1 (gateway), .2 and .3 (switches), .10 (server)
    for vid, cidr in vlans_cfg.items():
        if vid == 99:
            continue  # Management IPs are static
        net = ipaddress.IPv4Network(cidr, strict=False)
        lines.append(f"! Exclude static addresses from VLAN {vid} pool")
        lines.append(f"ip dhcp excluded-address {gateway(cidr)} {str(net.network_address + 9)}")

    lines.append("!")
    for vid, cidr in vlans_cfg.items():
        if vid == 99:
            continue
        vlan_name = VLANS[vid]
        pool_name = f"{site['site']}-VLAN{vid}-{vlan_name}"
        lines.append(f"ip dhcp pool {pool_name}")
        lines.append(f" network {network_addr(cidr)} {netmask(cidr)}")
        lines.append(f" default-router {gateway(cidr)}")
        lines.append(f" dns-server {dns}")
        lines.append(f" domain-name nexatech.local")
        lines.append(f" lease 1")
        lines.append("!")

    # ── Static Routes ──────────────────────────────────────────────────────
    lines.append("! --- Static Routes to remote branch ---")
    for vid, cidr in remote_site["vlans"].items():
        lines.append(
            f"ip route {network_addr(cidr)} {netmask(cidr)} {remote_site['wan_ip']}"
            f"  ! Route to {remote_site['site']} VLAN {vid} ({VLANS[vid]})"
        )
    lines.append(f"! Default route stub toward WAN (optional)")
    lines.append("!")

    # ── ACLs ──────────────────────────────────────────────────────────────
    lines.append(_acl_block(site, remote_site))

    lines.append("! --- Save Configuration ---")
    lines.append("end")
    lines.append("write memory")
    lines.append("")
    return "\n".join(lines)


def _acl_block(site: dict, remote_site: dict) -> str:
    """
    ACL Rules:
      1. HR (VLAN10) cannot reach Finance (VLAN30) - local or remote.
      2. Finance (VLAN30) cannot reach HR (VLAN10) - local or remote.
      3. Management VLAN99 accessible only from IT (VLAN20).
      4. IT (VLAN20) has full access everywhere (no restriction).
      5. Inter-branch traffic allowed for IT and Servers.
    """
    hr_net   = network_addr(site["vlans"][10])
    it_net   = network_addr(site["vlans"][20])
    fin_net  = network_addr(site["vlans"][30])
    srv_net  = network_addr(site["vlans"][40])
    mgmt_net = network_addr(site["vlans"][99])
    nm24     = "255.255.255.0"
    wc24     = "0.0.0.255"

    # Remote networks
    r_hr  = network_addr(remote_site["vlans"][10])
    r_fin = network_addr(remote_site["vlans"][30])

    acl = f"""\
! ============================================================
! ACL DESIGN for {site['site']}
!
! VLAN10-HR-ACL  : Applied inbound on G0/0.10
!   - Deny HR to local Finance
!   - Deny HR to remote Finance
!   - Permit everything else from HR
!
! VLAN30-FINANCE-ACL : Applied inbound on G0/0.30
!   - Deny Finance to local HR
!   - Deny Finance to remote HR
!   - Permit everything else from Finance
!
! MGMT-ACCESS    : Applied inbound on G0/0.99
!   - Permit only IT subnet to reach management
!   - Deny all others
! ============================================================
!
! ACL: HR cannot access Finance (local + remote)
ip access-list extended VLAN10-HR
 10 remark Deny HR to local Finance VLAN
 10 deny ip {hr_net} {wc24} {fin_net} {wc24}
 20 remark Deny HR to remote Finance VLAN
 20 deny ip {hr_net} {wc24} {r_fin} {wc24}
 30 remark Permit HR to access everything else
 30 permit ip {hr_net} {wc24} any
!
! ACL: Finance cannot access HR (local + remote)
ip access-list extended VLAN30-FINANCE
 10 remark Deny Finance to local HR VLAN
 10 deny ip {fin_net} {wc24} {hr_net} {wc24}
 20 remark Deny Finance to remote HR VLAN
 20 deny ip {fin_net} {wc24} {r_hr} {wc24}
 30 remark Permit Finance to access everything else
 30 permit ip {fin_net} {wc24} any
!
! ACL: Management VLAN restricted to IT admins only
ip access-list extended MGMT-ACCESS
 10 remark Permit IT subnet to management
 10 permit ip {it_net} {wc24} {mgmt_net} {wc24}
 20 remark Deny all other traffic to management
 20 deny ip any {mgmt_net} {wc24}
 30 remark Permit remaining management-originated traffic
 30 permit ip any any
!
"""
    return acl


# ─────────────────────────────────────────────
# Switch Generators
# ─────────────────────────────────────────────

def gen_sw1(site: dict) -> str:
    """
    SW1 - Distribution/Access switch connected to router.
    Ports:
      Fa0/1-2 : HR   (VLAN 10) access
      Fa0/3-4 : IT   (VLAN 20) access
      G0/1    : Trunk to Router G0/0
      G0/2    : Trunk to SW2
    """
    hostname = site["sw1_hostname"]
    mgmt_cidr = site["vlans"][99]
    mgmt_ip = site["mgmt_ip"]
    nm = netmask(mgmt_cidr)

    lines = [common_header(hostname, site["site"])]
    lines.append(vlan_block())

    # ── Management SVI ─────────────────────────────────────────────────────
    lines.append("! --- Management SVI (VLAN 99) ---")
    lines.append("interface vlan 99")
    lines.append(f" description Management-Interface")
    lines.append(f" ip address {mgmt_ip} {nm}")
    lines.append(" no shutdown")
    lines.append("!")
    lines.append(f"ip default-gateway {gateway(mgmt_cidr)}")
    lines.append("!")

    # ── Access Ports ────────────────────────────────────────────────────────
    lines.append("! --- Access Ports ---")
    lines.append("! Fa0/1-2 : HR Department (VLAN 10)")
    for p in ["FastEthernet0/1", "FastEthernet0/2"]:
        lines += _access_port(p, 10, "HR-PC")
    lines.append("! Fa0/3-4 : IT Department (VLAN 20)")
    for p in ["FastEthernet0/3", "FastEthernet0/4"]:
        lines += _access_port(p, 20, "IT-PC")

    # ── Unused ports shutdown ───────────────────────────────────────────────
    lines.append("! --- Disable unused access ports (security) ---")
    for i in range(5, 25):
        port = f"FastEthernet0/{i}"
        lines.append(f"interface {port}")
        lines.append(" shutdown")
        lines.append(" switchport mode access")
        lines.append(f" switchport access vlan 99")
        lines.append("!")

    # ── Trunk Ports ─────────────────────────────────────────────────────────
    lines.append("! --- Trunk Ports ---")
    lines += _trunk_port("GigabitEthernet0/1", f"Trunk-to-Router-{site['site']}")
    lines += _trunk_port("GigabitEthernet0/2", f"Trunk-to-SW2-{site['site']}")

    lines.append("! --- Spanning Tree ---")
    lines.append("spanning-tree mode rapid-pvst")
    lines.append("spanning-tree vlan 10,20,30,40,99 priority 4096")
    lines.append("!")
    lines.append("end")
    lines.append("write memory")
    lines.append("")
    return "\n".join(lines)


def gen_sw2(site: dict) -> str:
    """
    SW2 - Access switch for Finance/Servers/Printers.
    Ports:
      Fa0/1-2 : Finance (VLAN 30) access
      Fa0/3   : Server  (VLAN 40) access
      Fa0/4   : Printer (VLAN 40) access
      G0/1    : Trunk to SW1 G0/2
    """
    hostname = site["sw2_hostname"]
    mgmt_cidr = site["vlans"][99]
    mgmt_ip = site["mgmt_ip_sw2"]
    nm = netmask(mgmt_cidr)

    lines = [common_header(hostname, site["site"])]
    lines.append(vlan_block())

    # ── Management SVI ─────────────────────────────────────────────────────
    lines.append("! --- Management SVI (VLAN 99) ---")
    lines.append("interface vlan 99")
    lines.append(f" description Management-Interface")
    lines.append(f" ip address {mgmt_ip} {nm}")
    lines.append(" no shutdown")
    lines.append("!")
    lines.append(f"ip default-gateway {gateway(mgmt_cidr)}")
    lines.append("!")

    # ── Access Ports ────────────────────────────────────────────────────────
    lines.append("! --- Access Ports ---")
    lines.append("! Fa0/1-2 : Finance Department (VLAN 30)")
    for p in ["FastEthernet0/1", "FastEthernet0/2"]:
        lines += _access_port(p, 30, "Finance-PC")
    lines.append("! Fa0/3 : Server (VLAN 40)")
    lines += _access_port("FastEthernet0/3", 40, "Server")
    lines.append("! Fa0/4 : Printer (VLAN 40)")
    lines += _access_port("FastEthernet0/4", 40, "Printer")

    # ── Unused ports ────────────────────────────────────────────────────────
    lines.append("! --- Disable unused access ports ---")
    for i in range(5, 25):
        port = f"FastEthernet0/{i}"
        lines.append(f"interface {port}")
        lines.append(" shutdown")
        lines.append(" switchport mode access")
        lines.append(f" switchport access vlan 99")
        lines.append("!")

    # ── Trunk ───────────────────────────────────────────────────────────────
    lines.append("! --- Trunk Port ---")
    lines += _trunk_port("GigabitEthernet0/1", f"Trunk-to-SW1-{site['site']}")

    lines.append("! --- Spanning Tree ---")
    lines.append("spanning-tree mode rapid-pvst")
    lines.append("spanning-tree vlan 10,20,30,40,99 priority 8192")
    lines.append("!")
    lines.append("end")
    lines.append("write memory")
    lines.append("")
    return "\n".join(lines)


def _access_port(interface: str, vlan: int, description: str) -> list:
    return [
        f"interface {interface}",
        f" description {description}-VLAN{vlan}",
        " switchport mode access",
        f" switchport access vlan {vlan}",
        " spanning-tree portfast",
        " spanning-tree bpduguard enable",
        " no shutdown",
        "!",
    ]


def _trunk_port(interface: str, description: str) -> list:
    return [
        f"interface {interface}",
        f" description {description}",
        " switchport mode trunk",
        " switchport trunk encapsulation dot1q",
        " switchport trunk allowed vlan 10,20,30,40,99",
        " switchport trunk native vlan 99",
        " no shutdown",
        "!",
    ]


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    print("\nNexaTech Network Configuration Generator")
    print("=" * 45)

    configs = [
        ("R1-KOCHI.txt",      gen_router(KOCHI, BENGALURU)),
        ("R2-BENGALURU.txt",  gen_router(BENGALURU, KOCHI)),
        ("SW1-KOCHI.txt",     gen_sw1(KOCHI)),
        ("SW2-KOCHI.txt",     gen_sw2(KOCHI)),
        ("SW1-BENGALURU.txt", gen_sw1(BENGALURU)),
        ("SW2-BENGALURU.txt", gen_sw2(BENGALURU)),
    ]

    for filename, content in configs:
        save_config(filename, content)

    print("\nAll configurations generated successfully.")
    print("Run validate.py to check for errors.\n")


if __name__ == "__main__":
    main()
