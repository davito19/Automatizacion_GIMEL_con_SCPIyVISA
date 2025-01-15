import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import threading
import time
from controller.IT7900_controller import IT7900Controller 
import csv
from collections import deque
from datetime import datetime

class IT7900App:
    def __init__(self, main_panel):
        self.controller = None
        self.main_panel = main_panel
        self.running = False
        self.create_tabs()

    def create_tabs(self):
        """Crea pestañas en la UI."""
        notebook = ttk.Notebook(self.main_panel)
        notebook.pack(fill="both", expand=True)

        # Crear frames para cada pestaña
        self.connection_tab = ttk.Frame(notebook)
        self.config_tab = ttk.Frame(notebook)
        self.protection_tab = ttk.Frame(notebook)
        self.graph_tab = ttk.Frame(notebook)

        # Agregar pestañas al Notebook
        notebook.add(self.connection_tab, text="Conexión")
        notebook.add(self.config_tab, text="Configuración de Salida")
        notebook.add(self.protection_tab, text="Protecciones")
        notebook.add(self.graph_tab, text="Osciloscopio y Gráficos")

        # Crear widgets para cada pestaña
        self.create_connection_tab()
        self.create_config_tab()
        self.create_protection_tab()
        self.create_graph_tab()

    def create_connection_tab(self):
        """Crea la pestaña de conexión."""
        ttk.Label(self.connection_tab, text="IP del Emulador:").grid(row=0, column=0, padx=5, pady=5)
        self.ip_entry = ttk.Entry(self.connection_tab)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)

        connect_button = ttk.Button(self.connection_tab, text="Conectar", command=self.connect)
        connect_button.grid(row=0, column=2, padx=5, pady=5)

        disconnect_button = ttk.Button(self.connection_tab, text="Desconectar", command=self.disconnect)
        disconnect_button.grid(row=0, column=3, padx=5, pady=5)

    def create_config_tab(self):
        """Crea la pestaña de configuración de salida."""
        ttk.Label(self.config_tab, text="Modo de Operación:").grid(row=0, column=0, padx=5, pady=5)
        self.mode_var = tk.StringVar(value="AC")
        ttk.Combobox(self.config_tab, textvariable=self.mode_var, values=["AC", "DC", "AC+DC"]).grid(row=0, column=1)

        ttk.Label(self.config_tab, text="Voltaje (V):").grid(row=1, column=0, padx=5, pady=5)
        self.voltage_entry = ttk.Entry(self.config_tab)
        self.voltage_entry.grid(row=1, column=1)

        ttk.Label(self.config_tab, text="Corriente (A):").grid(row=2, column=0, padx=5, pady=5)
        self.current_entry = ttk.Entry(self.config_tab)
        self.current_entry.grid(row=2, column=1)

        ttk.Label(self.config_tab, text="Frecuencia (Hz):").grid(row=3, column=0, padx=5, pady=5)
        self.frequency_entry = ttk.Entry(self.config_tab)
        self.frequency_entry.grid(row=3, column=1)

        ttk.Label(self.config_tab, text="Potencia (W):").grid(row=4, column=0, padx=5, pady=5)
        self.power_entry = ttk.Entry(self.config_tab)
        self.power_entry.grid(row=4, column=1)

        apply_button = ttk.Button(self.config_tab, text="Aplicar Configuración", command=self.apply_settings)
        apply_button.grid(row=5, column=0, columnspan=2, pady=5)

    def create_protection_tab(self):
        """Crea la pestaña de protecciones."""
        ttk.Label(self.protection_tab, text="OVP (V):").grid(row=0, column=0, padx=5, pady=5)
        self.ovp_entry = ttk.Entry(self.protection_tab)
        self.ovp_entry.grid(row=0, column=1)

        ttk.Label(self.protection_tab, text="OCP (A):").grid(row=1, column=0, padx=5, pady=5)
        self.ocp_entry = ttk.Entry(self.protection_tab)
        self.ocp_entry.grid(row=1, column=1)

        apply_protection_button = ttk.Button(self.protection_tab, text="Aplicar Protecciones", command=self.apply_protections)
        apply_protection_button.grid(row=2, column=0, columnspan=2, pady=5)

    def connect(self):
        """Conecta al dispositivo."""
        ip = self.ip_entry.get()
        if ip:
            self.controller = IT7900Controller(ip)
            self.controller.connect()
            messagebox.showinfo("Conexión", "Conectado al dispositivo.")
        else:
            messagebox.showwarning("Advertencia", "Ingrese una dirección IP válida.")

    def disconnect(self):
        """Desconecta del dispositivo."""
        if self.controller:
            self.controller.disconnect()
            self.controller = None
            self.stop_graph()
            messagebox.showinfo("Conexión", "Desconectado del dispositivo.")
        else:
            messagebox.showwarning("Advertencia", "No hay conexión activa.")

    def apply_settings(self):
        """Aplica la configuración al dispositivo."""
        if self.controller:
            try:
                mode = self.mode_var.get()
                voltage = float(self.voltage_entry.get())
                current = float(self.current_entry.get())
                frequency = float(self.frequency_entry.get())
                power = float(self.power_entry.get())

                self.controller.set_output_mode(mode)
                self.controller.set_voltage(voltage)
                self.controller.set_current(current)
                self.controller.send_command(f"FREQ {frequency}")
                self.controller.enable_output()
                #self.controller.send_command(f"POWer {power}")

                messagebox.showinfo("Configuración", "Parámetros aplicados correctamente.")
            except ValueError:
                messagebox.showerror("Error", "Ingrese valores numéricos válidos.")
        else:
            messagebox.showwarning("Advertencia", "Conéctese al dispositivo primero.")

    def apply_protections(self):
        """Configura las protecciones."""
        if self.controller:
            try:
                ovp = float(self.ovp_entry.get())
                ocp = float(self.ocp_entry.get())

                self.controller.set_protection(ovp=ovp, ocp=ocp)

                messagebox.showinfo("Protecciones", "Protecciones configuradas correctamente.")
            except ValueError:
                messagebox.showerror("Error", "Ingrese valores numéricos válidos.")
        else:
            messagebox.showwarning("Advertencia", "Conéctese al dispositivo primero.")

    def start_graph(self):
        """Inicia la gráfica en tiempo real."""
        if self.controller:
            self.running = True
            self.controller.start_scope()
            threading.Thread(target=self.update_graph, daemon=True).start()
        else:
            messagebox.showwarning("Advertencia", "Conéctese al dispositivo primero.")

    def stop_graph(self):
        """Detiene la gráfica en tiempo real."""
        self.controller.stop_scope()
        self.running = False

    def create_graph_tab(self):
        """Crea la pestaña de gráficos."""
        # Frame superior para valores en tiempo real
        value_frame = ttk.Frame(self.graph_tab)
        value_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        self.voltage_rms_label = ttk.Label(value_frame, text="Voltaje RMS: N/A")
        self.voltage_rms_label.grid(row=0, column=0, padx=5)

        self.current_rms_label = ttk.Label(value_frame, text="Corriente RMS: N/A")
        self.current_rms_label.grid(row=0, column=1, padx=5)

        self.power_label = ttk.Label(value_frame, text="Potencia: N/A")
        self.power_label.grid(row=0, column=2, padx=5)

        self.frequency_label = ttk.Label(value_frame, text="Frecuencia: N/A")
        self.frequency_label.grid(row=0, column=3, padx=5)

        # Crear subplots en una cuadrícula de 2x3
        self.figure, self.axes = plt.subplots(2, 3, figsize=(10, 8), dpi=100)
        self.figure.tight_layout(pad=3.0)

        # Configurar títulos para cada subplot
        self.axes[0, 0].set_title("Voltaje RMS")
        self.axes[0, 0].set_ylabel("Voltaje (V)")

        self.axes[0, 1].set_title("Corriente RMS")
        self.axes[0, 1].set_ylabel("Corriente (A)")

        self.axes[0, 2].set_title("Potencia")
        self.axes[0, 2].set_ylabel("Potencia (W)")

        self.axes[1, 0].set_title("Frecuencia")
        self.axes[1, 0].set_ylabel("Frecuencia (Hz)")

        self.axes[1, 1].set_title("Voltaje Instantáneo")
        self.axes[1, 1].set_ylabel("Voltaje (V)")
        self.axes[1, 1].set_xlabel("Tiempo (ms)")

        # Deshabilitar el último subplot si no se usa
        self.axes[1, 2].axis("off")

        self.canvas = FigureCanvasTkAgg(self.figure, self.graph_tab)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Botones de control de gráfica
        control_frame = ttk.Frame(self.graph_tab)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        self.start_button = ttk.Button(control_frame, text="Iniciar Gráfica", command=self.start_graph)
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.stop_button = ttk.Button(control_frame, text="Detener Gráfica", command=self.stop_graph)
        self.stop_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def update_graph(self):
        """Actualiza la gráfica en tiempo real y guarda datos en un archivo CSV."""
        # Configuración inicial
        max_points = 100  # Máximo de puntos a mostrar en los gráficos
        x_data = deque(maxlen=max_points)
        voltage_rms_data = deque(maxlen=max_points)
        current_rms_data = deque(maxlen=max_points)
        power_data = deque(maxlen=max_points)
        frequency_data = deque(maxlen=max_points)
        voltage_instantaneous_data = deque(maxlen=1200)

        # Crear archivo CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ip_address = self.controller.resource_name.split("::")[1]
        csv_filename = f"IT7900_{ip_address}_{timestamp}.csv"

        with open(csv_filename, mode="w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([
                "Tiempo (s)", 
                "Voltaje RMS (V)", 
                "Corriente RMS (A)", 
                "Potencia (W)", 
                "Frecuencia (Hz)", 
                "Voltaje Instantáneo (V)"
            ])

            # Tiempo inicial
            start_time = time.time()

            while self.running:
                try:
                    # Obtener datos del dispositivo
                    voltage_rms = float(self.controller.measure_voltage())
                    current_rms = float(self.controller.measure_current())
                    power = float(self.controller.measure_power())
                    frequency = float(self.controller.measure_frequency())
                    voltage_instantaneous = self.controller.measure_instantaneous_voltage()

                    # Tiempo transcurrido
                    elapsed_time = time.time() - start_time

                    # Actualizar datos
                    x_data.append(elapsed_time)
                    voltage_rms_data.append(voltage_rms)
                    current_rms_data.append(current_rms)
                    power_data.append(power)
                    frequency_data.append(frequency)

                    if voltage_instantaneous:
                        voltage_instantaneous_data.extend(voltage_instantaneous)

                    # Guardar datos en CSV
                    csv_writer.writerow([
                        elapsed_time, 
                        voltage_rms, 
                        current_rms, 
                        power, 
                        frequency, 
                        ",".join(map(str, voltage_instantaneous))
                    ])

                    # Actualizar subplots
                    self.axes[0, 0].clear()
                    self.axes[0, 0].plot(x_data, voltage_rms_data, color="blue")
                    self.axes[0, 0].set_title("Voltaje RMS")
                    self.axes[0, 0].set_ylabel("Voltaje (V)")

                    self.axes[0, 1].clear()
                    self.axes[0, 1].plot(x_data, current_rms_data, color="green")
                    self.axes[0, 1].set_title("Corriente RMS")
                    self.axes[0, 1].set_ylabel("Corriente (A)")

                    self.axes[0, 2].clear()
                    self.axes[0, 2].plot(x_data, power_data, color="red")
                    self.axes[0, 2].set_title("Potencia")
                    self.axes[0, 2].set_ylabel("Potencia (W)")

                    self.axes[1, 0].clear()
                    self.axes[1, 0].plot(x_data, frequency_data, color="purple")
                    self.axes[1, 0].set_title("Frecuencia")
                    self.axes[1, 0].set_ylabel("Frecuencia (Hz)")

                    self.axes[1, 1].clear()
                    if voltage_instantaneous_data:
                        time_instant = list(range(len(voltage_instantaneous_data)))
                        self.axes[1, 1].plot(time_instant, list(voltage_instantaneous_data), color="orange")
                    self.axes[1, 1].set_title("Voltaje Instantáneo")
                    self.axes[1, 1].set_ylabel("Voltaje (V)")
                    self.axes[1, 1].set_xlabel("Tiempo (ms)")

                    self.figure.tight_layout(pad=3.0)
                    self.canvas.draw()

                    # Actualizar valores en tiempo real en la interfaz
                    self.voltage_rms_label.config(text=f"Voltaje RMS: {voltage_rms:.2f} V")
                    self.current_rms_label.config(text=f"Corriente RMS: {current_rms:.2f} A")
                    self.power_label.config(text=f"Potencia: {power:.2f} W")
                    self.frequency_label.config(text=f"Frecuencia: {frequency:.2f} Hz")

                except Exception as e:
                    print(f"Error al actualizar gráfica: {e}")
                    self.running = False
