import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time
import threading
import random
from collections import deque
import matplotlib.animation as animation

class SolarMPPTSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Solar MPPT Emergency AC Load Balancing System Simulation")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
        # System parameters
        self.solar_power = 0  # Current solar panel output (W)
        self.battery_voltage = 12.0  # Battery voltage (V)
        self.battery_capacity = 100.0  # Ah
        self.battery_soc = 70.0  # State of charge (%)
        self.mppt_efficiency = 95.0  # MPPT efficiency (%)
        self.inverter_efficiency = 90.0  # Inverter efficiency (%)
        self.ac_load = 500.0  # AC load power (W)
        self.using_inverter = True  # True if using inverter, False if using mains
        self.pwm_timer = 10.0  # PWM timer for switching (seconds)
        self.switch_threshold_low = 30.0  # Battery SOC threshold for switching to mains (%)
        self.switch_threshold_high = 40.0  # Battery SOC threshold for switching back to inverter (%)
        self.sunlight_intensity = 70.0  # Sunlight intensity (%)
        self.sunlight_variability = 20.0  # Sunlight variability (%)
        self.simulation_speed = 1.0  # Simulation speed multiplier
        
        # Data for plotting
        self.time_data = deque(maxlen=600)  # 10 minutes of data at 1 second intervals
        self.battery_data = deque(maxlen=600)
        self.solar_data = deque(maxlen=600)
        self.load_data = deque(maxlen=600)
        self.source_data = deque(maxlen=600)
        
        # Simulation state
        self.running = False
        self.sim_time = 0
        
        # Create the GUI
        self.create_gui()
        
        # Initialize plots
        self.init_plots()
    
    def create_gui(self):
        # Create main frames
        self.control_frame = ttk.Frame(self.root, padding=10)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.display_frame = ttk.Frame(self.root, padding=10)
        self.display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Control panel
        ttk.Label(self.control_frame, text="System Controls", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Battery controls
        ttk.Label(self.control_frame, text="Battery SOC (%):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.battery_soc_var = tk.DoubleVar(value=self.battery_soc)
        ttk.Scale(self.control_frame, from_=0, to=100, variable=self.battery_soc_var, 
                  command=self.update_battery_soc).grid(row=1, column=1, sticky=tk.EW, pady=5)
        self.battery_soc_label = ttk.Label(self.control_frame, text=f"{self.battery_soc:.1f}%")
        self.battery_soc_label.grid(row=1, column=2, sticky=tk.W, pady=5)
        
        # Solar controls
        ttk.Label(self.control_frame, text="Sunlight Intensity (%):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.sunlight_var = tk.DoubleVar(value=self.sunlight_intensity)
        ttk.Scale(self.control_frame, from_=0, to=100, variable=self.sunlight_var, 
                  command=self.update_sunlight).grid(row=2, column=1, sticky=tk.EW, pady=5)
        self.sunlight_label = ttk.Label(self.control_frame, text=f"{self.sunlight_intensity:.1f}%")
        self.sunlight_label.grid(row=2, column=2, sticky=tk.W, pady=5)
        
        ttk.Label(self.control_frame, text="Sunlight Variability (%):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.variability_var = tk.DoubleVar(value=self.sunlight_variability)
        ttk.Scale(self.control_frame, from_=0, to=50, variable=self.variability_var, 
                 command=self.update_variability).grid(row=3, column=1, sticky=tk.EW, pady=5)
        self.variability_label = ttk.Label(self.control_frame, text=f"{self.sunlight_variability:.1f}%")
        self.variability_label.grid(row=3, column=2, sticky=tk.W, pady=5)
        
        # Load controls
        ttk.Label(self.control_frame, text="AC Load (W):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.load_var = tk.DoubleVar(value=self.ac_load)
        ttk.Scale(self.control_frame, from_=0, to=2000, variable=self.load_var, 
                 command=self.update_load).grid(row=4, column=1, sticky=tk.EW, pady=5)
        self.load_label = ttk.Label(self.control_frame, text=f"{self.ac_load:.1f}W")
        self.load_label.grid(row=4, column=2, sticky=tk.W, pady=5)
        
        # MPPT/Switching settings
        ttk.Separator(self.control_frame, orient='horizontal').grid(row=5, column=0, columnspan=3, sticky=tk.EW, pady=10)
        ttk.Label(self.control_frame, text="Switching Controls", font=("Arial", 12, "bold")).grid(row=6, column=0, columnspan=2, pady=5)
        
        ttk.Label(self.control_frame, text="Low Battery Threshold (%):").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.threshold_low_var = tk.DoubleVar(value=self.switch_threshold_low)
        ttk.Scale(self.control_frame, from_=10, to=50, variable=self.threshold_low_var, 
                 command=self.update_threshold_low).grid(row=7, column=1, sticky=tk.EW, pady=5)
        self.threshold_low_label = ttk.Label(self.control_frame, text=f"{self.switch_threshold_low:.1f}%")
        self.threshold_low_label.grid(row=7, column=2, sticky=tk.W, pady=5)
        
        ttk.Label(self.control_frame, text="High Battery Threshold (%):").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.threshold_high_var = tk.DoubleVar(value=self.switch_threshold_high)
        ttk.Scale(self.control_frame, from_=20, to=60, variable=self.threshold_high_var, 
                 command=self.update_threshold_high).grid(row=8, column=1, sticky=tk.EW, pady=5)
        self.threshold_high_label = ttk.Label(self.control_frame, text=f"{self.switch_threshold_high:.1f}%")
        self.threshold_high_label.grid(row=8, column=2, sticky=tk.W, pady=5)
        
        ttk.Label(self.control_frame, text="PWM Timer (s):").grid(row=9, column=0, sticky=tk.W, pady=5)
        self.pwm_timer_var = tk.DoubleVar(value=self.pwm_timer)
        ttk.Scale(self.control_frame, from_=1, to=30, variable=self.pwm_timer_var, 
                 command=self.update_pwm_timer).grid(row=9, column=1, sticky=tk.EW, pady=5)
        self.pwm_timer_label = ttk.Label(self.control_frame, text=f"{self.pwm_timer:.1f}s")
        self.pwm_timer_label.grid(row=9, column=2, sticky=tk.W, pady=5)
        
        # Simulation speed
        ttk.Separator(self.control_frame, orient='horizontal').grid(row=10, column=0, columnspan=3, sticky=tk.EW, pady=10)
        ttk.Label(self.control_frame, text="Simulation Speed:").grid(row=11, column=0, sticky=tk.W, pady=5)
        self.speed_var = tk.DoubleVar(value=self.simulation_speed)
        ttk.Scale(self.control_frame, from_=0.1, to=10, variable=self.speed_var, 
                 command=self.update_speed).grid(row=11, column=1, sticky=tk.EW, pady=5)
        self.speed_label = ttk.Label(self.control_frame, text=f"{self.simulation_speed:.1f}x")
        self.speed_label.grid(row=11, column=2, sticky=tk.W, pady=5)
        
        # System status display
        ttk.Separator(self.control_frame, orient='horizontal').grid(row=12, column=0, columnspan=3, sticky=tk.EW, pady=10)
        ttk.Label(self.control_frame, text="System Status", font=("Arial", 12, "bold")).grid(row=13, column=0, columnspan=2, pady=5)
        
        self.status_frame = ttk.LabelFrame(self.control_frame, text="Current Status")
        self.status_frame.grid(row=14, column=0, columnspan=3, sticky=tk.EW, pady=10, padx=5)
        
        self.power_source_label = ttk.Label(self.status_frame, text="Power Source: Inverter", font=("Arial", 11))
        self.power_source_label.grid(row=0, column=0, sticky=tk.W, pady=2, padx=5)
        
        self.solar_output_label = ttk.Label(self.status_frame, text="Solar Output: 0.0 W", font=("Arial", 11))
        self.solar_output_label.grid(row=1, column=0, sticky=tk.W, pady=2, padx=5)
        
        self.battery_status_label = ttk.Label(self.status_frame, text="Battery: 70.0% (12.0V)", font=("Arial", 11))
        self.battery_status_label.grid(row=2, column=0, sticky=tk.W, pady=2, padx=5)
        
        self.load_status_label = ttk.Label(self.status_frame, text="AC Load: 500.0 W", font=("Arial", 11))
        self.load_status_label.grid(row=3, column=0, sticky=tk.W, pady=2, padx=5)
        
        # Control buttons
        self.button_frame = ttk.Frame(self.control_frame)
        self.button_frame.grid(row=15, column=0, columnspan=3, pady=10)
        
        self.start_button = ttk.Button(self.button_frame, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = ttk.Button(self.button_frame, text="Stop Simulation", command=self.stop_simulation, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5)
        
        self.reset_button = ttk.Button(self.button_frame, text="Reset Simulation", command=self.reset_simulation)
        self.reset_button.grid(row=0, column=2, padx=5)
    
    def init_plots(self):
        # Create figure for plotting
        self.fig = plt.Figure(figsize=(10, 8), dpi=100)
        self.fig.subplots_adjust(hspace=0.4)
        
        # Solar and battery subplot
        self.ax1 = self.fig.add_subplot(3, 1, 1)
        self.ax1.set_title('Battery SOC and Solar Output')
        self.ax1.set_ylabel('Value')
        self.battery_line, = self.ax1.plot([], [], 'b-', label='Battery SOC (%)')
        self.solar_line, = self.ax1.plot([], [], 'y-', label='Solar Output (W)')
        self.ax1.legend(loc='upper left')
        self.ax1.grid(True)
        
        # Load subplot
        self.ax2 = self.fig.add_subplot(3, 1, 2)
        self.ax2.set_title('AC Load')
        self.ax2.set_ylabel('Power (W)')
        self.load_line, = self.ax2.plot([], [], 'g-', label='AC Load (W)')
        self.ax2.legend(loc='upper left')
        self.ax2.grid(True)
        
        # Power source subplot
        self.ax3 = self.fig.add_subplot(3, 1, 3)
        self.ax3.set_title('Power Source')
        self.ax3.set_ylabel('Source')
        self.ax3.set_ylim(-0.5, 1.5)
        self.ax3.set_yticks([0, 1])
        self.ax3.set_yticklabels(['AC Mains', 'Inverter'])
        self.source_line, = self.ax3.plot([], [], 'r-', drawstyle='steps-post')
        self.ax3.grid(True)
        
        for ax in [self.ax1, self.ax2, self.ax3]:
            ax.set_xlabel('Time (s)')
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.display_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    # Update functions for controls
    def update_battery_soc(self, value):
        self.battery_soc = float(value)
        self.battery_soc_label.config(text=f"{self.battery_soc:.1f}%")
        self.update_status_display()
    
    def update_sunlight(self, value):
        self.sunlight_intensity = float(value)
        self.sunlight_label.config(text=f"{self.sunlight_intensity:.1f}%")
        self.update_status_display()
    
    def update_variability(self, value):
        self.sunlight_variability = float(value)
        self.variability_label.config(text=f"{self.sunlight_variability:.1f}%")
    
    def update_load(self, value):
        self.ac_load = float(value)
        self.load_label.config(text=f"{self.ac_load:.1f}W")
        self.update_status_display()
    
    def update_threshold_low(self, value):
        self.switch_threshold_low = float(value)
        self.threshold_low_label.config(text=f"{self.switch_threshold_low:.1f}%")
        if self.switch_threshold_low >= self.switch_threshold_high:
            self.switch_threshold_high = self.switch_threshold_low + 5
            self.threshold_high_var.set(self.switch_threshold_high)
            self.threshold_high_label.config(text=f"{self.switch_threshold_high:.1f}%")
    
    def update_threshold_high(self, value):
        self.switch_threshold_high = float(value)
        self.threshold_high_label.config(text=f"{self.switch_threshold_high:.1f}%")
        if self.switch_threshold_high <= self.switch_threshold_low:
            self.switch_threshold_low = self.switch_threshold_high - 5
            self.threshold_low_var.set(self.switch_threshold_low)
            self.threshold_low_label.config(text=f"{self.switch_threshold_low:.1f}%")
    
    def update_pwm_timer(self, value):
        self.pwm_timer = float(value)
        self.pwm_timer_label.config(text=f"{self.pwm_timer:.1f}s")
    
    def update_speed(self, value):
        self.simulation_speed = float(value)
        self.speed_label.config(text=f"{self.simulation_speed:.1f}x")
    
    def update_status_display(self):
        self.power_source_label.config(text=f"Power Source: {'Inverter' if self.using_inverter else 'AC Mains'}")
        self.solar_output_label.config(text=f"Solar Output: {self.solar_power:.1f} W")
        self.battery_status_label.config(text=f"Battery: {self.battery_soc:.1f}% ({self.battery_voltage:.1f}V)")
        self.load_status_label.config(text=f"AC Load: {self.ac_load:.1f} W")
    
    def start_simulation(self):
        if not self.running:
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            
            # Start simulation thread
            self.sim_thread = threading.Thread(target=self.run_simulation)
            self.sim_thread.daemon = True
            self.sim_thread.start()
            
            # Start animation
            self.ani = animation.FuncAnimation(self.fig, self.update_plot, interval=100)
            self.canvas.draw()
    
    def stop_simulation(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        if hasattr(self, 'ani'):
            self.ani.event_source.stop()
    
    def reset_simulation(self):
        self.stop_simulation()
        
        # Reset data
        self.time_data.clear()
        self.battery_data.clear()
        self.solar_data.clear()
        self.load_data.clear()
        self.source_data.clear()
        
        # Reset simulation time
        self.sim_time = 0
        
        # Reset plots
        for line in [self.battery_line, self.solar_line, self.load_line, self.source_line]:
            line.set_data([], [])
        
        self.canvas.draw()
        self.update_status_display()
    
    def calculate_solar_power(self):
        # Simulate solar panel output based on intensity and variability
        max_solar_power = 1000  # Maximum possible solar power (W)
        base_power = (self.sunlight_intensity / 100) * max_solar_power
        
        # Add variability
        if self.sunlight_variability > 0:
            variability_factor = random.uniform(-self.sunlight_variability, self.sunlight_variability) / 100
            solar_power = base_power * (1 + variability_factor)
        else:
            solar_power = base_power
        
        # Apply MPPT efficiency
        self.solar_power = max(0, solar_power * (self.mppt_efficiency / 100))
        return self.solar_power
    
    def update_battery(self, solar_power, load_power, time_delta):
        # Calculate power balance
        if self.using_inverter:
            # Inverter mode: battery supplies load power
            power_from_battery = load_power / (self.inverter_efficiency / 100)
        else:
            # AC Mains mode: battery doesn't supply load
            power_from_battery = 0
        
        # Calculate net power to battery
        net_power = solar_power - power_from_battery
        
        # Update battery state of charge
        battery_energy_wh = self.battery_capacity * self.battery_voltage
        energy_change_wh = net_power * (time_delta / 3600)  # Convert seconds to hours
        
        # Factor to account for charging efficiency (higher when charging, lower when discharging)
        if net_power > 0:
            efficiency = 0.95  # 95% charging efficiency
        else:
            efficiency = 1.0  # 100% discharging efficiency (already accounted for in inverter)
        
        energy_change_wh *= efficiency
        
        # Update battery energy
        current_energy_wh = (self.battery_soc / 100) * battery_energy_wh
        new_energy_wh = current_energy_wh + energy_change_wh
        
        # Calculate new SOC
        new_soc = (new_energy_wh / battery_energy_wh) * 100
        self.battery_soc = max(0, min(100, new_soc))
        
        # Update battery voltage based on SOC (simplified model)
        if self.battery_soc > 80:
            self.battery_voltage = 12.7 + (self.battery_soc - 80) * 0.03 / 20
        elif self.battery_soc > 50:
            self.battery_voltage = 12.2 + (self.battery_soc - 50) * 0.5 / 30
        elif self.battery_soc > 20:
            self.battery_voltage = 11.8 + (self.battery_soc - 20) * 0.4 / 30
        else:
            self.battery_voltage = 11.0 + (self.battery_soc) * 0.8 / 20
    
    def check_power_switching(self):
        # Check if we need to switch power source based on battery SOC
        if self.using_inverter and self.battery_soc <= self.switch_threshold_low:
            self.using_inverter = False
            self.last_switch_time = self.sim_time
        elif not self.using_inverter and self.battery_soc >= self.switch_threshold_high:
            # Only switch back after PWM timer has elapsed
            if hasattr(self, 'last_switch_time') and (self.sim_time - self.last_switch_time) >= self.pwm_timer:
                self.using_inverter = True
    
    def run_simulation(self):
        last_time = time.time()
        
        while self.running:
            current_time = time.time()
            real_delta = current_time - last_time
            sim_delta = real_delta * self.simulation_speed  # Scale by simulation speed
            
            # Update simulation time
            self.sim_time += sim_delta
            
            # Calculate solar power
            solar_power = self.calculate_solar_power()
            
            # Update battery state
            self.update_battery(solar_power, self.ac_load, sim_delta)
            
            # Check power source switching
            self.check_power_switching()
            
            # Update status display (in main thread)
            self.root.after(0, self.update_status_display)
            
            # Store data for plotting
            self.time_data.append(self.sim_time)
            self.battery_data.append(self.battery_soc)
            self.solar_data.append(solar_power)
            self.load_data.append(self.ac_load)
            self.source_data.append(1 if self.using_inverter else 0)
            
            # Update last time
            last_time = current_time
            
            # Sleep a bit to not overload CPU
            time.sleep(0.05)
    
    def update_plot(self, frame):
        # Update plot data if we have data
        if len(self.time_data) > 0:
            time_array = np.array(self.time_data)
            
            # Update battery and solar lines
            self.battery_line.set_data(time_array, np.array(self.battery_data))
            self.solar_line.set_data(time_array, np.array(self.solar_data))
            
            # Update load line
            self.load_line.set_data(time_array, np.array(self.load_data))
            
            # Update source line
            self.source_line.set_data(time_array, np.array(self.source_data))
            
            # Adjust x-axis limits to show the most recent data (last 120 seconds)
            if max(time_array) > 120:
                x_min = max(time_array) - 120
            else:
                x_min = 0
            x_max = max(time_array) + 5
            
            for ax in [self.ax1, self.ax2, self.ax3]:
                ax.set_xlim(x_min, x_max)
            
            # Adjust y-axis limits for battery and solar
            max_solar = max(np.array(self.solar_data)) if len(self.solar_data) > 0 else 100
            self.ax1.set_ylim(0, max(100, max_solar * 1.1))
            
            # Adjust y-axis limits for load
            max_load = max(np.array(self.load_data)) if len(self.load_data) > 0 else 500
            self.ax2.set_ylim(0, max_load * 1.1)
            
        return self.battery_line, self.solar_line, self.load_line, self.source_line

if __name__ == "__main__":
    root = tk.Tk()
    app = SolarMPPTSimulation(root)
    root.mainloop()
