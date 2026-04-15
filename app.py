import tkinter as tk
from tkinter import ttk, messagebox
import random
import threading
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class SmartAIIrrigationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart AI Irrigation System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0f172a')
        
        # Dark theme colors
        self.colors = {
            'bg': '#0f172a',
            'card': 'rgba(255,255,255,0.1)',
            'green': '#10b981',
            'blue': '#3b82f6',
            'text': '#f8fafc',
            'secondary': '#cbd5e1'
        }
        
        # Sensor data
        self.sensors = {
            'soil_moisture': 50,
            'temperature': 25,
            'water_level': 70,
            'rain_prob': 30
        }
        
        self.crop_methods = {
            'Rice': 'Flood Irrigation',
            'Wheat': 'Drip Irrigation',
            'Maize': 'Sprinkler',
            'Cotton': 'Drip Irrigation'
        }
        
        self.logged_in = False
        self.current_crop = 'Rice'
        
        self.setup_ui()
        
    def setup_ui(self):
        # Login Frame
        self.login_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.login_frame.pack(fill='both', expand=True)
        
        title_label = tk.Label(self.login_frame, text="Smart AI Irrigation", 
                              font=('Segoe UI', 36, 'bold'),
                              fg='#10b981', bg=self.colors['bg'])
        title_label.pack(pady=50)
        
        subtitle_label = tk.Label(self.login_frame, 
                                 text="Intelligent Farm Management System",
                                 font=('Segoe UI', 14), fg=self.colors['secondary'],
                                 bg=self.colors['bg'])
        subtitle_label.pack(pady=10)
        
        login_btn = tk.Button(self.login_frame, text="Continue with Google",
                             font=('Segoe UI', 14, 'bold'), bg='#4285f4',
                             fg='white', command=self.login,
                             relief='flat', padx=40, pady=15)
        login_btn.pack(pady=30)
        
        # Dashboard Frame (hidden initially)
        self.dashboard_frame = tk.Frame(self.root, bg=self.colors['bg'])
        
    def login(self):
        self.logged_in = True
        self.login_frame.destroy()
        self.create_dashboard()
        
    def create_dashboard(self):
        # Header
        header_frame = tk.Frame(self.dashboard_frame, bg=self.colors['bg'])
        header_frame.pack(fill='x', padx=20, pady=20)
        
        title_label = tk.Label(header_frame, text="Smart Irrigation Dashboard",
                              font=('Segoe UI', 24, 'bold'), fg='#10b981',
                              bg=self.colors['bg'])
        title_label.pack(side='left')
        
        profile_btn = tk.Button(header_frame, text="Logout", command=self.logout,
                               bg='#ef4444', fg='white', font=('Segoe UI', 10, 'bold'),
                               relief='flat', padx=20)
        profile_btn.pack(side='right')
        
        # Metrics Grid
        metrics_frame = tk.Frame(self.dashboard_frame, bg=self.colors['bg'])
        metrics_frame.pack(fill='x', padx=20, pady=10)
        
        self.metric_labels = {}
        metrics = [
            ('Soil Moisture', 'soil_moisture', '%', 'fas fa-tint', '#10b981'),
            ('Temperature', 'temperature', '°C', 'fas fa-thermometer-half', '#f59e0b'),
            ('Water Level', 'water_level', '%', 'fas fa-water', '#3b82f6'),
            ('Rain Probability', 'rain_prob', '%', 'fas fa-cloud-rain', '#8b5cf6')
        ]
        
        for i, (name, key, unit, icon, color) in enumerate(metrics):
            frame = tk.Frame(metrics_frame, bg='rgba(255,255,255,0.1)', relief='solid', bd=1)
            frame.grid(row=0, column=i, padx=10, pady=10, sticky='nsew')
            frame.configure(width=250, height=150)
            
            tk.Label(frame, text=name, font=('Segoe UI', 10), fg=self.colors['secondary'],
                    bg='rgba(255,255,255,0.1)').pack(pady=5)
            self.metric_labels[key] = tk.Label(frame, text="0", font=('Segoe UI', 36, 'bold'),
                                              fg=color, bg='rgba(255,255,255,0.1)')
            self.metric_labels[key].pack(pady=10)
        
        metrics_frame.grid_columnconfigure(0, weight=1)
        metrics_frame.grid_columnconfigure(1, weight=1)
        metrics_frame.grid_columnconfigure(2, weight=1)
        metrics_frame.grid_columnconfigure(3, weight=1)
        
        # AI Decision
        decision_frame = tk.LabelFrame(self.dashboard_frame, text="AI Irrigation Decision",
                                      font=('Segoe UI', 12, 'bold'), fg='#10b981',
                                      bg=self.colors['bg'], relief='flat')
        decision_frame.pack(fill='x', padx=20, pady=20)
        
        self.decision_label = tk.Label(decision_frame, text="Loading...", 
                                      font=('Segoe UI', 20, 'bold'),
                                      bg='rgba(16,185,129,0.2)', fg='#10b981',
                                      relief='solid', bd=2, pady=20)
        self.decision_label.pack(pady=20)
        
        self.reason_label = tk.Label(decision_frame, text="", 
                                    font=('Segoe UI', 12), fg=self.colors['secondary'],
                                    bg=self.colors['bg'])
        self.reason_label.pack()
        
        # Controls Row
        controls_frame = tk.Frame(self.dashboard_frame, bg=self.colors['bg'])
        controls_frame.pack(fill='x', padx=20, pady=10)
        
        # Crop Selection
        crop_frame = tk.LabelFrame(controls_frame, text="Crop Selection",
                                  font=('Segoe UI', 10, 'bold'), fg='#10b981',
                                  bg=self.colors['bg'], relief='flat')
        crop_frame.pack(side='left', fill='both', expand=True, padx=(0,10))
        
        tk.Label(crop_frame, text="Crop Type:", font=('Segoe UI', 10, 'bold'),
                fg=self.colors['text'], bg=self.colors['bg']).pack(anchor='w', padx=10, pady=5)
        self.crop_var = tk.StringVar(value='Rice')
        crop_menu = ttk.Combobox(crop_frame, textvariable=self.crop_var,
                                values=list(self.crop_methods.keys()),
                                state='readonly', font=('Segoe UI', 11))
        crop_menu.pack(padx=10, pady=5, fill='x')
        crop_menu.bind('<<ComboboxSelected>>', self.update_crop_method)
        
        self.method_label = tk.Label(crop_frame, text="Recommended: Flood Irrigation",
                                    font=('Segoe UI', 12, 'bold'), fg='#10b981',
                                    bg=self.colors['bg'])
        self.method_label.pack(pady=5)
        
        # Charts Frame
        charts_frame = tk.Frame(self.dashboard_frame, bg=self.colors['bg'])
        charts_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Moisture Chart
        fig1, ax1 = plt.subplots(figsize=(6, 3), facecolor=self.colors['bg'])
        ax1.set_facecolor(self.colors['bg'])
        self.moisture_line, = ax1.plot([], [], 'o-', color='#10b981', linewidth=3, markersize=8)
        ax1.set_title('Soil Moisture Trend (Last 5 Days)', color='white', fontsize=12, pad=20)
        ax1.set_ylabel('Moisture %', color='white')
        ax1.tick_params(colors='white')
        ax1.grid(True, alpha=0.3)
        self.moisture_canvas = FigureCanvasTkAgg(fig1, charts_frame)
        self.moisture_canvas.get_tk_widget().pack(side='left', fill='both', expand=True, padx=(0,10))
        
        # Water Usage Chart
        fig2, ax2 = plt.subplots(figsize=(6, 3), facecolor=self.colors['bg'])
        ax2.set_facecolor(self.colors['bg'])
        self.water_bars1 = ax2.bar([], [], color='#3b82f6', alpha=0.7, label='Used')
        self.water_bars2 = ax2.bar([], [], color='#10b981', alpha=0.7, label='Saved')
        ax2.set_title('Water Usage vs Saved', color='white', fontsize=12, pad=20)
        ax2.set_ylabel('Liters', color='white')
        ax2.tick_params(colors='white')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        self.water_canvas = FigureCanvasTkAgg(fig2, charts_frame)
        self.water_canvas.get_tk_widget().pack(side='right', fill='both', expand=True)
        
        self.dashboard_frame.pack(fill='both', expand=True)
        
        # Start sensor simulation
        self.moisture_data = [45, 52, 48, 55, 62]
        self.water_used = [120, 110, 95, 105, 88]
        self.water_saved = [30, 35, 42, 38, 45]
        
        self.update_display()
        self.sensor_thread = threading.Thread(target=self.simulate_sensors, daemon=True)
        self.sensor_thread.start()
        
    def logout(self):
        self.dashboard_frame.destroy()
        self.setup_ui()
        
    def simulate_sensors(self):
        while True:
            self.sensors['soil_moisture'] = max(10, min(95, self.sensors['soil_moisture'] + (random.random() - 0.5) * 8))
            self.sensors['temperature'] = max(15, min(45, self.sensors['temperature'] + (random.random() - 0.5) * 3))
            self.sensors['water_level'] = max(20, min(100, self.sensors['water_level'] + (random.random() - 0.5) * 5))
            self.sensors['rain_prob'] = max(0, min(100, self.sensors['rain_prob'] + (random.random() - 0.5) * 15))
            
            self.root.after(0, self.update_display)
            time.sleep(2.5)
            
    def update_display(self):
        # Update metrics
        for key, label in self.metric_labels.items():
            value = self.sensors[key]
            label.config(text=f"{value:.0f}{'%' if key != 'temperature' else '°C'}")
        
        # Update AI decision
        self.update_ai_decision()
        
        # Update charts
        self.update_charts()
        
    def update_ai_decision(self):
        soil = self.sensors['soil_moisture']
        rain = self.sensors['rain_prob']
        
        if soil < 30 and rain < 40:
            status = "🚿 IRRIGATION ON"
            color = '#10b981'
            reason = "Low soil moisture and minimal rain expected"
        elif rain > 60:
            status = "⛔ IRRIGATION OFF"
            color = '#ef4444'
            reason = "High rain probability detected"
        else:
            status = "⚖️ Moderate Irrigation"
            color = '#f59e0b'
            reason = "Optimal conditions - conserving water"
        
        self.decision_label.config(text=status, fg=color)
        self.reason_label.config(text=reason)
        
    def update_crop_method(self, event=None):
        crop = self.crop_var.get()
        method = self.crop_methods[crop]
        self.method_label.config(text=f"Recommended: {method}")
        
    def update_charts(self):
        # Moisture chart
        self.moisture_data.append(self.sensors['soil_moisture'])
        if len(self.moisture_data) > 5:
            self.moisture_data.pop(0)
        self.moisture_line.set_data(range(len(self.moisture_data)), self.moisture_data)
        ax1 = self.moisture_canvas.figure.axes[0]
        ax1.set_xlim(0, len(self.moisture_data)-1)
        ax1.set_ylim(0, 100)
        self.moisture_canvas.draw()
        
        # Water chart
        self.water_used.append(random.randint(80, 130))
        self.water_saved.append(random.randint(25, 50))
        if len(self.water_used) > 5:
            self.water_used.pop(0)
            self.water_saved.pop(0)
            
        ax2 = self.water_canvas.figure.axes[0]
        x = range(len(self.water_used))
        self.water_bars1 = ax2.bar(x, self.water_used, color='#3b82f6', alpha=0.7, label='Used')
        self.water_bars2 = ax2.bar(x, self.water_saved, color='#10b981', alpha=0.7, label='Saved')
        ax2.set_xlim(-0.5, len(self.water_used)-0.5)
        self.water_canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartAIIrrigationSystem(root)
    root.mainloop()
