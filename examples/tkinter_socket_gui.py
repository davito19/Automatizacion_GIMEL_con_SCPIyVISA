import tkinter as tk
from tkinter import messagebox
import socket
import pyvisa

class EquipmentControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Equipos con Socket y PyVISA")

        self.visa_address = tk.StringVar()
        self.command = tk.StringVar()
        self.response = tk.StringVar()

        self.rm = pyvisa.ResourceManager()
        self.instrument = None

        # Configuración de la interfaz gráfica
        self.create_widgets()

    def create_widgets(self):
        # Dirección VISA
        tk.Label(self.root, text="Dirección VISA:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.visa_address, width=30).grid(row=0, column=1, padx=10, pady=10)

        # Botón para conectarse al equipo
        tk.Button(self.root, text="Conectar", command=self.connect_equipment).grid(row=0, column=2, padx=10, pady=10)

        # Comando a enviar
        tk.Label(self.root, text="Comando:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.command, width=50).grid(row=1, column=1, padx=10, pady=10)

        # Botón para enviar comando y esperar respuesta
        tk.Button(self.root, text="Enviar y Esperar Respuesta", command=self.send_command_with_response).grid(row=1, column=2, padx=10, pady=10)

        # Botón para enviar comando sin esperar respuesta
        tk.Button(self.root, text="Enviar Sin Respuesta", command=self.send_command_no_response).grid(row=2, column=2, padx=10, pady=10)

        # Respuesta del equipo
        tk.Label(self.root, text="Respuesta:").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.response, width=50, state='readonly').grid(row=3, column=1, padx=10, pady=10)

    def connect_equipment(self):
        visa_address = self.visa_address.get()
        try:
            self.instrument = self.rm.open_resource(visa_address)
            # For Serial and TCP/IP socket connections enable the read Termination Character, or read's will timeout
            if self.instrument.resource_name.startswith('ASRL') or self.instrument.resource_name.endswith('SOCKET'):
                self.instrument.read_termination = '\n'
                print("yes")
            messagebox.showinfo("Conexión", f"Conectado exitosamente a {visa_address}")
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar al equipo: {e}")

    def send_command_with_response(self):
        if self.instrument is None:
            messagebox.showerror("Error", "No hay equipo conectado")
            return

        command = self.command.get()
        print(command)
        try:
            response = self.instrument.query(command)
            self.response.set(response)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el comando: {e}")

    def send_command_no_response(self):
        if self.instrument is None:
            messagebox.showerror("Error", "No hay equipo conectado")
            return

        command = self.command.get()
        try:
            self.instrument.write(command)
            messagebox.showinfo("Comando Enviado", "El comando fue enviado exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el comando: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EquipmentControlApp(root)
    root.mainloop()
