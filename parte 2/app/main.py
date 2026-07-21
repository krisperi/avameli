from getpass import getpass

from loader import load_json_config
from vendors import is_supported_vendor, get_supported_vendors_message
from parametros import map_parameters
from conn import apply_commands, mask_sensitive_commands, run_validation_commands

from pyvendors.paloalto import build_paloalto_config, get_paloalto_validation_commands
from pyvendors.fortios import build_fortigate_config, get_fortigate_validation_commands


DEFAULT_CONFIG_PATH = "vpn.json"


def validate_config(config):
    required_top_fields = ["vpn_name", "vpn_type", "psk", "phase1", "phase2", "devices"]

    for field in required_top_fields:
        if field not in config:
            return False, f"Campo obrigatório ausente: {field}"

    if config["vpn_type"] != "route_based":
        return False, "Este script suporta apenas vpn_type = route_based."

    if not isinstance(config["devices"], list) or len(config["devices"]) < 1:
        return False, "O campo devices deve conter pelo menos um dispositivo."

    for device in config["devices"]:
        required_device_fields = [
            "name",
            "vendor",
            "netmiko_device_type",
            "management_ip",
            "wan_ip",
            "peer_wan_ip",
            "local_subnet",
            "remote_subnet",
            "tunnel_ip",
            "remote_tunnel_ip"
        ]

        for field in required_device_fields:
            if field not in device:
                return False, f"Campo obrigatório ausente no device {device.get('name', 'unknown')}: {field}"

        if not is_supported_vendor(device["vendor"]):
            return False, (
                f"Vendor inválido: {device['vendor']}. "
                f"Vendors suportados: {get_supported_vendors_message()}"
            )

    return True, "Arquivo validado com sucesso."


def load_and_validate_config():
    config_path = input(f"Informe o caminho do JSON [{DEFAULT_CONFIG_PATH}]: ").strip()

    if not config_path:
        config_path = DEFAULT_CONFIG_PATH

    try:
        config = load_json_config(config_path)
    except Exception as error:
        print(f"[ERROR] Erro ao carregar arquivo: {error}")
        return None

    is_valid, message = validate_config(config)

    if not is_valid:
        print(f"[ERROR] {message}")
        print("[ACTION] Valide as informações do JSON e tente novamente.")
        return None

    print(f"[OK] {message}")
    return config


def get_credentials():
    print("\n=== Credenciais SSH ===")
    username = input("Usuário SSH: ").strip()
    password = getpass("Senha SSH: ")

    if not username or not password:
        print("[ERROR] Usuário ou senha não informado.")
        return None, None

    return username, password


def build_commands_for_device(config, device):
    vendor = device["vendor"]
    vpn_name = config["vpn_name"]
    psk = config["psk"]

    mapped_params = map_parameters(vendor, config["phase1"], config["phase2"])

    if vendor == "palo_alto":
        return build_paloalto_config(vpn_name, device, mapped_params, psk)

    if vendor == "fortigate":
        return build_fortigate_config(vpn_name, device, mapped_params, psk)

    raise ValueError(f"Vendor não suportado: {vendor}")


def configure_vpn():
    print("\n=== Configurar VPN IPSec Route-Based ===")

    config = load_and_validate_config()

    if not config:
        return

    username, password = get_credentials()

    if not username:
        return

    device_command_list = []

    for device in config["devices"]:
        print(f"\n[INFO] Gerando configuração para {device['name']} ({device['vendor']})...")

        try:
            commands = build_commands_for_device(config, device)
        except Exception as error:
            print(f"[ERROR] Falha ao gerar configuração para {device['name']}: {error}")
            return

        device_command_list.append((device, commands))

        print(f"\n=== Comandos para {device['name']} ===")
        for command in mask_sensitive_commands(commands):
            print(command)

    confirm = input("\nDeseja aplicar a configuração nos dispositivos informados? [y/N]: ").strip().lower()

    if confirm != "y":
        print("[INFO] Operação cancelada pelo usuário.")
        return

    for device, commands in device_command_list:
        success = apply_commands(device, commands, username, password)

        if not success:
            print(f"[ERROR] Falha ao aplicar configuração em {device['name']}.")
            return

    print("\n[OK] Fluxo de configuração finalizado.")


def validate_vpn():
    print("\n=== Validar VPN IPSec ===")

    config = load_and_validate_config()

    if not config:
        return

    username, password = get_credentials()

    if not username:
        return

    for device in config["devices"]:
        vendor = device["vendor"]

        if vendor == "palo_alto":
            commands = get_paloalto_validation_commands(device)
        elif vendor == "fortigate":
            commands = get_fortigate_validation_commands(device)
        else:
            print(f"[ERROR] Vendor inválido: {vendor}")
            continue

        run_validation_commands(device, commands, username, password)


def show_menu():
    while True:
        print("\n==============================")
        print(" VPN IPSec Automation CLI")
        print("==============================")
        print("1. Configurar VPN")
        print("2. Validar VPN")
        print("0. Sair")

        option = input("Selecione uma opção: ").strip()

        if option == "1":
            configure_vpn()
        elif option == "2":
            validate_vpn()
        elif option == "0":
            print("Encerrando aplicação.")
            break
        else:
            print("[ERROR] Opção inválida. Selecione 1, 2 ou 0.")


if __name__ == "__main__":
    show_menu()