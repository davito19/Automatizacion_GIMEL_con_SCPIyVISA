import tkinter as tk
from tkinter import ttk, messagebox
from controller.IT7900_controller import IT7900Controller

class IT7900App:
    def __init__(self, main_panel: tk.Frame):
        """Inicializa la interfaz para el control del emulador IT7900."""
        self.main_panel = main_panel
        self.controller = None
        self.setup_ui()

    def setup_ui(self):
        """Configura los elementos de la interfaz gráfica."""
        # Frame de conexión
        connection_frame = ttk.LabelFrame(self.main_panel, text="Conexión")
        connection_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(connection_frame, text="IP del Dispositivo:").grid(row=0, column=0, padx=5, pady=5)
        self.ip_entry = ttk.Entry(connection_frame)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)

        connect_button = ttk.Button(connection_frame, text="Conectar", command=self.connect_device)
        connect_button.grid(row=0, column=2, padx=5, pady=5)

        disconnect_button = ttk.Button(connection_frame, text="Desconectar", command=self.disconnect_device)
        disconnect_button.grid(row=0, column=3, padx=5, pady=5)

        # Frame de configuración
        config_frame = ttk.LabelFrame(self.main_panel, text="Configuración de Salida")
        config_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(config_frame, text="Modo de Salida:").grid(row=0, column=0, padx=5, pady=5)
        self.mode_var = tk.StringVar(value="AC")
        mode_combobox = ttk.Combobox(config_frame, textvariable=self.mode_var, values=["AC", "DC", "ACDC"])
        mode_combobox.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(config_frame, text="Voltaje (V):").grid(row=1, column=0, padx=5, pady=5)
        self.voltage_entry = ttk.Entry(config_frame)
        self.voltage_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(config_frame, text="Frecuencia (Hz):").grid(row=2, column=0, padx=5, pady=5)
        self.frequency_entry = ttk.Entry(config_frame)
        self.frequency_entry.grid(row=2, column=1, padx=5, pady=5)

        apply_button = ttk.Button(config_frame, text="Aplicar Configuración", command=self.apply_settings)
        apply_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Frame de mediciones
        measurement_frame = ttk.LabelFrame(self.main_panel, text="Mediciones")
        measurement_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        ttk.Button(measurement_frame, text="Medir Voltaje RMS", command=self.measure_voltage).grid(row=0, column=0, padx=5, pady=5)
        self.voltage_label = ttk.Label(measurement_frame, text="Voltaje RMS: N/A")
        self.voltage_label.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(measurement_frame, text="Medir Corriente RMS", command=self.measure_current).grid(row=1, column=0, padx=5, pady=5)
        self.current_label = ttk.Label(measurement_frame, text="Corriente RMS: N/A")
        self.current_label.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(measurement_frame, text="Medir Potencia Real", command=self.measure_power).grid(row=2, column=0, padx=5, pady=5)
        self.power_label = ttk.Label(measurement_frame, text="Potencia Real: N/A")
        self.power_label.grid(row=2, column=1, padx=5, pady=5)

    # Métodos para control del emulador
    def connect_device(self):
        ip_address = self.ip_entry.get()
        if ip_address:
            try:
                self.controller = IT7900Controller(ip_address)
                self.controller.connect()
                messagebox.showinfo("Conexión", "Conectado al dispositivo.")
            except Exception as e:
                # Mostrar el error en un cuadro de mensaje
                messagebox.showerror("Error de Conexión", f"No se pudo conectar al dispositivo:\n{e}")
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingrese una IP válida.")


    def disconnect_device(self):
        if self.controller:
            self.controller.disconnect()
            messagebox.showinfo("Conexión", "Desconectado del dispositivo.")
        else:
            messagebox.showwarning("Advertencia", "No hay conexión activa.")

    def apply_settings(self):
        if self.controller:
            mode = self.mode_var.get()
            voltage = self.voltage_entry.get()
            frequency = self.frequency_entry.get()
            try:
                self.controller.set_output_mode(mode)
                self.controller.set_voltage(float(voltage))
                self.controller.set_frequency(float(frequency))
                messagebox.showinfo("Configuración", "Parámetros aplicados correctamente.")
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos para voltaje y frecuencia.")
        else:
            messagebox.showwarning("Advertencia", "No hay conexión activa.")

    def measure_voltage(self):
        if self.controller:
            voltage = self.controller.measure_voltage()
            self.voltage_label.config(text=f"Voltaje RMS: {voltage} V")

    def measure_current(self):
        if self.controller:
            current = self.controller.measure_current()
            self.current_label.config(text=f"Corriente RMS: {current} A")

    def measure_power(self):
        if self.controller:
            power = self.controller.measure_power()
            self.power_label.config(text=f"Potencia Real: {power} W")
