from getpass import getpass

from loader import load_json_config
from vendors import is_supported_vendor, get_supported_vendors_message
from parametros import map_parameters
from conn import apply_commands, mask_sensitive_commands, run_validation_commands
from vendors.paloalto import build_palo_alto_config, get_palo_alto_validation_commands
from vendors.fortios import build_fortigate_config, get_fortigate_validation_commands


DEFAULT_CONFIG_PATH = "vpn.json"


def validate_config(config):
    required_top_fields = ["vpn_name", "phase1", "phase2", "devices"]

    for field in required_top_fields:
        if field not in config:
            return False, f"Campo obrigatório ausente: {field}"

    if not isinstance(config["devices"], list) or len(config["devices"]) < 2:
        return False, "O JSON deve conter pelo menos dois dispositivos."

    for device in config["devices"]:
        required_device_fields = [
            "name",
            "vendor",
            "netmiko_device_type",
            "management_ip",
            "wan_ip",
            "peer_wan_ip",
            "local_subnet",
            "remote_subnet"
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


def load_and_validate():
    config_path = input(f"Informe o caminho do JSON [{DEFAULT_CONFIG_PATH}]: ").strip()

    if not config_path:
        config_path = DEFAULT_CONFIG_PATH

    try:
        config = load_json_config(config_path)

    except Exception as error:
        print(f"[ERROR] {error}")
        return None

    is_valid, message = validate_config(config)

    if not is_valid:
        print(f"[ERROR] {message}")
        print("[ACTION] Valide as informações do arquivo JSON e tente novamente.")
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


def configure_vpn():
    print("\n=== Configurar VPN IPSec ===")

    config = load_and_validate()

    if not config:
        return

    username, password = get_credentials()

    if not username:
        return

    psk = getpass("Pre-shared Key da VPN: ")

    if not psk:
        print("[ERROR] PSK não informada.")
        return

    vpn_name = config["vpn_name"]
    phase1 = config["phase1"]
    phase2 = config["phase2"]

    all_device_commands = []

    for device in config["devices"]:
        vendor = device["vendor"]

        print(f"\n[INFO] Mapeando parâmetros para {device['name']} ({vendor})...")
        mapped_params = map_parameters(vendor, phase1, phase2)

        print(f"[INFO] Gerando configuração para {device['name']}...")

        if vendor == "palo_alto":
            commands = build_palo_alto_config(vpn_name, device, mapped_params, psk)

        elif vendor == "fortigate":
            commands = build_fortigate_config(vpn_name, device, mapped_params, psk)

        else:
            print(f"[ERROR] Vendor inválido: {vendor}")
            print(f"[INFO] Vendors suportados: {get_supported_vendors_message()}")
            return

        all_device_commands.append((device, commands))

        print(f"\n=== Comandos para {device['name']} ===")
        for command in mask_sensitive_commands(commands):
            print(command)

    confirm = input("\nDeseja aplicar a configuração nos dois firewalls? [y/N]: ").strip().lower()

    if confirm != "y":
        print("[INFO] Operação cancelada pelo usuário.")
        return

    for device, commands in all_device_commands:
        success = apply_commands(device, commands, username, password)

        if not success:
            print(f"[ERROR] Falha ao aplicar configuração em {device['name']}")
            return

    print("\n[OK] Fluxo de configuração finalizado.")


def validate_vpn():
    print("\n=== Validar VPN IPSec ===")

    config = load_and_validate()

    if not config:
        return

    username, password = get_credentials()

    if not username:
        return

    for device in config["devices"]:
        vendor = device["vendor"]

        if vendor == "palo_alto":
            commands = get_palo_alto_validation_commands(device)

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
