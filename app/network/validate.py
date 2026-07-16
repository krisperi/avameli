from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException


def _parse_hostname(running_config_output):


    for line in running_config_output.splitlines():
        line = line.strip()

        if line.startswith("hostname "):
            return line.split("hostname ", 1)[1].strip()

    return None


def _parse_vlans(vlan_brief_output):

    vlans = {}

    for line in vlan_brief_output.splitlines():
        line = line.strip()

        if not line:
            continue

        parts = line.split()

        if len(parts) < 2:
            continue

        vlan_id = parts[0]

        if vlan_id.isdigit():
            vlans[int(vlan_id)] = parts[1]

    return vlans


def validate_switch_configuration(connection_data, configuration_data):

    device = {
        "device_type": connection_data["device_type"],
        "host": connection_data["host"],
        "port": connection_data["port"],
        "username": connection_data["username"],
        "password": connection_data["password"],
        "secret": connection_data["secret"],
    }

    validation_results = []

    try:
        connection = ConnectHandler(**device)

        if connection_data.get("secret"):
            connection.enable()

        running_config = connection.send_command("show running-config")
        vlan_brief = connection.send_command("show vlan brief")

        connection.disconnect()

        expected_hostname = configuration_data["hostname"]
        expected_vlans = configuration_data["vlans"]

        current_hostname = _parse_hostname(running_config)
        current_vlans = _parse_vlans(vlan_brief)

        has_divergence = False

        # Validação do hostname
        if current_hostname == expected_hostname:
            validation_results.append(
                f"OK - Hostname correto: {expected_hostname}"
            )
        else:
            has_divergence = True
            validation_results.append(
                "ALERTA - Hostname divergente."
            )
            validation_results.append(
                f"  Esperado: {expected_hostname}"
            )
            validation_results.append(
                f"  Encontrado: {current_hostname}"
            )

        # Validação das VLANs
        for vlan in expected_vlans:
            expected_vlan_id = vlan["id"]
            expected_vlan_name = vlan["name"]

            current_vlan_name = current_vlans.get(expected_vlan_id)

            if current_vlan_name is None:
                has_divergence = True
                validation_results.append(
                    f"ALERTA - VLAN {expected_vlan_id} não encontrada."
                )
                validation_results.append(
                    f"  Esperado: VLAN {expected_vlan_id} - {expected_vlan_name}"
                )
                continue

            if current_vlan_name == expected_vlan_name:
                validation_results.append(
                    f"OK - VLAN {expected_vlan_id} correta: {expected_vlan_name}"
                )
            else:
                has_divergence = True
                validation_results.append(
                    f"ALERTA - VLAN {expected_vlan_id} com nome divergente."
                )
                validation_results.append(
                    f"  Esperado: {expected_vlan_name}"
                )
                validation_results.append(
                    f"  Encontrado: {current_vlan_name}"
                )

        if has_divergence:
            return False, "Validação concluída com divergências.", validation_results

        return True, "Validação concluída com sucesso.", validation_results

    except NetmikoAuthenticationException:
        return False, "Erro de autenticação durante a validação.", []

    except NetmikoTimeoutException:
        return False, "Erro de timeout durante a validação.", []

    except Exception as error:
        return False, f"Erro inesperado durante a validação: {error}", []