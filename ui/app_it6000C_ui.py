import tkinter as tk
from tkinter import ttk, messagebox
from controller.IT6000C_controller import IT6000CController  # Asegúrate de que la clase esté definida.

class IT6000CApp:
    def __init__(self, main_panel):
        self.controller = None
        self.main_panel = main_panel
        self.create_widgets()

    def create_widgets(self):
        """Construye la UI dentro del main_panel."""

        # Frame de Conexión
        connection_frame = ttk.LabelFrame(self.main_panel, text="Conexión")
        connection_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(connection_frame, text="IP del Emulador:").grid(row=0, column=0, padx=5, pady=5)
        self.ip_entry = ttk.Entry(connection_frame)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)

        connect_button = ttk.Button(connection_frame, text="Conectar", command=self.connect)
        connect_button.grid(row=0, column=2, padx=5, pady=5)

        disconnect_button = ttk.Button(connection_frame, text="Desconectar", command=self.disconnect)
        disconnect_button.grid(row=0, column=3, padx=5, pady=5)

        # Frame de Configuración
        config_frame = ttk.LabelFrame(self.main_panel, text="Configuración de Salida")
        config_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(config_frame, text="Modo de Operación:").grid(row=0, column=0, padx=5, pady=5)
        self.mode_var = tk.StringVar(value="CV")
        ttk.Combobox(config_frame, textvariable=self.mode_var, values=["CV", "CC", "CP"]).grid(row=0, column=1)

        ttk.Label(config_frame, text="Voltaje (V):").grid(row=1, column=0, padx=5, pady=5)
        self.voltage_entry = ttk.Entry(config_frame)
        self.voltage_entry.grid(row=1, column=1)

        ttk.Label(config_frame, text="Corriente (A):").grid(row=2, column=0, padx=5, pady=5)
        self.current_entry = ttk.Entry(config_frame)
        self.current_entry.grid(row=2, column=1)

        ttk.Label(config_frame, text="Potencia (W):").grid(row=3, column=0, padx=5, pady=5)
        self.power_entry = ttk.Entry(config_frame)
        self.power_entry.grid(row=3, column=1)

        apply_button = ttk.Button(config_frame, text="Aplicar Configuración", command=self.apply_settings)
        apply_button.grid(row=4, column=0, columnspan=2, pady=5)

        # Frame de Protección
        protection_frame = ttk.LabelFrame(self.main_panel, text="Protecciones")
        protection_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(protection_frame, text="OVP (V):").grid(row=0, column=0, padx=5, pady=5)
        self.ovp_entry = ttk.Entry(protection_frame)
        self.ovp_entry.grid(row=0, column=1)

        ttk.Label(protection_frame, text="OCP (A):").grid(row=1, column=0, padx=5, pady=5)
        self.ocp_entry = ttk.Entry(protection_frame)
        self.ocp_entry.grid(row=1, column=1)

        apply_protection_button = ttk.Button(protection_frame, text="Aplicar Protecciones", command=self.apply_protections)
        apply_protection_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Frame de Mediciones
        measurement_frame = ttk.LabelFrame(self.main_panel, text="Mediciones en Tiempo Real")
        measurement_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        measure_voltage_button = ttk.Button(measurement_frame, text="Medir Voltaje", command=self.measure_voltage)
        measure_voltage_button.grid(row=0, column=0, padx=5, pady=5)

        self.voltage_label = ttk.Label(measurement_frame, text="Voltaje: N/A")
        self.voltage_label.grid(row=0, column=1)

        measure_current_button = ttk.Button(measurement_frame, text="Medir Corriente", command=self.measure_current)
        measure_current_button.grid(row=1, column=0, padx=5, pady=5)

        self.current_label = ttk.Label(measurement_frame, text="Corriente: N/A")
        self.current_label.grid(row=1, column=1)

        measure_power_button = ttk.Button(measurement_frame, text="Medir Potencia", command=self.measure_power)
        measure_power_button.grid(row=2, column=0, padx=5, pady=5)

        self.power_label = ttk.Label(measurement_frame, text="Potencia: N/A")
        self.power_label.grid(row=2, column=1)

    def connect(self):
        """Conecta al dispositivo."""
        ip = self.ip_entry.get()
        if ip:
            self.controller = IT6000CController(ip)
            self.controller.connect()
            messagebox.showinfo("Conexión", "Conectado al dispositivo.")
        else:
            messagebox.showwarning("Advertencia", "Ingrese una dirección IP válida.")

    def disconnect(self):
        """Desconecta del dispositivo."""
        if self.controller:
            self.controller.disconnect()
            self.controller = None
            messagebox.showinfo("Conexión", "Desconectado del dispositivo.")
        else:
            messagebox.showwarning("Advertencia", "No hay conexión activa.")

    def apply_settings(self):
        """Aplica la configuración al dispositivo."""
        if self.controller:
            mode = self.mode_var.get()
            voltage = self.voltage_entry.get()
            current = self.current_entry.get()
            power = self.power_entry.get()
            try:
                self.controller.configure_mode(mode)
                if voltage:
                    self.controller.set_voltage(float(voltage))
                if current:
                    self.controller.set_current(float(current))
                if power:
                    self.controller.send_command(f"SOURce:POWer {float(power)}")
                messagebox.showinfo("Configuración", "Parámetros aplicados correctamente.")
            except ValueError:
                messagebox.showerror("Error", "Ingrese valores numéricos válidos.")
        else:
            messagebox.showwarning("Advertencia", "Conéctese al dispositivo primero.")

    def apply_protections(self):
        """Configura las protecciones."""
        if self.controller:
            ovp = self.ovp_entry.get()
            ocp = self.ocp_entry.get()
            try:
                if ovp:
                    self.controller.set_protection(ovp=float(ovp))
                if ocp:
                    self.controller.set_protection(ocp=float(ocp))
                messagebox.showinfo("Protecciones", "Protecciones configuradas correctamente.")
            except ValueError:
                messagebox.showerror("Error", "Ingrese valores numéricos válidos.")
        else:
            messagebox.showwarning("Advertencia", "Conéctese al dispositivo primero.")

    def measure_voltage(self):
        """Realiza la medición de voltaje."""
        if self.controller:
            voltage = self.controller.measure_voltage()
            self.voltage_label.config(text=f"Voltaje: {voltage} V")
        else:
            messagebox.showwarning("Advertencia", "Conéctese al dispositivo primero.")

    def measure_current(self):
        """Realiza la medición de corriente."""
        if self.controller:
            current = self.controller.measure_current()
            self.current_label.config(text=f"Corriente: {current} A")
        else:
            messagebox.showwarning("Advertencia", "Conéctese al dispositivo primero.")

    def measure_power(self):
        """Realiza la medición de potencia."""
        if self.controller:
            power = self.controller.measure_power()
            self.power_label.config(text=f"Potencia: {power} W")
        else:
            messagebox.showwarning("Advertencia", "Conéctese al dispositivo primero.")
