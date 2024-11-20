import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import serial
import threading
import time

class VoltageMonitorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Voltage Monitor")
        self.master.geometry("400x600")
        self.master.configure(bg="#f5f5f5")

        # Enable resizing
        self.master.resizable(True, True)

        # Set up serial connection (change COM port as needed)
        self.serial_port = serial.Serial('COM3', 9600, timeout=1)  # Replace 'COM3' with your Arduino port
        self.running = False
        self.data_a0 = []
        self.data_a1 = []
        self.time_data = []

        # Header Frame with Centered Title
        header_frame = tk.Frame(master, bg="#f5f5f5", pady=10)
        header_frame.pack(fill=tk.X)
        title_label = tk.Label(header_frame, text="Voltage Monitor", font=("Arial", 16, "bold"), bg="#f5f5f5")
        title_label.pack(side=tk.TOP, pady=10)

        # Control Buttons with Larger Size
        control_frame = tk.Frame(master, bg="#f5f5f5")
        control_frame.pack(fill=tk.X, pady=10)

        self.start_button = tk.Button(control_frame, text="Start", command=self.start_reading, bg="#ffffff", font=("Arial", 14), width=10, height=2)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.stop_button = tk.Button(control_frame, text="Stop", command=self.stop_reading, state=tk.DISABLED, bg="#ffffff", font=("Arial", 14), width=10, height=2)
        self.stop_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Voltage Display
        self.voltage_frame = tk.Frame(master, bg="#f5f5f5")
        self.voltage_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.voltage_a0_label = tk.Label(self.voltage_frame, text="Voltage A0: ", font=("Arial", 25), bg="#f5f5f5")
        self.voltage_a0_label.pack(pady=5)

        self.voltage_a1_label = tk.Label(self.voltage_frame, text="Voltage A1: ", font=("Arial", 25), bg="#f5f5f5")
        self.voltage_a1_label.pack(pady=5)

        # Graph
        self.fig, self.ax = plt.subplots()
        self.ax.set_title("Real-time Voltage Graph")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Voltage (V)")
        self.ax.grid()

        # Embed Matplotlib figure in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Properly close app on window close
        self.master.protocol("WM_DELETE_WINDOW", self.close)

    def read_voltage(self):
        start_time = time.time()
        while self.running:
            if self.serial_port.in_waiting > 0:
                line = self.serial_port.readline()##.decode('utf-8').strip()
                if line:
                    voltages = line.split(',')
                    if len(voltages) == 2:
                        voltage_a0 = float(voltages[0])
                        voltage_a1 = float(voltages[1])

                        # Update voltage labels
                        self.voltage_a0_label.config(text=f"Voltage A0: {voltage_a0:.2f} V")
                        self.voltage_a1_label.config(text=f"Voltage A1: {voltage_a1:.2f} V")

                        # Update data lists for plotting
                        current_time = time.time() - start_time
                        self.time_data.append(current_time)
                        self.data_a0.append(voltage_a0)
                        self.data_a1.append(voltage_a1)

                        # Keep only the latest 20 points to make the graph more responsive
                        if len(self.time_data) > 20:
                            self.time_data.pop(0)
                            self.data_a0.pop(0)
                            self.data_a1.pop(0)

                        # Update plot
                        self.ax.clear()
                        self.ax.plot(self.time_data, self.data_a0, label="Voltage A0", color="blue")
                        self.ax.plot(self.time_data, self.data_a1, label="Voltage A1", color="red")
                        self.ax.set_title("Real-time Voltage Graph")
                        self.ax.set_xlabel("Time (s)")
                        self.ax.set_ylabel("Voltage (V)")
                        self.ax.grid()
                        self.ax.legend()

                        # Draw updated canvas
                        self.canvas.draw()

    def start_reading(self):
        self.running = True
        self.start_button.config(state=tk.DISABLED)  # Disable start button after starting
        self.stop_button.config(state=tk.NORMAL)
        self.thread = threading.Thread(target=self.read_voltage)
        self.thread.start()

    def stop_reading(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)  # Enable start button after stopping
        self.stop_button.config(state=tk.DISABLED)
        self.thread.join()  # Wait for the thread to finish

    def close(self):
        self.running = False
        if self.serial_port.is_open:
            self.serial_port.close()
        self.master.destroy()  # Close the Tkinter window

if __name__ == "__main__":
    root = tk.Tk()
    app = VoltageMonitorApp(root)
    root.mainloop()
