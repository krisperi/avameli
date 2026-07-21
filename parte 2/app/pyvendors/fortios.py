import ipaddress


def cidr_to_ip_netmask(cidr):
    network = ipaddress.ip_network(cidr, strict=False)
    return str(network.network_address), str(network.netmask)


def cidr_to_interface_ip_netmask(cidr):
    interface = ipaddress.ip_interface(cidr)
    return str(interface.ip), str(interface.netmask)


def build_fortigate_config(vpn_name, device, mapped_params, psk):
    phase1 = mapped_params["phase1"]
    phase2 = mapped_params["phase2"]

    local_ip, local_mask = cidr_to_ip_netmask(device["local_subnet"])
    remote_ip, remote_mask = cidr_to_ip_netmask(device["remote_subnet"])
    tunnel_ip, tunnel_mask = cidr_to_interface_ip_netmask(device["tunnel_ip"])

    local_obj = "LAN-LOCAL"
    remote_obj = "LAN-REMOTE"
    phase2_name = f"{vpn_name}-P2"

    phase1_proposal = f"{phase1['encryption']}-{phase1['integrity']}"
    phase2_proposal = f"{phase2['encryption']}-{phase2['integrity']}"

    commands = [

        "config vpn ipsec phase1-interface",
        f"edit \"{vpn_name}\"",
        f"set interface \"{device['wan_interface']}\"",
        f"set ike-version {phase1['ike_version']}",
        "set peertype any",
        f"set remote-gw {device['peer_wan_ip']}",
        f"set proposal {phase1_proposal}",
        f"set dhgrp {phase1['dh_group']}",
        f"set keylife {phase1['lifetime']}",
        "set authmethod psk",
        f"set psksecret \"{psk}\"",
        "set net-device enable",
        "next",
        "end",

        "config vpn ipsec phase2-interface",
        f"edit \"{phase2_name}\"",
        f"set phase1name \"{vpn_name}\"",
        f"set proposal {phase2_proposal}",
        "set pfs enable",
        f"set dhgrp {phase2['pfs_group']}",
        f"set keylifeseconds {phase2['lifetime']}",
        f"set src-subnet {local_ip} {local_mask}",
        f"set dst-subnet {remote_ip} {remote_mask}",
        "next",
        "end",

        "config system interface",
        f"edit \"{vpn_name}\"",
        f"set ip {tunnel_ip} {tunnel_mask}",
        "set allowaccess ping",
        "next",
        "end",

        "config router static",
        "edit 10",
        f"set dst {remote_ip} {remote_mask}",
        f"set device \"{vpn_name}\"",
        "next",
        "end",

        "config firewall address",
        f"edit \"{local_obj}\"",
        f"set subnet {local_ip} {local_mask}",
        "next",
        f"edit \"{remote_obj}\"",
        f"set subnet {remote_ip} {remote_mask}",
        "next",
        "end",

        "config firewall policy",
        "edit 1",
        "set name \"LAN-VPN\"",
        f"set srcintf \"{device['lan_interface']}\"",
        f"set dstintf \"{vpn_name}\"",
        f"set srcaddr \"{local_obj}\"",
        f"set dstaddr \"{remote_obj}\"",
        "set action accept",
        "set schedule always",
        "set service ALL",
        "set nat disable",
        "next",
        "end",

        "config firewall policy",
        "edit 2",
        "set name \"VPN-LAN\"",
        f"set srcintf \"{vpn_name}\"",
        f"set dstintf \"{device['lan_interface']}\"",
        f"set srcaddr \"{remote_obj}\"",
        f"set dstaddr \"{local_obj}\"",
        "set action accept",
        "set schedule always",
        "set service ALL",
        "set nat disable",
        "next",
        "end"
    ]

    return commands


def get_fortigate_validation_commands(device):
    return [
        "diagnose vpn ike gateway list",
        "diagnose vpn tunnel list",
        "get router info routing-table all",
        f"execute ping {device['peer_wan_ip']}",
        f"execute ping {device['remote_tunnel_ip']}"
    ]
