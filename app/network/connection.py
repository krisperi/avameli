from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

def apply_switch_configuration(connection_data, commands):
    """
    Aplica comandos de configuração no switch Cisco.

    Args:
        connection_data (dict): Dados de conexão com o switch.
        commands (list): Lista de comandos de configuração.

    Returns:
        tuple: (status, message, output)
    """

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

        output = connection.send_config_set(commands)

        connection.disconnect()

        return True, "Configuração aplicada com sucesso.", output

    except NetmikoAuthenticationException:
        return False, "Erro de autenticação. Verifique usuário, senha ou secret enable.", ""

    except NetmikoTimeoutException:
        return False, "Erro de timeout. Verifique IP, porta SSH ou conectividade.", ""

    except Exception as error:
        return False, f"Erro inesperado ao aplicar configuração: {error}", ""