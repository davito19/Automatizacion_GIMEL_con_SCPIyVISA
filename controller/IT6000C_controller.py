import pyvisa

class IT6000CController:
    def __init__(self, ip_address, port=8080):
        self.resource_name = f"TCPIP::{ip_address}::{port}::SOCKET"
        self.rm = pyvisa.ResourceManager()
        self.instrument = None

    def connect(self):
        """Conectar al dispositivo"""
        try:
            self.instrument = self.rm.open_resource(self.resource_name)
            self.instrument.timeout = 5000
            self.instrument.write_termination = "\n"
            self.instrument.read_termination = "\n"
            print("Conectado al IT6000C")
        except Exception as e:
            print(f"Error al conectar: {e}")

    def disconnect(self):
        """Desconectar el dispositivo"""
        if self.instrument:
            self.instrument.close()
            print("Desconectado del IT6000C")

    def send_command(self, command):
        """Enviar un comando SCPI"""
        try:
            self.instrument.write(command)
        except Exception as e:
            print(f"Error al enviar comando: {e}")

    def query(self, command):
        """Consultar un comando SCPI"""
        try:
            return self.instrument.query(command)
        except Exception as e:
            print(f"Error al realizar consulta: {e}")
            return None

    # Funciones Básicas
    def set_output_state(self, state):
        """Habilitar o deshabilitar salida"""
        self.send_command(f"OUTPut {1 if state else 0}")

    def set_voltage(self, voltage):
        """Configurar voltaje de salida"""
        self.send_command(f"SOURce:VOLTage {voltage}")

    def set_current(self, current):
        """Configurar corriente de salida"""
        self.send_command(f"SOURce:CURRent {current}")

    def measure_voltage(self):
        """Medir el voltaje de salida"""
        return self.query("MEASure:VOLTage?")

    def measure_current(self):
        """Medir la corriente de salida"""
        return self.query("MEASure:CURRent?")

    def measure_power(self):
        """Medir la potencia de salida"""
        return self.query("MEASure:POWer?")

    def configure_mode(self, mode="CV"):
        """Configurar el modo de operación (CV, CC, CP)"""
        self.send_command(f"SOURce:FUNCtion {mode}")

    def set_protection(self, ovp=None, ocp=None):
        """Configurar protecciones"""
        if ovp is not None:
            self.send_command(f"SOURce:VOLTage:PROTection:LEVel {ovp}")
        if ocp is not None:
            self.send_command(f"SOURce:CURRent:PROTection:LEVel {ocp}")
