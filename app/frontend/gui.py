import tkinter as tk
from tkinter import ttk, messagebox
from network.connection import test_switch_connection, apply_switch_configuration
from network.config_builder import build_switch_config_commands
from network.wr import save_switch_configuration


class CiscoAutomationGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Automação de Switch Cisco")
        self.root.geometry("850x700")
        self.root.resizable(False, False)

        self._create_variables()
        self._create_widgets()

    def _create_variables(self):
        # Variáveis de conexão
        self.switch_host = tk.StringVar()
        self.switch_port = tk.StringVar(value="22")
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.secret = tk.StringVar()
        self.device_type = tk.StringVar(value="cisco_ios")

        # Variáveis de configuração
        self.hostname = tk.StringVar(value="SWITCH_AUTOMATIZADO")

        # Variáveis das VLANs
        self.vlan_1_id = tk.StringVar(value="10")
        self.vlan_1_name = tk.StringVar(value="VLAN_DADOS")

        self.vlan_2_id = tk.StringVar(value="20")
        self.vlan_2_name = tk.StringVar(value="VLAN_VOZ")

        self.vlan_3_id = tk.StringVar(value="50")
        self.vlan_3_name = tk.StringVar(value="VLAN_SEGURANCA")

    def _create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill="both", expand=True)

        title_label = ttk.Label(
            main_frame,
            text="Automação de Switch Cisco",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 15))

        self._create_connection_frame(main_frame)
        self._create_configuration_frame(main_frame)
        self._create_buttons_frame(main_frame)
        self._create_logs_frame(main_frame)

    def _create_connection_frame(self, parent):
        connection_frame = ttk.LabelFrame(
            parent,
            text="Conexão com o Switch",
            padding=10
        )
        connection_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(connection_frame, text="Switch Host/IP:").grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )
        ttk.Entry(
            connection_frame,
            textvariable=self.switch_host,
            width=35
        ).grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Label(connection_frame, text="Porta SSH:").grid(
            row=0,
            column=2,
            sticky="w",
            padx=5,
            pady=5
        )
        ttk.Entry(
            connection_frame,
            textvariable=self.switch_port,
            width=15
        ).grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        ttk.Label(connection_frame, text="Usuário:").grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )
        ttk.Entry(
            connection_frame,
            textvariable=self.username,
            width=35
        ).grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Label(connection_frame, text="Senha:").grid(
            row=1,
            column=2,
            sticky="w",
            padx=5,
            pady=5
        )
        ttk.Entry(
            connection_frame,
            textvariable=self.password,
            show="*",
            width=15
        ).grid(
            row=1,
            column=3,
            padx=5,
            pady=5
        )

        ttk.Label(connection_frame, text="Enable Secret:").grid(
            row=2,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )
        ttk.Entry(
            connection_frame,
            textvariable=self.secret,
            show="*",
            width=35
        ).grid(
            row=2,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Label(connection_frame, text="Device Type:").grid(
            row=2,
            column=2,
            sticky="w",
            padx=5,
            pady=5
        )
        ttk.Entry(
            connection_frame,
            textvariable=self.device_type,
            width=15
        ).grid(
            row=2,
            column=3,
            padx=5,
            pady=5
        )

    def _create_configuration_frame(self, parent):
        config_frame = ttk.LabelFrame(
            parent,
            text="Configuração Desejada",
            padding=10
        )
        config_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(config_frame, text="Hostname:").grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )
        ttk.Entry(
            config_frame,
            textvariable=self.hostname,
            width=35
        ).grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky="w"
        )

        ttk.Label(
            config_frame,
            text="VLAN ID",
            font=("Arial", 10, "bold")
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=(15, 5)
        )

        ttk.Label(
            config_frame,
            text="VLAN Name",
            font=("Arial", 10, "bold")
        ).grid(
            row=1,
            column=1,
            sticky="w",
            padx=5,
            pady=(15, 5)
        )

        ttk.Entry(
            config_frame,
            textvariable=self.vlan_1_id,
            width=15
        ).grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )
        ttk.Entry(
            config_frame,
            textvariable=self.vlan_1_name,
            width=35
        ).grid(
            row=2,
            column=1,
            padx=5,
            pady=5,
            sticky="w"
        )

        ttk.Entry(
            config_frame,
            textvariable=self.vlan_2_id,
            width=15
        ).grid(
            row=3,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )
        ttk.Entry(
            config_frame,
            textvariable=self.vlan_2_name,
            width=35
        ).grid(
            row=3,
            column=1,
            padx=5,
            pady=5,
            sticky="w"
        )

        ttk.Entry(
            config_frame,
            textvariable=self.vlan_3_id,
            width=15
        ).grid(
            row=4,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )
        ttk.Entry(
            config_frame,
            textvariable=self.vlan_3_name,
            width=35
        ).grid(
            row=4,
            column=1,
            padx=5,
            pady=5,
            sticky="w"
        )

    def _create_buttons_frame(self, parent):
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill="x", pady=(0, 10))

        test_button = ttk.Button(
            buttons_frame,
            text="Testar Conexão",
            command=self.test_connection
        )
        test_button.pack(side="left", padx=5)

        execute_button = ttk.Button(
            buttons_frame,
            text="Executar Automação",
            command=self.execute_automation
        )
        execute_button.pack(side="left", padx=5)

        clear_button = ttk.Button(
            buttons_frame,
            text="Limpar Logs",
            command=self.clear_logs
        )
        clear_button.pack(side="left", padx=5)

    def _create_logs_frame(self, parent):
        logs_frame = ttk.LabelFrame(
            parent,
            text="Logs / Resultado",
            padding=10
        )
        logs_frame.pack(fill="both", expand=True)

        self.logs_text = tk.Text(
            logs_frame,
            height=15,
            width=95
        )
        self.logs_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            logs_frame,
            command=self.logs_text.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.logs_text.configure(yscrollcommand=scrollbar.set)

        self._write_log("Aguardando execução...")

    def _write_log(self, message):
        self.logs_text.insert(tk.END, f"{message}\n")
        self.logs_text.see(tk.END)

    def clear_logs(self):
        self.logs_text.delete("1.0", tk.END)
        self._write_log("Logs limpos.")

    def _validate_required_fields(self):
        required_fields = {
            "Switch Host/IP": self.switch_host.get().strip(),
            "Porta SSH": self.switch_port.get().strip(),
            "Usuário": self.username.get().strip(),
            "Senha": self.password.get().strip(),
            "Device Type": self.device_type.get().strip(),
            "Hostname": self.hostname.get().strip(),
            "VLAN 1 ID": self.vlan_1_id.get().strip(),
            "VLAN 1 Name": self.vlan_1_name.get().strip(),
            "VLAN 2 ID": self.vlan_2_id.get().strip(),
            "VLAN 2 Name": self.vlan_2_name.get().strip(),
            "VLAN 3 ID": self.vlan_3_id.get().strip(),
            "VLAN 3 Name": self.vlan_3_name.get().strip(),
        }

        for field_name, field_value in required_fields.items():
            if not field_value:
                return False, f"O campo '{field_name}' é obrigatório."

        if not self.switch_port.get().strip().isdigit():
            return False, "O campo 'Porta SSH' deve conter apenas números."

        vlan_ids = [
            self.vlan_1_id.get().strip(),
            self.vlan_2_id.get().strip(),
            self.vlan_3_id.get().strip(),
        ]

        for vlan_id in vlan_ids:
            if not vlan_id.isdigit():
                return False, f"O VLAN ID '{vlan_id}' deve conter apenas números."

            vlan_id_number = int(vlan_id)

            if vlan_id_number < 1 or vlan_id_number > 4094:
                return False, f"O VLAN ID '{vlan_id}' deve estar entre 1 e 4094."

        if len(vlan_ids) != len(set(vlan_ids)):
            return False, "Os VLAN IDs não podem ser repetidos."

        return True, "Campos validados com sucesso."

    def _get_form_data(self):
        return {
            "connection": {
                "host": self.switch_host.get().strip(),
                "port": int(self.switch_port.get().strip()),
                "username": self.username.get().strip(),
                "password": self.password.get().strip(),
                "secret": self.secret.get().strip(),
                "device_type": self.device_type.get().strip(),
            },
            "configuration": {
                "hostname": self.hostname.get().strip(),
                "vlans": [
                    {
                        "id": int(self.vlan_1_id.get().strip()),
                        "name": self.vlan_1_name.get().strip()
                    },
                    {
                        "id": int(self.vlan_2_id.get().strip()),
                        "name": self.vlan_2_name.get().strip()
                    },
                    {
                        "id": int(self.vlan_3_id.get().strip()),
                        "name": self.vlan_3_name.get().strip()
                    },
                ]
            }
        }

    def test_connection(self):
        is_valid, message = self._validate_required_fields()

        if not is_valid:
            messagebox.showerror("Erro de validação", message)
            self._write_log(f"Erro: {message}")
            return

        form_data = self._get_form_data()
        connection = form_data["connection"]

        self._write_log("Iniciando teste de conexão com o switch...")
        self._write_log(f"Switch: {connection['host']}")
        self._write_log(f"Porta SSH: {connection['port']}")
        self._write_log(f"Usuário: {connection['username']}")
        self._write_log(f"Device Type: {connection['device_type']}")

        status, result_message = test_switch_connection(connection)

        if status:
            self._write_log(result_message)
            messagebox.showinfo("Teste de Conexão", result_message)
        else:
            self._write_log(f"Falha na conexão: {result_message}")
            messagebox.showerror("Teste de Conexão", result_message)

#
    def execute_automation(self):
        is_valid, message = self._validate_required_fields()

        if not is_valid:
            messagebox.showerror("Erro de validação", message)
            self._write_log(f"Erro: {message}")
        return

        form_data = self._get_form_data()
        connection = form_data["connection"]
        config = form_data["configuration"]

        self._write_log("Iniciando fluxo de automação.")
        self._write_log("Gerando comandos de configuração...")

        commands = build_switch_config_commands(config)

        self._write_log("Comandos que serão aplicados:")

        for command in commands:
            self._write_log(f"  {command}")

        self._write_log("")
        self._write_log("Conectando ao switch para aplicar configuração...")

        status, result_message, output = apply_switch_configuration(connection, commands)

        if not status:
            self._write_log(f"Falha ao aplicar configuração: {result_message}")
            messagebox.showerror("Erro na Automação", result_message)
        return

        self._write_log(result_message)

        if output:
            self._write_log("Retorno do switch:")
            self._write_log(output)

        self._write_log("")
        self._write_log("Salvando configuração na NVRAM...")

        save_status, save_message, save_output = save_switch_configuration(connection)

        if not save_status:
            self._write_log(f"Falha ao salvar configuração: {save_message}")
            messagebox.showerror("Erro ao Salvar", save_message)
            return

        self._write_log(save_message)

        if save_output:
            self._write_log("Retorno do comando de salvamento:")
            self._write_log(save_output)

        self._write_log("")
        self._write_log("Automação concluída com sucesso.")

        messagebox.showinfo(
            "Automação Concluída",
            "Hostname e VLANs configurados com sucesso. Configuração salva na NVRAM."
    )

    def run(self):
        self.root.mainloop()