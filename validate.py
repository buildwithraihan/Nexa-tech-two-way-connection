#!/usr/bin/env python3
"""
NexaTech Solutions - Configuration Validator
Checks generated Cisco IOS configs for common errors.
Device-type aware: router checks only run on R1/R2, switch checks only on SW*.
"""

import os
import re
import ipaddress
from pathlib import Path

CONFIG_DIR = "configs"
PASS = "[PASS]"
FAIL = "[FAIL]"
WARN = "[WARN]"

errors_found = 0
warnings_found = 0


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def is_router(device: str) -> bool:
    return device.startswith("R1") or device.startswith("R2")


def is_switch(device: str) -> bool:
    return device.startswith("SW")


def report(status: str, device: str, message: str):
    global errors_found, warnings_found
    print(f"  {status} {device}: {message}")
    if status == FAIL:
        errors_found += 1
    elif status == WARN:
        warnings_found += 1


# ─────────────────────────────────────────────
# Check Functions
# ─────────────────────────────────────────────

def check_hostnames(device: str, content: str):
    expected = device.replace(".txt", "")
    if f"hostname {expected}" in content:
        report(PASS, device, f"Hostname set to '{expected}'")
    else:
        report(FAIL, device, f"Missing hostname. Expected 'hostname {expected}'")


def check_vlans(device: str, content: str):
    """VLANs are defined on switches only."""
    if not is_switch(device):
        return
    for vid in [10, 20, 30, 40, 99]:
        if f"vlan {vid}" in content:
            report(PASS, device, f"VLAN {vid} defined")
        else:
            report(FAIL, device, f"VLAN {vid} missing")


def check_ip_addresses(device: str, content: str):
    """Validate all IP address statements are syntactically valid."""
    ip_lines = re.findall(r"ip address (\S+) (\S+)", content)
    for ip_str, mask_str in ip_lines:
        try:
            ipaddress.ip_address(ip_str)
            ipaddress.ip_address(mask_str)
            report(PASS, device, f"Valid IP: {ip_str} {mask_str}")
        except ValueError:
            report(FAIL, device, f"Invalid IP: {ip_str} {mask_str}")


def check_no_duplicate_ips(device: str, content: str):
    """Detect duplicate IP assignments within a config file."""
    ip_addresses = re.findall(r"ip address (\S+) \S+", content)
    seen = set()
    for ip in ip_addresses:
        if ip in seen:
            report(FAIL, device, f"Duplicate IP address: {ip}")
        else:
            seen.add(ip)
    if ip_addresses:
        report(PASS, device, f"No duplicate IPs ({len(ip_addresses)} addresses checked)")


def check_trunk_ports(device: str, content: str):
    """Switches must have trunks allowing VLANs 10,20,30,40,99."""
    if not is_switch(device):
        return
    required = "10,20,30,40,99"
    if f"switchport trunk allowed vlan {required}" in content:
        report(PASS, device, f"Trunk allowed VLANs correct ({required})")
    else:
        report(FAIL, device, f"Trunk VLANs missing or incorrect. Expected: {required}")


def check_dhcp(device: str, content: str):
    """Routers must have DHCP pools for VLANs 10, 20, 30, 40."""
    if not is_router(device):
        return
    for vid in [10, 20, 30, 40]:
        if re.search(rf"ip dhcp pool.*VLAN{vid}", content):
            report(PASS, device, f"DHCP pool for VLAN {vid} present")
        else:
            report(FAIL, device, f"DHCP pool for VLAN {vid} missing")
    if "ip dhcp excluded-address" in content:
        report(PASS, device, "DHCP excluded addresses configured")
    else:
        report(FAIL, device, "DHCP excluded addresses missing")


def check_static_routes(device: str, content: str):
    """Routers must have static routes to remote subnets."""
    if not is_router(device):
        return
    route_count = len(re.findall(r"^ip route ", content, re.MULTILINE))
    if route_count >= 5:
        report(PASS, device, f"Static routes present ({route_count} routes)")
    elif route_count > 0:
        report(WARN, device, f"Only {route_count} static routes; expected at least 5")
    else:
        report(FAIL, device, "No static routes found")


def check_acls(device: str, content: str):
    """Routers must define and apply all three ACLs."""
    if not is_router(device):
        return
    for acl in ["VLAN10-HR", "VLAN30-FINANCE", "MGMT-ACCESS"]:
        if acl in content:
            report(PASS, device, f"ACL '{acl}' defined")
        else:
            report(FAIL, device, f"ACL '{acl}' missing")
    if "ip access-group" in content:
        report(PASS, device, "ACL applied to interface(s) via ip access-group")
    else:
        report(FAIL, device, "No ip access-group found on any interface")


def check_security_basics(device: str, content: str):
    """Check basic security hardening on all devices."""
    checks = {
        "enable secret": "Enable secret password",
        "service password-encryption": "Password encryption",
        "no ip domain-lookup": "Domain lookup disabled",
        "exec-timeout": "Exec timeout configured",
        "banner motd": "MOTD banner",
    }
    for cmd, label in checks.items():
        if cmd in content:
            report(PASS, device, label)
        else:
            report(WARN, device, f"Missing: {label}")


def check_dot1q_encapsulation(device: str, content: str):
    """Router sub-interfaces must all have dot1Q encapsulation."""
    if not is_router(device):
        return
    subifs = re.findall(r"interface GigabitEthernet0/0\.\d+", content)
    encaps = re.findall(r"encapsulation dot1Q \d+", content)
    if len(subifs) > 0 and len(subifs) == len(encaps):
        report(PASS, device, f"dot1Q on all {len(subifs)} sub-interfaces")
    else:
        report(FAIL, device,
               f"dot1Q mismatch: {len(subifs)} sub-interfaces vs {len(encaps)} encapsulations")


def check_mgmt_svi(device: str, content: str):
    """Switches must have VLAN 99 SVI and a default gateway."""
    if not is_switch(device):
        return
    if "interface vlan 99" in content.lower():
        report(PASS, device, "Management SVI (VLAN 99) present")
    else:
        report(FAIL, device, "Management SVI (VLAN 99) missing")
    if "ip default-gateway" in content:
        report(PASS, device, "Default gateway configured")
    else:
        report(FAIL, device, "Default gateway missing")


def check_portfast_bpduguard(device: str, content: str):
    """Access ports should have PortFast and BPDUGuard."""
    if not is_switch(device):
        return
    if "spanning-tree portfast" in content:
        report(PASS, device, "PortFast on access ports")
    else:
        report(WARN, device, "PortFast not found (recommended on access ports)")
    if "spanning-tree bpduguard enable" in content:
        report(PASS, device, "BPDUGuard on access ports")
    else:
        report(WARN, device, "BPDUGuard not found (recommended on access ports)")


def check_wan_interface(device: str, content: str):
    """Router WAN interface must use /30 from 10.10.10.0/30."""
    if not is_router(device):
        return
    wan_ips = re.findall(r"ip address (10\.10\.10\.\d+) 255\.255\.255\.252", content)
    if wan_ips:
        report(PASS, device, f"WAN /30 address configured: {wan_ips[0]}")
    else:
        report(FAIL, device, "WAN /30 address missing (expect 10.10.10.x 255.255.255.252)")


def check_subnet_overlap(device: str, content: str):
    """Detect overlapping DHCP pool networks within a router config."""
    if not is_router(device):
        return
    networks = []
    for match in re.finditer(r"network (\S+) (\S+)", content):
        try:
            net = ipaddress.IPv4Network(f"{match.group(1)}/{match.group(2)}", strict=False)
            networks.append(net)
        except ValueError:
            pass
    for i, n1 in enumerate(networks):
        for n2 in networks[i + 1:]:
            if n1.overlaps(n2):
                report(FAIL, device, f"Subnet overlap: {n1} overlaps {n2}")
                return
    if networks:
        report(PASS, device, f"No subnet overlaps ({len(networks)} networks checked)")


def check_write_memory(device: str, content: str):
    if "write memory" in content:
        report(PASS, device, "write memory present")
    else:
        report(WARN, device, "write memory missing at end of config")


# ─────────────────────────────────────────────
# Main Runner
# ─────────────────────────────────────────────

def validate_file(filepath: str):
    device = os.path.basename(filepath)
    print(f"\n{'='*55}")
    print(f"  Validating: {device}")
    print(f"{'='*55}")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    check_hostnames(device, content)
    check_security_basics(device, content)
    check_vlans(device, content)
    check_ip_addresses(device, content)
    check_no_duplicate_ips(device, content)
    check_wan_interface(device, content)
    check_dot1q_encapsulation(device, content)
    check_trunk_ports(device, content)
    check_dhcp(device, content)
    check_static_routes(device, content)
    check_acls(device, content)
    check_mgmt_svi(device, content)
    check_portfast_bpduguard(device, content)
    check_subnet_overlap(device, content)
    check_write_memory(device, content)


def main():
    print("\nNexaTech Configuration Validator")
    print("=" * 45)

    config_files = sorted(Path(CONFIG_DIR).glob("*.txt"))
    if not config_files:
        print(f"\n[ERROR] No config files found in '{CONFIG_DIR}/'")
        print("Run generate.py first.\n")
        return

    for cfg_file in config_files:
        validate_file(str(cfg_file))

    print(f"\n{'='*55}")
    print(f"  Validation Complete")
    print(f"  Errors  : {errors_found}")
    print(f"  Warnings: {warnings_found}")
    if errors_found == 0:
        print("  Result  : ALL CHECKS PASSED - Configs ready for Packet Tracer")
    else:
        print(f"  Result  : {errors_found} ERROR(S) - review before deployment")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    main()
