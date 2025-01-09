import pyvisa

class IT8600Controller:
    def __init__(self, ip_address, port=8080):
        self.resource_name = f"TCPIP::{ip_address}::{port}::SOCKET"
        self.rm = pyvisa.ResourceManager()
        self.instrument = None

    def connect(self):
        try:
            self.instrument = self.rm.open_resource(self.resource_name)
            self.instrument.timeout = 5000
            self.instrument.write_termination = "\n"
            self.instrument.read_termination = "\n"
            print("Conectado al IT8600")
        except Exception as e:
            print(f"Error al conectar al dispositivo: {e}")

    def disconnect(self):
        if self.instrument:
            self.instrument.close()
            print("Desconectado del IT8600")

    def send_command(self, command):
        try:
            self.instrument.write(command)
        except Exception as e:
            print(f"Error al enviar comando: {e}")

    def query(self, command):
        try:
            return self.instrument.query(command)
        except Exception as e:
            print(f"Error al realizar consulta: {e}")
            return None

    # Modos de operación
    def set_mode(self, mode="AC"):
        self.send_command(f"SYSTem:MODE {mode}")

    def set_load_mode(self, mode="CC"):
        self.send_command(f"FUNC {mode}")

    # Configuración de parámetros
    def set_current(self, value):
        self.send_command(f"CURRent {value}")

    def set_voltage(self, value):
        self.send_command(f"VOLTage {value}")

    def set_power(self, value):
        self.send_command(f"POWer {value}")

    # Medición
    def measure_voltage(self):
        return self.query("MEAS:VOLT?")

    def measure_current(self):
        return self.query("MEAS:CURR?")

    def measure_power(self):
        return self.query("MEAS:POW?")

    def enable_load(self, enable=True):
        state = "ON" if enable else "OFF"
        self.send_command(f"INPut {state}")

# Ejemplo de uso
if __name__ == "__main__":
    controller = IT8600Controller("192.168.0.102")
    controller.connect()
    controller.set_mode("AC")
    controller.set_load_mode("CC")
    controller.set_current(5)
    voltage = controller.measure_voltage()
    print(f"Voltaje medido: {voltage} V")
    controller.disconnect()
