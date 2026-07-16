import os
from datetime import datetime

from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException


def _sanitize_filename(value):
    """
    Remove ou substitui caracteres inválidos para nomes de arquivo.
    """

    invalid_chars = ["<", ">", ":", '"', "/", "\\", "|", "?", "*", " "]

    sanitized_value = value

    for char in invalid_chars:
        sanitized_value = sanitized_value.replace(char, "_")

    return sanitized_value


def backup_running_config(connection_data, hostname, backup_dir="backups"):

    device = {
        "device_type": connection_data["device_type"],
        "host": connection_data["host"],
        "port": connection_data["port"],
        "username": connection_data["username"],
        "password": connection_data["password"],
        "secret": connection_data["secret"],
    }

    try:
        os.makedirs(backup_dir, exist_ok=True)

        connection = ConnectHandler(**device)

        if connection_data.get("secret"):
            connection.enable()

        running_config = connection.send_command("show running-config")

        connection.disconnect()

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_hostname = _sanitize_filename(hostname)

        file_name = f"{safe_hostname}_{timestamp}.cfg"
        file_path = os.path.join(backup_dir, file_name)

        with open(file_path, "w", encoding="utf-8") as backup_file:
            backup_file.write(running_config)

        return True, "Backup da configuração realizado com sucesso.", file_path

    except NetmikoAuthenticationException:
        return False, "Erro de autenticação ao realizar backup.", ""

    except NetmikoTimeoutException:
        return False, "Erro de timeout ao realizar backup.", ""

    except Exception as error:
        return False, f"Erro inesperado ao realizar backup: {error}", ""
