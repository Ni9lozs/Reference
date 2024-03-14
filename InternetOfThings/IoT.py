import random
import time
import tkinter as tk

class SmartLight:
    def __init__(self, device_id):
        self.device_id = device_id
        self.status = False
        self.brightness = 0

    def turn_on(self):
        self.status = True

    def turn_off(self):
        self.status = False

    def set_brightness(self, brightness):
        self.brightness = brightness
        if self.brightness == 0:
            self.status = False
        else: 
            self.status = True

    def randomize_state(self):
        if random.random() < 0.5 or self.brightness == 0:
            self.turn_on()
        else:
            self.turn_off()
        if self.status:    
            self.set_brightness(random.randint(0, 100))
        else:
            self.set_brightness(0)

class Thermostat:
    def __init__(self, device_id):
        self.device_id = device_id
        self.status = False
        self.temperature = 20

    def turn_on(self):
        self.status = True

    def turn_off(self):
        self.status = False

    def set_temperature(self, temperature):
        self.temperature = temperature

    def randomize_state(self):
        if random.random() < 0.5:
            self.turn_on()
        else:
            self.turn_off()
        self.set_temperature(random.randint(15, 30))

class SecurityCamera:
    def __init__(self, device_id):
        self.device_id = device_id
        self.status = False
        self.security_status = "Secure"

    def turn_on(self):
        self.status = True

    def turn_off(self):
        self.status = False

    def set_security_status(self, status):
        self.security_status = status

    def randomize_state(self):
        if random.random() < 0.5:
            self.turn_on()
        else:
            self.turn_off()
        self.set_security_status(random.choice(["Secure", "Intruder Detected"]))

class AutomationSystem:
    def __init__(self):
        self.devices = []

    def discover_device(self, device):
        self.devices.append(device)

    def execute_automation_tasks(self):
        for device in self.devices:
            device.randomize_state()

class MonitoringDashboard:
    def __init__(self, automation_system):
        self.automation_system = automation_system
        self.root = tk.Tk()
        self.root.title("IoT Monitoring Dashboard")

        self.device_status_labels = []

        for device in automation_system.devices:
            device_label = tk.Label(self.root, text=f"{device.__class__.__name__} {device.device_id}: Status - Unknown")
            device_label.pack()
            self.device_status_labels.append(device_label)

        self.smart_light_brightness_label = tk.Label(self.root, text="SmartLight Brightness")
        self.smart_light_brightness_label.pack()
        self.smart_light_brightness_slider = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL)
        self.smart_light_brightness_slider.pack()

        self.thermostat_temperature_label = tk.Label(self.root, text="Thermostat Temperature")
        self.thermostat_temperature_label.pack()
        self.thermostat_temperature_slider = tk.Scale(self.root, from_=15, to=30, orient=tk.HORIZONTAL)
        self.thermostat_temperature_slider.pack()

        update_button = tk.Button(self.root, text="Update Status", command=self.update_status)
        update_button.pack()

    def update_status(self):
        for index, device in enumerate(self.automation_system.devices):
            device.randomize_state()
            status_text = f"{device.__class__.__name__} {device.device_id}: Status - {'On' if device.status else 'Off'}, "
            if hasattr(device, 'brightness'):
                device.set_brightness(self.smart_light_brightness_slider.get())
                status_text += f"Brightness - {device.brightness}%"
            elif hasattr(device, 'temperature'):
                device.set_temperature(self.thermostat_temperature_slider.get())
                status_text += f"Temperature - {device.temperature}°C"
            elif hasattr(device, 'security_status'):
                status_text += f"Security Status - {device.security_status}"

            self.device_status_labels[index].config(text=status_text)

    def run(self):
        self.root.mainloop()

light1 = SmartLight(1)
thermostat1 = Thermostat(2)
camera1 = SecurityCamera(3)

automation_system = AutomationSystem()
automation_system.discover_device(light1)
automation_system.discover_device(thermostat1)
automation_system.discover_device(camera1)

dashboard = MonitoringDashboard(automation_system)
dashboard.run()
