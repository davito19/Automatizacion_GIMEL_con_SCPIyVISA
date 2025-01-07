import pyvisa
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque



# Change VISA_ADDRESS to a SOCKET address, e.g. 'TCPIP::169.254.104.59::5025::SOCKET'
VISA_ADDRESS = 'TCPIP0::192.168.0.100::8080::SOCKET'

# Comandos SCPI a ejecutar
commands = [
    "SYSTem:REMote",  
    "*IDN?",                               # Consultar la identificación del instrumento                                              # Poner el instrumento en modo de control remoto                             # Consultar la identificación del instrumento
    "SYSTem:FUNCtion ONE",                 # Configurar el modo de energía en 1-fase
    "FUNCtion AC",                         # Configurar la salida en modo AC
    "VOLTage 220",                         # Configurar el voltaje RMS a 220V
    "FREQuency 60.0",                      # Configurar la frecuencia a 60Hz
    "CURRent:PROTection:RMS 90",           # Configurar la protección RMS de corriente a 90A
    "CURRent:PROTection:PEAK 270",         # Configurar la protección pico de corriente a 270A
    "OUTPut ON"                          # Encender la salida del instrumento
]

try:
    # Create a connection (session) to the TCP/IP socket on the instrument.
    resourceManager = pyvisa.ResourceManager()
    session = resourceManager.open_resource(VISA_ADDRESS)

    # For Serial and TCP/IP socket connections enable the read Termination Character, or read's will timeout
    if session.resource_name.startswith('ASRL') or session.resource_name.endswith('SOCKET'):
        session.read_termination = '\n'

    # We can find out details of the connection
    print('IP: %s\nHostname: %s\nPort: %d\n' %
          (session.get_visa_attribute(pyvisa.constants.VI_ATTR_TCPIP_ADDR),
           session.get_visa_attribute(pyvisa.constants.VI_ATTR_TCPIP_HOSTNAME),
           session.get_visa_attribute(pyvisa.constants.VI_ATTR_TCPIP_PORT)))

    # Identificar el dispositivo y ejecutar comandos de configuración

    # Ejecución de los comandos SCPI
    for command in commands:
        if "?" in command:
            # Si el comando es una consulta, imprimir el resultado
            response = session.query(command)
            print(f"{command} -> {response.strip('\n')}")
        else:
            # Si el comando es una configuración, solo enviarlo
            session.write(command)

    # Tomar medidas durante 1 minuto (60 segundos)
    tiempo_inicial = time.time()
    # Inicializar deques para almacenar los datos de manera eficiente
    tiempo_max = 60  # Almacenar los últimos 60 segundos de datos
    tiempos = deque(maxlen=tiempo_max)
    voltajes = deque(maxlen=tiempo_max)
    corrientes = deque(maxlen=tiempo_max)
    potencias = deque(maxlen=tiempo_max)
    # Configuración de la gráfica en tiempo real
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 6))

    # Configuración inicial de los límites de los ejes
    ax1.set_ylim(0, 120)
    ax2.set_ylim(0, 10)
    ax3.set_ylim(0, 2000)

    def actualizar(frame):
        # Medir el voltaje, corriente y potencia
        voltaje = float(session.query("MEASure:VOLTage?"))
        corriente = float(session.query("MEASure:CURRent?"))
        potencia = float(session.query("MEASure:POWer?"))
        # Registrar el tiempo actual
        tiempo_actual = time.time() - tiempo_inicial
        print("time: ", len(tiempos), ":" ,tiempo_actual)
        # Almacenar los datos en las listas
        tiempos.append(tiempo_actual)
        voltajes.append(voltaje)
        corrientes.append(corriente)
        potencias.append(potencia)

        # Limpiar y actualizar las gráficas
        ax1.clear()
        ax1.plot(tiempos, voltajes, label='Voltaje (V)', color='blue')
        ax1.set_xlabel('Tiempo (s)', fontsize=10)
        ax1.set_ylabel('Voltaje (V)', fontsize=10)
        ax1.set_title('Voltaje en función del tiempo', fontsize=12)
        ax1.grid(True)
        ax1.legend()
        ax1.ticklabel_format(useOffset=False, style='plain')  # Evitar notación científica
        # Actualizar límites si el valor excede los límites actuales
        if max(voltajes) > ax1.get_ylim()[1]:
            ax1.set_ylim(0, max(voltajes) * 1.1)

        ax2.clear()
        ax2.plot(tiempos, corrientes, label='Corriente (A)', color='orange')
        ax2.set_xlabel('Tiempo (s)', fontsize=10)
        ax2.set_ylabel('Corriente (A)', fontsize=10)
        ax2.set_title('Corriente en función del tiempo', fontsize=12)
        ax2.grid(True)
        ax2.legend()
        ax2.ticklabel_format(useOffset=False, style='plain')  # Evitar notación científica
        if max(corrientes) > ax2.get_ylim()[1]:
            ax2.set_ylim(0, max(corrientes) * 1.1)

        ax3.clear()
        ax3.plot(tiempos, potencias, label='Potencia (W)', color='green')
        ax3.set_xlabel('Tiempo (s)', fontsize=10)
        ax3.set_ylabel('Potencia (W)', fontsize=10)
        ax3.set_title('Potencia en función del tiempo', fontsize=12)
        ax3.grid(True)
        ax3.legend()
        ax3.ticklabel_format(useOffset=False, style='plain')  # Evitar notación científica
        if max(potencias) > ax3.get_ylim()[1]:
            ax3.set_ylim(0, max(potencias) * 1.1)
        
        plt.tight_layout()

    # Crear la animación
    ani = animation.FuncAnimation(fig, actualizar, interval=100, blit=False, save_count=60)

    # Mostrar la gráfica y detener la ejecución cuando se cierre la ventana
    plt.show()

    # Apagar la salida después de cerrar la ventana
    response = session.query("SYSTem:ERRor?")             # Consultar la información de error del instrumento
    print(f"SYSTem:ERRor? -> {response.strip('\n')}")
    session.write("SYSTem:CLEar")                         # Limpiar la cola de errores
    session.write("OUTPut:PROTection:CLEar")              # Limpiar el estado de protección del instrumento
    session.write("OUTPut OFF")
    # Close the connection to the instrument
    session.close()
    resourceManager.close()

except pyvisa.Error as ex:
    print('An pyvisa error occurred: %s' % ex)
except Exception as e: 
    print('An error occurred: %s' % e)
