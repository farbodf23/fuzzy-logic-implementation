import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tkinter as tk
from tkinter import ttk, messagebox

plt.rcParams['font.family'] = 'DejaVu Sans'


cars = ctrl.Antecedent(np.arange(0, 51, 1), 'cars')
waiting_time = ctrl.Antecedent(np.arange(0, 301, 1), 'waiting_time')
green_time = ctrl.Consequent(np.arange(10, 121, 1), 'green_time')

cars['low'] = fuzz.trimf(cars.universe, [0, 0, 20])
cars['medium'] = fuzz.trimf(cars.universe, [10, 25, 40])
cars['high'] = fuzz.trapmf(cars.universe, [30, 40, 50, 50])

waiting_time['short'] = fuzz.trimf(waiting_time.universe, [0, 0, 100])
waiting_time['medium'] = fuzz.trimf(waiting_time.universe, [60, 150, 240])
waiting_time['long'] = fuzz.trapmf(waiting_time.universe, [180, 240, 300, 300])

green_time['very_short'] = fuzz.trimf(green_time.universe, [10, 15, 30])
green_time['short'] = fuzz.trimf(green_time.universe, [25, 40, 60])
green_time['medium'] = fuzz.trimf(green_time.universe, [50, 70, 90])
green_time['long'] = fuzz.trimf(green_time.universe, [80, 100, 110])
green_time['very_long'] = fuzz.trapmf(green_time.universe, [100, 110, 120, 120])

rules = [
    ctrl.Rule(cars['low'] & waiting_time['short'], green_time['very_short']),
    ctrl.Rule(cars['low'] & waiting_time['medium'], green_time['short']),
    ctrl.Rule(cars['low'] & waiting_time['long'], green_time['medium']),
    ctrl.Rule(cars['medium'] & waiting_time['short'], green_time['short']),
    ctrl.Rule(cars['medium'] & waiting_time['medium'], green_time['medium']),
    ctrl.Rule(cars['medium'] & waiting_time['long'], green_time['long']),
    ctrl.Rule(cars['high'] & waiting_time['short'], green_time['long']),
    ctrl.Rule(cars['high'] & waiting_time['medium'], green_time['very_long']),
    ctrl.Rule(cars['high'] & waiting_time['long'], green_time['very_long']),
]

traffic_ctrl = ctrl.ControlSystem(rules)

def get_antecedent_label(value, antecedent):
    max_label, max_mu = None, 0
    for label in antecedent.terms:
        mu = fuzz.interp_membership(antecedent.universe, antecedent[label].mf, value)
        if mu > max_mu:
            max_mu, max_label = mu, label
    return max_label

def calculate_fuzzy_cycle():
    try:
        prio = {
            'N': float(cars_n_var.get()) + 0.01 * float(wt_n_var.get()),
            'S': float(cars_s_var.get()) + 0.01 * float(wt_s_var.get()),
            'E': float(cars_e_var.get()) + 0.01 * float(wt_e_var.get()),
            'W': float(cars_w_var.get()) + 0.01 * float(wt_w_var.get())
        }
        
        dirs = [('North', 'N'), ('South', 'S'), ('East', 'E'), ('West', 'W')]
        sorted_dirs = sorted(dirs, key=lambda x: prio[x[1]], reverse=True)
        
        cycle_data = []
        total_cycle = 0
        
        var_map = {'N': (cars_n_var, wt_n_var), 'S': (cars_s_var, wt_s_var), 
                  'E': (cars_e_var, wt_e_var), 'W': (cars_w_var, wt_w_var)}
        
        for rank, (dir_name, dir_key) in enumerate(sorted_dirs, 1):
            c_var, w_var = var_map[dir_key]
            cars_val = float(c_var.get())
            wt_val = float(w_var.get())
            
            sim = ctrl.ControlSystemSimulation(traffic_ctrl)
            sim.input['cars'] = cars_val
            sim.input['waiting_time'] = wt_val
            sim.compute()
            
            gt_val = max(20, sim.output['green_time'])
            cars_label = get_antecedent_label(cars_val, cars)
            wt_label = get_antecedent_label(wt_val, waiting_time)
            gt_label = get_antecedent_label(gt_val, green_time)
            
            cycle_data.append((rank, dir_name, cars_label, wt_label, gt_label, gt_val))
            total_cycle += gt_val
        
        show_clean_output(cycle_data, total_cycle)
        
    except:
        messagebox.showerror("Error", "Enter valid numbers")

def show_clean_output(cycle_data, total_cycle):
    output = "\n"
    output += "=" * 60 + "\n"
    output += "          FUZZY TRAFFIC CYCLE PLAN              \n"
    output += "=" * 60 + "\n\n"
    
    output += f"{'Rank':<4} {'Direction':<8} {'Status':<20} {'Green':<12}\n"
    output += "-" * 60 + "\n"
    
    for rank, dir_name, cars_label, wt_label, gt_label, gt in cycle_data:
        status = f"{cars_label} cars, {wt_label} wait"
        output += f"{rank:<4}  {dir_name:<8}  {status:<20}  {gt_label} ({gt:.0f}s)\n"
    
    output += "-" * 60 + "\n"
    output += f"{'Total Cycle Time:':<35} {total_cycle:.0f} seconds\n"
    output += "=" * 60 + "\n"
    
    messagebox.showinfo("Fuzzy Cycle Plan", output)

def show_beautiful_graphic(cycle_data):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    circle = patches.Circle((0.5, 0.5), 0.4, color='lightgray', ec='black', lw=2)
    ax1.add_patch(circle)
    
    colors = ['limegreen', 'darkred', 'darkred', 'darkred']
    labels = ['N', 'S', 'E', 'W']
    angles = [90, 270, 0, 180]
    
    for i in range(4):
        angle = np.deg2rad(angles[i])
        x = 0.5 + 0.3 * np.cos(angle)
        y = 0.5 + 0.3 * np.sin(angle)
        rank = cycle_data[i][0] if i < len(cycle_data) else ""
        ax1.scatter(x, y, c=colors[i], s=1200, ec='black', lw=3)
        ax1.text(x, y, labels[i], ha='center', va='center', fontweight='bold', fontsize=16, color='white')
        if rank:
            ax1.text(x, y-0.22, str(rank), ha='center', fontsize=14, fontweight='bold', color='black')
    
    ax1.set_xlim(0,1); ax1.set_ylim(0,1); ax1.set_aspect('equal')
    ax1.set_title("Traffic Priority Circle", fontweight='bold', fontsize=14)
    ax1.axis('off')
    
    ranks = [d[0] for d in cycle_data]
    gts = [d[5] for d in cycle_data]
    bars = ax2.bar(ranks, gts, color=['lime', 'green', 'orange', 'red'], alpha=0.8, width=0.5)
    ax2.set_xlabel('Priority Rank'); ax2.set_ylabel('Green Time (s)')
    ax2.set_title('Green Time Timeline', fontweight='bold', fontsize=14)
    
    for bar, (_, dir_name, _, _, gt_label, gt) in zip(bars, cycle_data):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1, gt_label, 
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.tight_layout()
    plt.show()

def show_plot(var):
    var.view()
    plt.show()

# GUI
root = tk.Tk()
root.title("Fuzzy Traffic Light")
root.geometry("700x650")
root.configure(bg="#0f0f23")

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#0f0f23", foreground="#e0e0ff")
style.configure("Dark.TButton", background="#1a1a3a", foreground="white", font=("Arial", 11, "bold"))
style.map("Dark.TButton", background=[("active", "#4a5a9a")])

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=15, pady=15)

tab1 = tk.Frame(notebook, bg="#0f0f23")
notebook.add(tab1, text="Inputs")

frame = tk.Frame(tab1, bg="#0f0f23")
frame.place(relx=0.5, rely=0.5, anchor="center")

cars_n_var = tk.StringVar(value="12"); wt_n_var = tk.StringVar(value="90")
cars_s_var = tk.StringVar(value="28"); wt_s_var = tk.StringVar(value="150")
cars_e_var = tk.StringVar(value="5"); wt_e_var = tk.StringVar(value="40")
cars_w_var = tk.StringVar(value="42"); wt_w_var = tk.StringVar(value="250")

entries = [
    (cars_n_var, wt_n_var, "North"), 
    (cars_s_var, wt_s_var, "South"),
    (cars_w_var, wt_w_var, "West"), 
    (cars_e_var, wt_e_var, "East")
]

for i, (c_var, w_var, label) in enumerate(entries):
    row = i * 3
    ttk.Label(frame, text=label, font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, pady=10)
    ttk.Label(frame, text="Cars:").grid(row=row+1, column=0, sticky="e")
    ttk.Entry(frame, textvariable=c_var, width=10).grid(row=row+1, column=1, padx=5)
    ttk.Label(frame, text="Wait(s):").grid(row=row+2, column=0, sticky="e")
    ttk.Entry(frame, textvariable=w_var, width=10).grid(row=row+2, column=1, padx=5)

ttk.Button(frame, text="Calculate Fuzzy Cycle", style="Dark.TButton", command=calculate_fuzzy_cycle).grid(row=12, column=0, columnspan=3, pady=30)

tab2 = tk.Frame(notebook, bg="#0f0f23")
notebook.add(tab2, text="Fuzzy Plots")

btn_frame = tk.Frame(tab2, bg="#0f0f23")
btn_frame.place(relx=0.5, rely=0.5, anchor="center")

ttk.Button(btn_frame, text="Cars MF", style="Dark.TButton", command=lambda: show_plot(cars)).pack(pady=15, fill="x")
ttk.Button(btn_frame, text="Waiting Time MF", style="Dark.TButton", command=lambda: show_plot(waiting_time)).pack(pady=15, fill="x")
ttk.Button(btn_frame, text="Green Time MF", style="Dark.TButton", command=lambda: show_plot(green_time)).pack(pady=15, fill="x")

root.mainloop()