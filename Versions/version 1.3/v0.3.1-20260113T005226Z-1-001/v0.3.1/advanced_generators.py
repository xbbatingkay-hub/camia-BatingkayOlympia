# Advanced Generators with Unique Fix Mechanics
import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import pygame

# Sound setup (will be initialized from main game)
sound1 = None
sound2 = None

# --- Plasma Generator ---
class PlasmaGenerator():
    # High-output generator with "Plasma Stream" minigame for fixing
    def __init__(self, gen_level):
        self.gen_level = gen_level
        self.running = True
        self.off = False
        self.safe_until = 0
        self.start_generating()

    def start_generating(self):
        current_time = time.time()
        
        if self.running:
            if current_time >= self.safe_until:
                if random.random() < 0.08:  # 8% chance to break
                    self.running = False
                    return

            elif False:
                self.off = True
                return

            if self.off:
                self.running = False
                return

            global g, total_g_earned, g_given8
            g += g_given8
            total_g_earned += g_given8
            gain_exp(g_given8)
            try:
                g_label.config(text=f"{g:,.2f}G")
            except:
                pass
            root.after(1000, self.start_generating)

    def lvlup(self):
        global g_given8
        g_given8 = int(g_given8 * 1.35)
        return g_given8

    def mark_fixed(self):
        self.safe_until = time.time() + random.randint(120, 600)
        self.running = True
        self.off = False
        self.start_generating()


# --- Steam Generator (500G/s but breaks easily) ---
class SteamGenerator():
    # Moderate output with high break chance - old rusty equipment
    def __init__(self, gen_level):
        self.gen_level = gen_level
        self.running = True
        self.off = False
        self.safe_until = 0
        self.start_generating()

    def start_generating(self):
        current_time = time.time()
        
        if self.running:
            if current_time >= self.safe_until:
                if random.random() < 0.25:  # 25% chance to break - breaks very easily!
                    self.running = False
                    return

            elif False:
                self.off = True
                return

            if self.off:
                self.running = False
                return

            global g, total_g_earned, g_given11
            g += g_given11
            total_g_earned += g_given11
            gain_exp(g_given11)
            try:
                g_label.config(text=f"{g:,.2f}G")
            except:
                pass
            root.after(1000, self.start_generating)

    def lvlup(self):
        global g_given11
        g_given11 = int(g_given11 * 1.25)
        return g_given11

    def mark_fixed(self):
        self.safe_until = time.time() + random.randint(60, 300)
        self.running = True
        self.off = False
        self.start_generating()


# --- Void Generator ---
class VoidGenerator():
    # Extreme output with "Void Connection" timing minigame
    def __init__(self, gen_level):
        self.gen_level = gen_level
        self.running = True
        self.off = False
        self.safe_until = 0
        self.start_generating()

    def start_generating(self):
        current_time = time.time()
        
        if self.running:
            if current_time >= self.safe_until:
                if random.random() < 0.10:  # 10% chance to break
                    self.running = False
                    return

            elif False:
                self.off = True
                return

            if self.off:
                self.running = False
                return

            global g, total_g_earned, g_given9
            g += g_given9
            total_g_earned += g_given9
            gain_exp(g_given9)
            try:
                g_label.config(text=f"{g:,.2f}G")
            except:
                pass
            root.after(1000, self.start_generating)

    def lvlup(self):
        global g_given9
        g_given9 = int(g_given9 * 1.4)
        return g_given9

    def mark_fixed(self):
        self.safe_until = time.time() + random.randint(180, 600)
        self.running = True
        self.off = False
        self.start_generating()


# --- Chronos Generator ---
class ChronosGenerator():
    # Time-based generator with "Time Dilution" puzzle minigame
    def __init__(self, gen_level):
        self.gen_level = gen_level
        self.running = True
        self.off = False
        self.safe_until = 0
        self.start_generating()

    def start_generating(self):
        current_time = time.time()
        
        if self.running:
            if current_time >= self.safe_until:
                if random.random() < 0.12:  # 12% chance to break
                    self.running = False
                    return

            elif False:
                self.off = True
                return

            if self.off:
                self.running = False
                return

            global g, total_g_earned, g_given10
            g += g_given10
            total_g_earned += g_given10
            gain_exp(g_given10)
            try:
                g_label.config(text=f"{g:,.2f}G")
            except:
                pass
            root.after(1000, self.start_generating)

    def lvlup(self):
        global g_given10
        g_given10 = int(g_given10 * 1.45)
        return g_given10

    def mark_fixed(self):
        self.safe_until = time.time() + random.randint(240, 600)
        self.running = True
        self.off = False
        self.start_generating()


# --- Plasma Fix Minigame ---
def plasma_fix(gen_list_to_fix):
    if not gen_list_to_fix:
        messagebox.showinfo("No Generators", "You have no Plasma generators to fix!")
        return

    clicks_needed = 6
    clicks = [0]
    time_left = [20]

    maint_win = tk.Toplevel(root)
    maint_win.geometry("500x400")
    maint_win.title("Plasma Stream Calibration")
    maint_win.grab_set()

    # Create moving target
    target_x = [250]
    target_y = [200]
    direction = [1, 1]

    def move_target():
        target_x[0] += 5 * direction[0]
        target_y[0] += 5 * direction[1]
        
        if target_x[0] <= 30 or target_x[0] >= 470:
            direction[0] *= -1
        if target_y[0] <= 50 or target_y[0] >= 350:
            direction[1] *= -1
        
        target_button.place(x=target_x[0], y=target_y[0])
        if maint_win.winfo_exists():
            maint_win.after(50, move_target)

    tk.Label(maint_win, text="Hit the plasma stream 6 times to calibrate!", font=("Arial", 12)).pack(pady=10)
    
    progress_bar = ttk.Progressbar(
        maint_win, orient="horizontal", mode="determinate",
        length=300, maximum=clicks_needed
    )
    progress_bar.pack(pady=10)

    timer_label = tk.Label(maint_win, text=f"Time left: {time_left[0]}s", font=("Arial", 12), fg="red")
    timer_label.pack(pady=5)

    def update_timer():
        if clicks[0] >= clicks_needed:
            return
        time_left[0] -= 1
        timer_label.config(text=f"Time left: {time_left[0]}s")
        if time_left[0] <= 0:
            maint_win.destroy()
        else:
            maint_win.after(1000, update_timer)

    def on_correct_click():
        if sound1:
            sound1.play()
        clicks[0] += 1
        progress_bar['value'] = clicks[0]
        if clicks[0] >= clicks_needed:
            for gobj in gen_list_to_fix:
                gobj.running = True
                gobj.off = False
                gobj.mark_fixed()
                gobj.start_generating()
            try:
                gen_update()
            except:
                pass
            maint_win.destroy()
        else:
            # Change direction on hit
            direction[0] *= -1
            direction[1] *= -1

    target_button = tk.Button(maint_win, text="●", font=("Arial", 20), bg="cyan", fg="blue",
                             command=on_correct_click, width=3, height=1)
    target_button.place(x=target_x[0], y=target_y[0])
    
    move_target()
    update_timer()


# --- Void Connection Fix Minigame ---
def void_fix(gen_list_to_fix):
    if not gen_list_to_fix:
        messagebox.showinfo("No Generators", "You have no Void generators to fix!")
        return

    success_needed = 5
    success = [0]
    time_left = [25]

    maint_win = tk.Toplevel(root)
    maint_win.geometry("450x350")
    maint_win.title("Void Connection")
    maint_win.grab_set()

    timer_label = tk.Label(
        maint_win,
        text=f"Time left: {time_left[0]}s",
        font=("Arial", 12),
        fg="purple"
    )
    timer_label.pack(pady=(10, 5))

    tk.Label(
        maint_win,
        text="Hold SPACE when indicator is in the green zone!",
        font=("Arial", 11)
    ).pack(pady=(5, 10))

    # Indicator bar
    indicator_frame = tk.Frame(maint_win, width=300, height=30, bg="black")
    indicator_frame.pack(pady=10)
    indicator_frame.pack_propagate(False)

    # Green zone
    green_start = random.randint(100, 180)
    green_width = 60
    green_zone = tk.Frame(indicator_frame, width=green_width, height=30, bg="green")
    green_zone.place(x=green_start, y=0)

    # Moving indicator
    indicator = tk.Frame(indicator_frame, width=5, height=30, bg="white")
    indicator.place(x=0, y=0)

    indicator_pos = [0]
    indicator_direction = [1]
    indicator_speed = 4

    def move_indicator():
        indicator_pos[0] += indicator_speed * indicator_direction[0]
        if indicator_pos[0] >= 295:
            indicator_direction[0] = -1
        elif indicator_pos[0] <= 0:
            indicator_direction[0] = 1
        indicator.place(x=indicator_pos[0], y=0)
        if maint_win.winfo_exists():
            maint_win.after(30, move_indicator)

    def check_hold(event):
        if indicator_pos[0] >= green_start and indicator_pos[0] <= green_start + green_width:
            success[0] += 1
            success_label.config(text=f"Connections: {success[0]}/{success_needed}")
            if success[0] >= success_needed:
                for gobj in gen_list_to_fix:
                    gobj.running = True
                    gobj.off = False
                    gobj.mark_fixed()
                    gobj.start_generating()
                try:
                    gen_update()
                except:
                    pass
                maint_win.destroy()

    def update_timer():
        if success[0] >= success_needed:
            return
        time_left[0] -= 1
        timer_label.config(text=f"Time left: {time_left[0]}s")
        if time_left[0] <= 0:
            messagebox.showerror('Connection Lost', 'Void connection failed!')
            maint_win.destroy()
        else:
            maint_win.after(1000, update_timer)

    success_label = tk.Label(maint_win, text=f"Connections: {success[0]}/{success_needed}", font=("Arial", 12))
    success_label.pack(pady=10)

    maint_win.bind('<KeyRelease-space>', check_hold)
    
    move_indicator()
    update_timer()


# --- Chronos Time Dilution Fix Minigame ---
def chronos_fix(gen_list_to_fix):
    if not gen_list_to_fix:
        messagebox.showinfo("No Generators", "You have no Chronos generators to fix!")
        return

    puzzles_needed = 4
    solved = [0]
    time_left = [30]

    maint_win = tk.Toplevel(root)
    maint_win.geometry("500x450")
    maint_win.title("Time Dilution Puzzle")
    maint_win.grab_set()

    # Generate 4 unique time-based puzzles
    puzzles = []
    for i in range(puzzles_needed):
        puzzle = {
            "target": random.randint(5, 12),
            "options": sorted(random.sample(range(2, 15), 4)),
            "solved": False
        }
        puzzles.append(puzzle)

    def create_puzzle_widgets(puzzle_idx):
        # Clear previous puzzle
        for widget in puzzle_frame.winfo_children():
            widget.destroy()
        
        if puzzle_idx >= puzzles_needed:
            # All puzzles solved!
            for gobj in gen_list_to_fix:
                gobj.running = True
                gobj.off = False
                gobj.mark_fixed()
                gobj.start_generating()
            try:
                gen_update()
            except:
                pass
            messagebox.showinfo("Success!", "Time dilution complete! Generators restored.")
            maint_win.destroy()
            return

        puzzle = puzzles[puzzle_idx]
        
        tk.Label(puzzle_frame, text=f"Puzzle {puzzle_idx + 1}/{puzzles_needed}", 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(puzzle_frame, text=f"What is {puzzle['target']} × 3 - {puzzle['target']}?", 
                font=("Arial", 12)).pack(pady=10)
        
        def check_answer(answer):
            correct = puzzle["target"] * 2
            if answer == correct:
                solved[0] += 1
                puzzles[puzzle_idx]["solved"] = True
                create_puzzle_widgets(puzzle_idx + 1)
            else:
                messagebox.showerror("Wrong!", "Time dilates... Try again!")
                time_left[0] -= 5
                timer_label.config(text=f"Time left: {time_left[0]}s")

        for opt in puzzle["options"]:
            ttk.Button(puzzle_frame, text=str(opt), 
                      command=lambda a=opt: check_answer(a)).pack(side="left", padx=5, pady=10)

    puzzle_frame = tk.Frame(maint_win)
    puzzle_frame.pack(pady=10)

    timer_label = tk.Label(maint_win, text=f"Time left: {time_left[0]}s", font=("Arial", 12), fg="dark blue")
    timer_label.pack(pady=10)

    def update_timer():
        if solved[0] >= puzzles_needed:
            return
        time_left[0] -= 1
        timer_label.config(text=f"Time left: {time_left[0]}s")
        if time_left[0] <= 0:
            messagebox.showerror('Temporal Failure', 'Time dilation failed! Generators remain broken.')
            maint_win.destroy()
        else:
            maint_win.after(1000, update_timer)

    create_puzzle_widgets(0)
    update_timer()


# Advanced Generator Variables
plasma_price = 50000
plasma_shop_amnt = 1
plasma_amnt = 0
plasma_list = []
g_given8 = 2500  # Produces 2500G/s
gen_lvl8 = 1
upgrade_cost8 = 50000
plasma_stock = 1

void_price = 200000
void_shop_amnt = 1
void_amnt = 0
void_list = []
g_given9 = 10000  # Produces 10000G/s
gen_lvl9 = 1
upgrade_cost9 = 200000
void_stock = 1

chronos_price = 1000000
chronos_shop_amnt = 1
chronos_amnt = 0
chronos_list = []
g_given10 = 50000  # Produces 50000G/s
gen_lvl10 = 1
upgrade_cost10 = 1000000
chronos_stock = 1

# --- Steam Generator Variables (500G/s but breaks easily) ---
steam_price = 5000
steam_shop_amnt = 1
steam_amnt = 0
steam_list = []
g_given11 = 500  # Produces 500G/s
gen_lvl11 = 1
upgrade_cost11 = 5000
steam_stock = 10  # More common, can stock up

# Placeholder functions (will be connected to main game)
def set_sounds(s_sound1, s_sound2, s_root, s_gen_update=None, s_gain_exp=None, s_g_label=None):
    global sound1, sound2, root, gen_update, gain_exp, g_label
    sound1 = s_sound1
    sound2 = s_sound2
    root = s_root
    # These may be None if called before they're defined
    gen_update = s_gen_update
    gain_exp = s_gain_exp
    g_label = s_g_label

# Function to update references after main game loads
def update_references(s_gen_update, s_gain_exp, s_g_label):
    global gen_update, gain_exp, g_label
    gen_update = s_gen_update
    gain_exp = s_gain_exp
    g_label = s_g_label
