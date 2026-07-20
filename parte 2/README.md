## **As informações da parte 2 estão em docs/automation-plan.md**

Passo a passo do lab 

Configurando interface no ubuntu 16.04
Download do git
Download do python3
git pull para ter acesso aos códigos.
Configuração da interface ens4 na rede de mgmt (10.32.160.10/24)


PALO ALTO
Primeiro, tive que configurar o SSH no Palo Alto

delete deviceconfig system type dhcp-client
set deviceconfig system type static
commit

set deviceconfig system ip-address 10.32.160.2
set deviceconfig system netmask 255.255.255.0 
set deviceconfig system default-gateway 10.32.160.10 
set deviceconfig system dns-setting servers primary 8.8.8.8
commit

set mgt-config users risperi password
<inserir a senha 2 vezes>


FORTIGATE
Primeiro, remover o modo dhcp da interface escolhida e permitir ssh e ping

config system interface
edit port1
set mode static
set ip 10.32.160.1 255.255.255.0
set allowaccess ping https ssh

Depois configurar o mesmo usuário do Palo Alto para facilitar o acesso ao LAB, em ambiente produtivo haveria outra forma de autenticação por parte das automações

config system admin
edit admin
set password X
end