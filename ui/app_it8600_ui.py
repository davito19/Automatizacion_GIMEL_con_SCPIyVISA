import tkinter as tk
from tkinter import ttk
from controller.IT8600_controller import IT8600Controller  # Asegúrate de que esta clase esté definida en tu proyecto.

class IT8600App:
    def __init__(self, main_panel):
        """
        Inicializa la UI dentro de un main_panel proporcionado.
        """
        self.controller = None  # Instancia del controlador IT8600
        self.main_panel = main_panel
        self.create_widgets()

    def create_widgets(self):
        """
        Construye la interfaz dentro del panel principal.
        """
        # Frame de Conexión
        connection_frame = ttk.LabelFrame(self.main_panel, text="Conexión")
        connection_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(connection_frame, text="IP del Dispositivo:").grid(row=0, column=0, padx=5, pady=5)
        self.ip_entry = ttk.Entry(connection_frame)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)

        connect_button = ttk.Button(connection_frame, text="Conectar", command=self.connect)
        connect_button.grid(row=0, column=2, padx=5, pady=5)

        disconnect_button = ttk.Button(connection_frame, text="Desconectar", command=self.disconnect)
        disconnect_button.grid(row=0, column=3, padx=5, pady=5)

        # Frame de Configuración
        config_frame = ttk.LabelFrame(self.main_panel, text="Configuración de Carga")
        config_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Frame de Configuración (dentro de create_widgets)
        ttk.Label(config_frame, text="Modo de Carga:").grid(row=0, column=0, padx=5, pady=5)
        self.mode_var = tk.StringVar()
        self.mode_combobox = ttk.Combobox(config_frame, textvariable=self.mode_var, values=["CC", "CR", "CP", "Short"])
        self.mode_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.mode_combobox.current(0)

        ttk.Label(config_frame, text="Corriente (A):").grid(row=1, column=0, padx=5, pady=5)
        self.current_entry = ttk.Entry(config_frame)
        self.current_entry.grid(row=1, column=1, padx=5, pady=5)

        apply_button = ttk.Button(config_frame, text="Aplicar Configuración", command=self.apply_settings)
        apply_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Frame de Mediciones
        measurement_frame = ttk.LabelFrame(self.main_panel, text="Mediciones")
        measurement_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        measure_voltage_button = ttk.Button(measurement_frame, text="Medir Voltaje", command=self.measure_voltage)
        measure_voltage_button.grid(row=0, column=0, padx=5, pady=5)

        self.voltage_label = ttk.Label(measurement_frame, text="Voltaje: N/A")
        self.voltage_label.grid(row=0, column=1, padx=5, pady=5)

        measure_current_button = ttk.Button(measurement_frame, text="Medir Corriente", command=self.measure_current)
        measure_current_button.grid(row=1, column=0, padx=5, pady=5)

        self.current_label = ttk.Label(measurement_frame, text="Corriente: N/A")
        self.current_label.grid(row=1, column=1, padx=5, pady=5)

    def connect(self):
        """
        Conecta al dispositivo usando la IP proporcionada.
        """
        ip_address = self.ip_entry.get()
        if ip_address:
            self.controller = IT8600Controller(ip_address)
            self.controller.connect()
        else:
            self.show_message("Advertencia", "Ingrese una dirección IP válida.")

    def disconnect(self):
        """
        Desconecta del dispositivo.
        """
        if self.controller:
            self.controller.disconnect()
            self.controller = None
        else:
            self.show_message("Advertencia", "No hay conexión activa.")

    def apply_settings(self):
        if self.controller:
            mode = self.mode_var.get()
            try:
                if mode == "Short":
                    self.controller.send_command("INPut:SHORt ON")
                else:
                    self.controller.set_load_mode(mode)
                self.show_message("Información", f"Modo {mode} aplicado correctamente.")
            except Exception as e:
                self.show_message("Error", f"Error al aplicar configuración: {e}")
        else:
            self.show_message("Advertencia", "Conéctese al dispositivo primero.")

    def measure_voltage(self):
        """
        Realiza la medición de voltaje.
        """
        if self.controller:
            voltage = self.controller.measure_voltage()
            self.voltage_label.config(text=f"Voltaje: {voltage} V")
        else:
            self.show_message("Advertencia", "Conéctese al dispositivo primero.")

    def measure_current(self):
        """
        Realiza la medición de corriente.
        """
        if self.controller:
            current = self.controller.measure_current()
            self.current_label.config(text=f"Corriente: {current} A")
        else:
            self.show_message("Advertencia", "Conéctese al dispositivo primero.")

    @staticmethod
    def show_message(title, message):
        """
        Muestra un cuadro de mensaje.
        """
        tk.messagebox.showinfo(title, message)

# Ejemplo de integración
if __name__ == "__main__":
    root = tk.Tk()
    main_panel = ttk.Frame(root)
    main_panel.pack(fill="both", expand=True)

    app = IT8600App(main_panel)
    root.mainloop()