def build_switch_config_commands(configuration_data):

    hostname = configuration_data["hostname"]
    vlans = configuration_data["vlans"]

    commands = []

    commands.append(f"hostname {hostname}")

    for vlan in vlans:
        commands.append(f"vlan {vlan['id']}")
        commands.append(f"name {vlan['name']}")

    return commands
