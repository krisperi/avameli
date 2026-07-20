from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException


def mask_sensitive_commands(commands):
    masked = []

    for command in commands:
        if "pre-shared-key key" in command:
            masked.append(command.split("pre-shared-key key")[0] + "pre-shared-key key ********")
        elif "set psksecret" in command:
            masked.append("set psksecret ********")
        else:
            masked.append(command)

    return masked


def connect_device(device, username, password):
    return ConnectHandler(
        device_type=device["netmiko_device_type"],
        host=device["management_ip"],
        username=username,
        password=password
    )


def apply_commands(device, commands, username, password):
    try:
        print(f"\n[INFO] Conectando em {device['name']} - {device['management_ip']}")

        connection = connect_device(device, username, password)

        print("[OK] Conectado com sucesso.")
        print("[INFO] Aplicando configuração...")

        if device["vendor"] == "fortigate":
            output = ""
            for command in commands:
                output += connection.send_command_timing(command) + "\n"

        else:
            output = connection.send_config_set(commands)
            print("[INFO] Executando commit no Palo Alto...")
            output += "\n" + connection.send_command_timing("commit", read_timeout=180)

        print(output)

        connection.disconnect()

        print(f"[OK] Configuração finalizada em {device['name']}")
        return True

    except NetmikoAuthenticationException:
        print(f"[ERROR] Falha de autenticação em {device['name']}")
        return False

    except NetmikoTimeoutException:
        print(f"[ERROR] Timeout ao conectar em {device['name']}")
        return False

    except Exception as error:
        print(f"[ERROR] Erro inesperado em {device['name']}: {error}")
        return False


def run_validation_commands(device, commands, username, password):
    try:
        print(f"\n[INFO] Conectando em {device['name']} para validação...")

        connection = connect_device(device, username, password)

        for command in commands:
            print(f"\n=== {device['name']} | {command} ===")
            output = connection.send_command_timing(command, read_timeout=60)
            print(output)

        connection.disconnect()

    except Exception as error:
        print(f"[ERROR] Falha na validação de {device['name']}: {error}")
