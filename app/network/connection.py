from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException


def test_switch_connection(connection_data):

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

        prompt = connection.find_prompt()

        output = connection.send_command("show version")

        connection.disconnect()

        if output:
            return True, f"Conexão realizada com sucesso. Prompt atual: {prompt}"

        return True, "Conexão realizada com sucesso."

    except NetmikoAuthenticationException:
        return False, "Erro de autenticação. Verifique usuário, senha ou secret enable."

    except NetmikoTimeoutException:
        return False, "Erro de timeout. Verifique IP, porta SSH, conectividade ou se o SSH está habilitado no switch."

    except Exception as error:
        return False, f"Erro inesperado ao conectar no switch: {error}"
#
#
#
def apply_switch_configuration(connection_data, commands):

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