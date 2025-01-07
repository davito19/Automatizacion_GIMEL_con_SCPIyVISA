import pyvisa

class IT7900Controller:
    def __init__(self, ip_address, port=8080):
        self.resource_name = f"TCPIP::{ip_address}::{port}::SOCKET"
        self.rm = pyvisa.ResourceManager()
        self.instrument = None

    def connect(self):
        """Conecta al emulador IT7900."""
        try:
            self.instrument = self.rm.open_resource(self.resource_name)
            self.instrument.timeout = 5000
            self.instrument.write_termination = "\n"
            self.instrument.read_termination = "\n"
            print(f"Conectado a {self.resource_name}")
        except Exception as e:
            print(f"Error al conectar al dispositivo: {e}")

    def disconnect(self):
        """Cierra la conexión con el emulador."""
        if self.instrument:
            self.instrument.close()
            print("Conexión cerrada.")

    def send_command(self, command):
        """Envía un comando SCPI."""
        try:
            self.instrument.write(command)
            print(f"Comando enviado: {command}")
        except Exception as e:
            print(f"Error al enviar comando: {e}")

    def query(self, command):
        """Realiza una consulta SCPI."""
        try:
            response = self.instrument.query(command)
            return response.strip()
        except Exception as e:
            print(f"Error al realizar consulta: {e}")
            return None

    # Funciones Básicas
    def set_output_mode(self, mode="AC"):
        """Configura el modo de salida: AC, DC, ACDC."""
        self.send_command(f"FUNC {mode}")

    def set_phase_mode(self, mode="ONE"):
        """Configura el modo de fase: ONE (monofásico), THREE (trifásico)."""
        self.send_command(f"SYST:FUNC {mode}")

    def set_waveform(self, waveform="SINE"):
        """Configura la forma de onda: SINE, SQUARE, TRIANGLE, etc."""
        self.send_command(f"WAVE {waveform.upper()}")

    def set_voltage(self, voltage, phase=None):
        """Configura el voltaje RMS. Si se especifica la fase, se configura esa fase."""
        command = f"VOLT {voltage}" if not phase else f"PVOLT {phase},{voltage}"
        self.send_command(command)

    def set_current(self, current):
        """Configura el límite de corriente RMS."""
        self.send_command(f"CURR {current}")

    def set_frequency(self, frequency):
        """Configura la frecuencia de salida."""
        self.send_command(f"FREQ {frequency}")

    def enable_output(self, enable=True):
        """Activa o desactiva la salida."""
        state = "ON" if enable else "OFF"
        self.send_command(f"OUTP {state}")

    # Capacidades de Medición
    def measure_voltage(self):
        """Mide el voltaje RMS."""
        return self.query("MEAS:VOLT?")

    def measure_current(self):
        """Mide la corriente RMS."""
        return self.query("MEAS:CURR?")

    def measure_power(self):
        """Mide la potencia real."""
        return self.query("MEAS:POW?")

    def measure_frequency(self):
        """Mide la frecuencia actual."""
        return self.query("MEAS:FREQ?")

    def measure_harmonics(self, harmonic_order, phase="A"):
        """Mide un armónico específico."""
        return self.query(f"FETC:VOLT:HARM? {phase},{harmonic_order}")

    def measure_thd(self, phase="A"):
        """Mide la distorsión armónica total (THD) para una fase."""
        return self.query(f"FETC:VOLT:HARM:THD? {phase}")

    # Funciones Avanzadas
    def configure_list_mode(self, steps):
        """Configura el modo lista con pasos predefinidos."""
        self.send_command("LIST:CRE")
        for step in steps:
            self.send_command(f"LIST:STEP {step}")
        self.send_command("LIST:CONF")

    def start_sweep(self, start, stop, step, mode="VOLT"):
        """Configura y comienza un barrido de parámetros."""
        self.send_command(f"SWE:{mode}:STAR {start}")
        self.send_command(f"SWE:{mode}:STOP {stop}")
        self.send_command(f"SWE:{mode}:STEP {step}")
        self.send_command("INIT:SWE")

    def configure_protection(self, voltage_limit=None, current_limit=None):
        """Configura límites de protección de voltaje y corriente."""
        if voltage_limit:
            self.send_command(f"VOLT:LIM {voltage_limit}")
        if current_limit:
            self.send_command(f"CURR:LIM {current_limit}")

    # Protecciones y Seguridad
    def clear_protection(self):
        """Limpia el estado de protección."""
        self.send_command("OUTP:PROT:CLE")

    # Funciones Osciloscopio
    def start_scope(self):
        """Inicia el osciloscopio."""
        self.send_command("SCOP:RUN")

    def stop_scope(self):
        """Detiene el osciloscopio."""
        self.send_command("SCOP:STOP")

    def capture_single(self):
        """Captura un solo evento."""
        self.send_command("SCOP:SING")

# Ejemplo de Uso
if __name__ == "__main__":
    ip = "192.168.0.101"
    controller = IT7900Controller(ip)

    controller.connect()
    controller.set_output_mode("AC")
    controller.set_phase_mode("ONE")
    controller.set_waveform("SINE")
    controller.set_voltage(220)
    controller.set_frequency(50)
    controller.enable_output(True)

    print(f"Voltaje RMS: {controller.measure_voltage()} V")
    print(f"Corriente RMS: {controller.measure_current()} A")
    print(f"Potencia Real: {controller.measure_power()} W")

    controller.enable_output(False)
    controller.disconnect()
