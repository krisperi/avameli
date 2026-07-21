def build_paloalto_config(vpn_name, device, mapped_params, psk):
    phase1 = mapped_params["phase1"]
    phase2 = mapped_params["phase2"]

    ike_profile = f"IKE-PROFILE-{vpn_name}"
    ipsec_profile = f"IPSEC-PROFILE-{vpn_name}"
    ike_gateway = f"IKE-GW-{vpn_name}"
    proxy_id = f"{vpn_name}-P2"
    route_name = f"ROUTE-{vpn_name}"

    local_obj = "LAN-LOCAL"
    remote_obj = "LAN-REMOTE"

    commands = [
        f"set address {local_obj} ip-netmask {device['local_subnet']}",
        f"set address {remote_obj} ip-netmask {device['remote_subnet']}",

        f"set network ike crypto-profiles ike-crypto-profiles {ike_profile} encryption {phase1['encryption']}",
        f"set network ike crypto-profiles ike-crypto-profiles {ike_profile} hash {phase1['integrity']}",
        f"set network ike crypto-profiles ike-crypto-profiles {ike_profile} dh-group {phase1['dh_group']}",
        f"set network ike crypto-profiles ike-crypto-profiles {ike_profile} lifetime seconds {phase1['lifetime']}",

        f"set network ike crypto-profiles ipsec-crypto-profiles {ipsec_profile} esp encryption {phase2['encryption']}",
        f"set network ike crypto-profiles ipsec-crypto-profiles {ipsec_profile} esp authentication {phase2['integrity']}",
        f"set network ike crypto-profiles ipsec-crypto-profiles {ipsec_profile} dh-group {phase2['pfs_group']}",
        f"set network ike crypto-profiles ipsec-crypto-profiles {ipsec_profile} lifetime seconds {phase2['lifetime']}",

        f"set network interface tunnel units {device['tunnel_interface']} ip {device['tunnel_ip']}",
        f"set network virtual-router {device['virtual_router']} interface {device['tunnel_interface']}",
        f"set zone {device['vpn_zone']} network layer3 {device['tunnel_interface']}",

        f"set network ike gateway {ike_gateway} authentication pre-shared-key key {psk}",
        f"set network ike gateway {ike_gateway} protocol ikev2 ike-crypto-profile {ike_profile}",
        f"set network ike gateway {ike_gateway} protocol-common local-address interface {device['wan_interface']}",
        f"set network ike gateway {ike_gateway} protocol-common local-address ip {device['wan_ip']}",
        f"set network ike gateway {ike_gateway} protocol-common peer-address ip {device['peer_wan_ip']}",

        f"set network tunnel ipsec {vpn_name} tunnel-interface {device['tunnel_interface']}",
        f"set network tunnel ipsec {vpn_name} auto-key ike-gateway {ike_gateway}",
        f"set network tunnel ipsec {vpn_name} auto-key ipsec-crypto-profile {ipsec_profile}",

        f"set network tunnel ipsec {vpn_name} auto-key proxy-id {proxy_id} protocol any",
        f"set network tunnel ipsec {vpn_name} auto-key proxy-id {proxy_id} local {device['local_subnet']}",
        f"set network tunnel ipsec {vpn_name} auto-key proxy-id {proxy_id} remote {device['remote_subnet']}",

        f"set network virtual-router {device['virtual_router']} routing-table ip static-route {route_name} destination {device['remote_subnet']}",
        f"set network virtual-router {device['virtual_router']} routing-table ip static-route {route_name} interface {device['tunnel_interface']}",
        f"set network virtual-router {device['virtual_router']} routing-table ip static-route {route_name} nexthop ip-address {device['remote_tunnel_ip']}",

        f"set rulebase security rules LAN-VPN from {device['local_zone']}",
        f"set rulebase security rules LAN-VPN to {device['vpn_zone']}",
        f"set rulebase security rules LAN-VPN source {local_obj}",
        f"set rulebase security rules LAN-VPN destination {remote_obj}",
        "set rulebase security rules LAN-VPN application any",
        "set rulebase security rules LAN-VPN service any",
        "set rulebase security rules LAN-VPN action allow",

        f"set rulebase security rules VPN-LAN from {device['vpn_zone']}",
        f"set rulebase security rules VPN-LAN to {device['local_zone']}",
        f"set rulebase security rules VPN-LAN source {remote_obj}",
        f"set rulebase security rules VPN-LAN destination {local_obj}",
        "set rulebase security rules VPN-LAN application any",
        "set rulebase security rules VPN-LAN service any",
        "set rulebase security rules VPN-LAN action allow"
    ]

    return commands


def get_paloalto_validation_commands(device):
    return [
        "show vpn ike-sa",
        "show vpn ipsec-sa",
        f"show interface {device['tunnel_interface']}",
        "show routing route",
        f"ping source {device['tunnel_ip'].split('/')[0]} host {device['remote_tunnel_ip']}"
    ]
