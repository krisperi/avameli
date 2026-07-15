from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException


def save_switch_configuration(connection_data):

    device = {
        "device_type": connection_data["device_type"],
        "host": connection_data["host"],
        "port": connection_data["port"],
        "username": connection_data["username"],
        "password": connection_data["password"],
        "secret": connection_data["secret"],
    }

    try:
        connection = ConnectHandler(**device)

        if connection_data.get("secret"):
            connection.enable()

        output = connection.send_command_timing("write memory")

        connection.disconnect()

        return True, "Configuração salva na NVRAM com sucesso.", output

    except NetmikoAuthenticationException:
        return False, "Erro de autenticação ao salvar configuração.", ""

    except NetmikoTimeoutException:
        return False, "Erro de timeout ao salvar configuração.", ""

    except Exception as error:
        return False, f"Erro inesperado ao salvar configuração: {error}", ""