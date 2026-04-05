import serial
import serial.tools.list_ports
import json
import sys
import os
from tkinter import *
from tkinter import messagebox
import time


# ── Detección automática del puerto Arduino ──────────────────────────────────
def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    keywords = ['arduino', 'usb', 'uart', 'serial', 'ch340', 'cp210', 'ftdi']
    for port in ports:
        desc = (port.description + port.manufacturer if port.manufacturer else port.description).lower()
        if any(k in desc for k in keywords):
            return port.device
    return ports[0].device if ports else None


def connect_arduino():
    port = find_arduino_port()
    if not port:
        messagebox.showerror("Error", "No se encontró ningún puerto serie.\nConecta el Arduino e intenta de nuevo.")
        sys.exit(1)
    try:
        conn = serial.Serial(port, 9600, timeout=0.1)
        time.sleep(2)
        conn.reset_input_buffer()
        return conn, port
    except serial.SerialException as e:
        messagebox.showerror("Error de puerto", f"No se pudo abrir {port}:\n{e}")
        sys.exit(1)


# ── Rutas multiplataforma ────────────────────────────────────────────────────
def img_path(filename):
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "images", filename)


# ── Aplicación principal ─────────────────────────────────────────────────────
class ArduinoApp:
    def __init__(self, root, arduino, port):
        self.root    = root
        self.arduino = arduino

        self.root.title("Comunicación con Arduino - Proyecto Final")
        self.root.geometry("850x650")
        self.root.config(bg="white")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self._build_ui(port)
        self._load_images()
        self.update_label()

    def _build_ui(self, port):
        self.frame = Frame(self.root, bg="white")
        self.frame.pack(fill="both", expand=True)

        self.status_label = Label(
            self.frame,
            text=f"Conectado en {port}\nEsperando datos...",
            font=("Arial", 20),
            bg="white"
        )
        self.status_label.pack(pady=20)

    def _load_images(self):
        try:
            self.img1 = PhotoImage(file=img_path("1.png"))
            self.img2 = PhotoImage(file=img_path("2.png"))
            self.img3 = PhotoImage(file=img_path("3.png"))
            self.img4 = PhotoImage(file=img_path("4.png"))

            self.img_labels = {
                1: Label(self.frame, image=self.img1, bg="white"),
                2: Label(self.frame, image=self.img2, bg="white"),
                3: Label(self.frame, image=self.img3, bg="white"),
                4: Label(self.frame, image=self.img4, bg="white"),
            }
        except TclError:
            messagebox.showwarning(
                "Imágenes no encontradas",
                f"No se hallaron los .png en:\n{img_path('')}"
            )
            sys.exit(1)

    def update_label(self):
        try:
            linea = self.arduino.readline().decode('utf-8', errors='replace').rstrip()
            if linea:
                try:
                    obj           = json.loads(linea)
                    distancia     = obj["distancia"]
                    etiqueta      = obj["etiqueta"]
                    key           = obj["key"]

                    for lbl in self.img_labels.values():
                        lbl.pack_forget()

                    nombres = {1: "Cerca", 2: "Medio-cerca", 3: "Normal", 4: "Lejos"}
                    if key in self.img_labels:
                        self.img_labels[key].pack()
                        etiqueta = nombres.get(key, etiqueta)

                    self.status_label.config(text=f"{distancia} cms.\n{etiqueta}")

                except (ValueError, json.JSONDecodeError):
                    print(f"Dato no válido: {linea}")

        except Exception as e:
            print(f"Error en la lectura: {e}")

        self.root.after(100, self.update_label)

    def on_close(self):
        if self.arduino.is_open:
            self.arduino.close()
        self.root.destroy()


# ── Punto de entrada ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    arduino, port = connect_arduino()

    root = Tk()
    app  = ArduinoApp(root, arduino, port)
    root.mainloop()