# Manual Técnico del Sistema de Automatización y Monitoreo de Equipos de Laboratorio GIMEL

---

## **1. Configuración de la Red LAN**

Se configuró una red utilizando el estándar IEEE 802.3ab para Gigabit Ethernet, logrando velocidades de hasta 1 Gbps sobre cables UTP categoría 5, según ANSI/TIA-568A, con capacidad para distancias de hasta 100 metros sin pérdida significativa de señal. El switch Alcatel OmniSwitch 6250-P24 fue ajustado mediante CLI para gestionar eficientemente el tráfico de datos, implementando VLAN y asignando direcciones IP estáticas según su manual técnico.

### **1.1. Descripción de las Direcciones IP Asignadas**
Cada instrumento se encuentra configurado con una dirección IP única dentro del segmento de red **192.168.0.x/24**, para garantizar una comunicación adecuada:

- **IT7909-350-90 (Fuente AC):** 192.168.0.100
- **IT6000C (Fuente DC):** 192.168.0.101
- **IT8615L (Emuladores de Carga):**
  - Dispositivo 1: 192.168.0.102
  - Dispositivo 2: 192.168.0.103
  - Dispositivo 3: 192.168.0.104



### **1.2. Configuración de las Interfaces de Red y puerto**

---

### **1.2.1 Configuración de Conexión LAN y Puerto para Socket en el IT6000C**

#### Requisitos Previos
- Asegúrate de que el equipo esté conectado a una red Ethernet funcional.
- Conecta el dispositivo a la red a través del puerto LAN de la parte trasera.
- Verifica que el dispositivo esté apagado antes de realizar cualquier conexión.

#### 1. Acceder al Menú de Configuración de Red
1. Enciende el dispositivo.
2. Presiona la combinación de teclas `[Shift]` + `[P-set]` para entrar al menú de configuración del sistema.

#### 2. Configurar la Interfaz LAN
1. Navega en el menú hasta la opción **LAN** y presiona `[Enter]`.
2. Selecciona **IP-Conf** para configurar los parámetros de red:
   - **IP Mode**:
     - `Auto`: Para asignación automática mediante DHCP.
     - `Manual`: Para configuración manual.
   - **IP**: Introduce la dirección IP deseada (por ejemplo, `192.168.0.100`).
   - **Mask**: Introduce la máscara de subred (por ejemplo, `255.255.255.0`).
   - **Gateway**: Introduce la puerta de enlace (por ejemplo, `192.168.0.1`).
3. Configura valores adicionales si es necesario:
   - **DNS1**: Dirección del servidor DNS preferido.
   - **DNS2**: Dirección del servidor DNS alternativo.
4. Configura el **Socket Port**: Introduce el puerto de comunicación deseado (por defecto, `30000`).

#### 3. Guardar los Cambios
1. Presiona `[Enter]` para guardar cada configuración.
2. Usa `[Esc]` para regresar al menú principal.

#### 4. Probar la Conexión
1. Conecta un dispositivo (como una computadora) en la misma red.
2. Realiza un **ping** al dispositivo utilizando la dirección IP configurada para verificar la conexión.
3. Si configuraste un puerto socket, asegúrate de que el software cliente pueda comunicarse a través del puerto especificado.

---

### **1.2.2 Configuración de Conexión LAN y Puerto para Socket en el IT7900**


#### Requisitos previos
- Conecta el equipo IT7900 a una red mediante el puerto LAN en el panel trasero.
- Asegúrate de que el dispositivo esté apagado antes de realizar cualquier conexión.

#### 1. Acceder al menú de configuración de comunicación
1. Enciende el dispositivo.
2. Presiona `[Shift]` + `[System]` en el panel frontal para acceder al menú del sistema.
3. Usa los botones de navegación o la pantalla táctil para seleccionar la opción **Set the communication interface**.

#### 2. Configurar la interfaz LAN
1. En el menú **LAN Interface**, configura los parámetros necesarios:
   - **IP Mode**:
     - `DHCP`: Asignación automática de dirección IP.
     - `Manual`: Configuración manual de la IP.
   - **IP Address**: Introduce la dirección IP deseada, por ejemplo, `192.168.0.100`.
   - **Subnet Mask**: Especifica la máscara de subred, por ejemplo, `255.255.255.0`.
   - **Gateway**: Configura la puerta de enlace, por ejemplo, `192.168.0.1`.
   - **Socket Port**: Define el puerto de comunicación, por ejemplo, `8080`.


#### 3. Activar y configurar servicios LAN
1. En el mismo menú, habilita los servicios de comunicación necesarios:
   - **RAW Socket**: Habilita la comunicación directa mediante sockets.
   - **Ping**: Activa la función de ping para probar la conectividad.
   - **Telnet-SCPI**: Permite comandos remotos a través de Telnet.


#### 4. Guardar los cambios
1. Una vez configurados los parámetros, presiona `[Enter]` para guardar los cambios.
2. Usa `[Esc]` para regresar al menú principal.


#### 5. Probar la conexión
1. Desde una computadora en la misma red, realiza un **ping** a la dirección IP configurada para confirmar la conectividad.
2. Si configuraste un puerto socket, utiliza software cliente (como PuTTY o Python) para conectarte al puerto y verificar la comunicación.

---

### **1.2.3 Configuración de Conexión LAN y Puerto para Socket en el IT8600**

#### Requisitos previos
- Conecta el equipo IT7900 a una red mediante el puerto LAN en el panel trasero.
- Asegúrate de que el dispositivo esté apagado antes de realizar cualquier conexión.

#### 1. Acceder al menú de configuración
1. Enciende el dispositivo.
2. Presiona el botón `[Menu]` en el panel frontal para acceder al menú principal.

#### 2. Configuración de la interfaz LAN
1. En el menú, selecciona **COMM CONFIG** (Configuración de comunicación) y presiona `[Enter]`.
2. Navega a la opción **LAN** y presiona `[Enter]`.
3. Configura los siguientes parámetros:
   - **IP Mode**:
     - `DHCP`: Para asignación automática de dirección IP.
     - `MANUAL`: Para configuración manual de la IP.
   - **IP Address**: Introduce la dirección IP deseada (por ejemplo, `192.168.0.100`).
   - **Subnet Mask**: Introduce la máscara de subred (por ejemplo, `255.255.255.0`).
   - **Gateway**: Configura la puerta de enlace (por ejemplo, `192.168.0.1`).
   - **Socket Port**: Define el puerto de comunicación (por ejemplo, `8080`).

#### 3. Guardar los cambios
1. Presiona `[Enter]` para guardar cada configuración.
2. Usa `[Esc]` para regresar al menú principal.

#### 4. Verificar la conectividad
1. Conecta un dispositivo en la misma red y realiza un **ping** a la dirección IP configurada.
2. Si configuraste un puerto socket, utiliza un cliente de pruebas como PuTTY o una herramienta de programación (por ejemplo, Python) para verificar la conexión al puerto.

---

### **1.3 Configuración del Switch**

#### Configuración de Red en Topología Estrella con VLAN en Alcatel OS6250/6450

Este segmento describe el proceso paso a paso para configurar una red en topología estrella utilizando VLAN en un switch Alcatel OS6250/6450.

#### Requisitos Previos

1. Un switch Alcatel OS6250/6450.
2. Software de terminal como PuTTY o Tera Term.
3. Credenciales de acceso al switch.
4. Conexión física entre los dispositivos y el switch.

### Pasos para la Configuración

#### 1. Conexión y Acceso al Switch

1. Conecta un cable de consola entre tu computadora y el puerto de consola del switch.
2. Configura la conexión en el software de terminal:
   - Velocidad: **9600 baudios**.
   - Datos: **8 bits**.
   - Paridad: **ninguna**.
   - Bit de parada: **1 bit**.
3. Accede al CLI del switch con las credenciales correspondientes.

#### 2. Configuración de los Puertos

1. Identifica los puertos a utilizar para los dispositivos finales y el puerto troncal.
2. Habilita los puertos:
   ```
   interface ethernet <puerto>
   no shutdown
   ```
3. Verifica el estado de los puertos:
   ```
   show interfaces status
   ```

#### 3. Creación de VLANs

1. Define las VLANs necesarias:
   ```
   vlan <ID_VLAN>
   name <nombre_VLAN>
   exit
   ```
2. Repite este paso para cada VLAN requerida.

#### 4. Asignación de Puertos a las VLANs

- **Modo acceso** (dispositivos finales):
  ```
  interface ethernet <puerto>
  vlan pvid <ID_VLAN>
  exit
  ```
- **Modo troncal** (hacia otro switch o router):
  ```
  interface ethernet <puerto_troncal>
  vlan trunk enable
  vlan trunk allowed <ID_VLAN_1>,<ID_VLAN_2>,...
  exit
  ```

#### 5. Habilitación de Etiquetado 802.1Q

Asegúrate de que el etiquetado de VLAN esté habilitado en los puertos troncales:
``` 
interface ethernet <puerto_troncal>
 vlan tagging enable
 exit
```

#### 6. Configuración de VLAN de Administración (Opcional)

1. Crea una VLAN para administración:
   ```
   vlan <ID_VLAN_ADMIN>
   name ADMIN
   exit
   ```
2. Asigna una dirección IP al switch dentro de esta VLAN:
   ```
   interface vlan <ID_VLAN_ADMIN>
   ip address <IP_ADMIN> <MASCARA>
   exit
   ```

#### 7. Verificación de la Configuración

1. Confirma las VLAN creadas:
   ```
   show vlan
   ```
2. Verifica las interfaces asignadas:
   ```
   show interfaces vlan
   ```
3. Revisa la configuración en ejecución:
   ```
   show running-config
   ```

#### 8. Guardar la Configuración

Para evitar la pérdida de configuración tras un reinicio, guarda los cambios:
``` 
write memory
```

#### 9. Pruebas Finales

1. Conecta los dispositivos finales y verifica la conectividad dentro de cada VLAN.
2. Prueba la conectividad entre las VLAN y el gateway configurado.

#### Notas

- Consulta la documentación oficial del switch para obtener más detalles sobre comandos avanzados.

---


