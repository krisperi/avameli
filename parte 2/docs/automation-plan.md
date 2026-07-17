# Plano de Automação de VPN IPSec entre FortiGate e Palo Alto

## Resumo

Seguindo para a parte 2 do desafio - esse documento descreve um plano para automatizar a configuração de uma VPN IPSec site-to-site entre os firewalls FortiGate e Palo Alto.

O objetivo é definir os parâmetros necessários, ferramentas, passos lógicos da automação, considerações específicas de ambiente multi-vendor e estratégias de validação e alertas.

A automação proposta considera o uso de Python com entrada de dados em JSON e módulos específicos para cada fabricante, permitindo que a mesma estrutura de dados gere configurações compatíveis com FortiGate e Palo Alto.

## 




## Cenário proposto

O cenário proposto contempla uma VPN IPSec site-to-site entre dois sites:

![High Level Design](hld-topology.png)



### Informações gerais
| **Item** | **Site A** | **Site B** |
|---|---|---|
| **Fabricante** | Palo Alto | Fortinet |
| **Função** | Firewall | Firewall |
| **Tipo de VPN** | IPSec Site-to-site | IPSec Site-to-site |
| **Autenticação** | Pre-shared key | Pre-shared key |
| **IKE Version** | IKEv2 | IKEv2 |


### Endereçamento

| Endereço | Palo Alto | Fortigate |
|---|---:|---:|
| IP WAN | `203.0.113.10` | `198.51.100.20` |
| IP de gerenciamento | `10.32.160.1` | `10.32.160.2` |
| Rede local | `10.1.1.0/24` | `10.2.1.0/24` |
| Interface WAN | `TBD` | `TBD` |
| Interface LAN/Trust | `TBD` | `TBD` |
| Nome do túnel | `IPSEC-TU1` | `IPSEC-TU1` |


```
- Por se tratar de um ambiente de laboratório virtual não-produtivo, os IPs de WAN escolhidos são correspondentes a faixa TEST-NET da IANA usada para fins de documentação.

- Os ranges de gerência e rede local são fictícios para teste do laboratório

- Nome lógico do túnel IPSec foi o mesmo utilizado em ambos os firewalls para facilitar identificação operacional e troubleshooting.
```

### Parametros da VPN

### Phase 1 - IKE

| Parâmetro | Valor |
|---|---|
| IKE Version | IKEv2 |
| Autenticação | Pre-shared Key |
| Criptografia | AES-256 |
| Integridade | SHA-256 |
| Diffie-Hellman Group | Group 19 |
| Lifetime | 28800 segundos |

### Phase 2 - IPSec

| Parâmetro | Valor |
|---|---|
| Criptografia | AES-256 |
| Integridade | SHA-256 |
| PFS | Habilitado |
| PFS Group | Group 19 |
| Lifetime | 3600 segundos |
| Tráfego protegido | `10.1.1.0/24` <> `10.2.1.0/24` |


### Rede de túnel


