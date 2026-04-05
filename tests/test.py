import serial
import serial.tools.list_ports
import sys
import time


# ── Detección automática del puerto Arduino ──────────────────────────────────
def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    keywords = ['arduino', 'usb', 'uart', 'serial', 'ch340', 'cp210', 'ftdi']
    for port in ports:
        desc = (port.description + (port.manufacturer or "")).lower()
        if any(k in desc for k in keywords):
            return port.device
    return ports[0].device if ports else None


# ── Lectura del puerto ───────────────────────────────────────────────────────
def read_arduino(port):
    arduino = serial.Serial(port, 9600, timeout=0.1)
    time.sleep(2)
    arduino.reset_input_buffer()
    print(f"Puerto abierto con éxito: {port}")
    return arduino


def main():
    port = find_arduino_port()
    if not port:
        print("Error: No se encontró ningún puerto serie. Conecta el Arduino e intenta de nuevo.")
        sys.exit(1)

    arduino = None
    try:
        arduino = read_arduino(port)
        while True:
            linea = arduino.readline().decode('utf-8', errors='replace').strip()
            if linea:
                print(f"Recibido: {linea}")
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")

    except Exception as e:
        print(f"Error fatal: {e}")

    finally:
        if arduino and arduino.is_open:
            arduino.close()
            print("Puerto cerrado correctamente.")


# ── Punto de entrada ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()