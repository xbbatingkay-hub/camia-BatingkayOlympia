# Import libraries for GUI, utilities, and audio
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sv_ttk  # For modern theme
import random
import json
import os
import pygame
import time
from datetime import datetime, timedelta
from random_popups import PopupManager
from advanced_generators import *  # Import advanced generators
clicky = 0
# Player Stats Variables
total_g_earned = 0
total_clicks = 0
total_generators_owned = 0

# Rotating upgrades system
upgrade_rotation_timer = 600  # 10 minutes in seconds
next_rotation_time = 0
current_rotation_index = 0

# Define possible rotating upgrades
rotating_upgrades = [
    {"name": "Music Player Unlock", "cost": 5000, "effect": "Unlock the custom music player feature", "duration": 0},
    {"name": "Click Multiplier x2", "cost": 500, "effect": "Double click power for 5 minutes", "duration": 300},
    {"name": "Generator Boost", "cost": 1000, "effect": "All generators produce 2x for 3 minutes", "duration": 180},
    {"name": "Tax Immunity", "cost": 2500, "effect": "Skip next tax collection", "duration": 0},
    {"name": "Lucky Strike", "cost": 777, "effect": "Next 10 clicks guaranteed critical (5x)", "duration": 0},
    {"name": "Speed Boost", "cost": 1500, "effect": "Generators run 1.5x faster for 5 minutes", "duration": 300},
    {"name": "Fortune Bonus", "cost": 3000, "effect": "Earn 25% more G for 10 minutes", "duration": 600},
]

# Active upgrades tracking
active_upgrades = []

# Guide for adding new items: set variables → add to shop() → add to upgrade() → add to gen_stats()
# Music toggle
mus = True
music_player_unlocked = False  # Player must unlock this upgrade first
# Game state variables
g = 0  # Player's gold
clickg = 1  # Gold per click
taxtime = 300  # Tax interval (seconds)
# Standard generator variables
gen_price = 10
gen_shop_amnt = 1
gen_list = []
gen_amnt = 0
g_given1 = 0.1
gen_lvl = 1
upgrade_cost = 100
#massive generators
bgen_price = 100
bgen_shop_amnt = 1
bgen_amnt = 0
bgen_list = []
g_given2 = 1
gen_lvl2 = 1
upgrade_cost2 = 200
#industrial generators
igen_price = 250
igen_shop_amnt = 1
igen_amnt = 0
igen_list = []
g_given3 = 10
gen_lvl3 = 1
upgrade_cost3 = 200
#random generators
randgen_price = 777
randgen_shop_amnt = 1
randgen_amnt = 0
randgen_list = []
g_given4 = 100
gen_lvl4 = 1
upgrade_cost4 = 777
gen_chance = 0.25
# nuclear generators
ngen_price = 500
ngen_shop_amnt = 1
ngen_amnt = 0
ngen_list = []
g_given5 = 500
gen_lvl5 = 1
upgrade_cost5 = 50
ngen_stock = 3
# quantum generators
qgen_price = 2500
qgen_shop_amnt = 1
qgen_amnt = 0
qgen_list = []
g_given6 = 2000
gen_lvl6 = 1
upgrade_cost6 = 100
qgen_stock = 2
# fusion generators
fgen_price = 15000
fgen_shop_amnt = 1
fgen_amnt = 0
fgen_list = []
g_given7 = 10000
gen_lvl7 = 1
upgrade_cost7 = 200
fgen_stock = 1
# Stock variables for each generator type
gen_stock = 15
bgen_stock = 10
igen_stock = 10
randgen_stock = 7
ngen_stock = 3
qgen_stock = 2
fgen_stock = 1

# Other upgrade costs
# Why the big jump? Cuz i love making games hard
upgrade_cost8 = 250
upgrade_cost9 = 400 
upgrade_cost10 = 450
upgrade_cost11 = 300
# Theres so much code, i forgot where these leads to but im just following my original scaling
# Dark theme toggle counter
click2 = 0
fixeth = 20  # Clicks to repair a generator
elec = True  # Electricity status
firstshop = False  # First-time shop flag
# Progression system
level = 1
current_exp = 0
next_level_exp = 100  # G needed for next level

# Setup audio file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
try:
    sound1_path = os.path.join(BASE_DIR, "sounds", "correct.mp3")
except FileNotFoundError:
    pass
try:
    sound2_path = os.path.join(BASE_DIR, "sounds", "wrong.mp3")
except FileNotFoundError:
    pass
try:
    sound3_path = os.path.join(BASE_DIR, "sounds", "elec.mp3")
except FileNotFoundError:
    pass
try:
    sound4_path = os.path.join(BASE_DIR, "sounds", "timeup.mp3")
except FileNotFoundError:
    pass
try:
    sound5_path = os.path.join(BASE_DIR, "sounds", "energy1.mp3")
except FileNotFoundError:
    pass
try:
    sound6_path = os.path.join(BASE_DIR, "sounds", "energy2.mp3")
except FileNotFoundError:
    pass
try:
    sound7_path = os.path.join(BASE_DIR, "sounds", "buttonpress1.mp3")
except FileNotFoundError:
    pass
try:
    sound8_path = os.path.join(BASE_DIR, "sounds", "you-are-an-idiot.mp3")
except FileNotFoundError:
    pass
try:
    sound9_path = os.path.join(BASE_DIR, "sounds", "yougotmail.mp3")
except FileNotFoundError:
    pass
try:
    sound10_path = os.path.join(BASE_DIR, "sounds", "math-song.mp3")
except FileNotFoundError:
    pass
try:
    sound11_path = os.path.join(BASE_DIR, "sounds", "dr-reflex-hammer-hit.mp3")
except FileNotFoundError:
    pass
# Initialize pygame mixer for sound effects
pygame.mixer.init()
sound1 = pygame.mixer.Sound(sound1_path)
sound2 = pygame.mixer.Sound(sound2_path)
sound3 = pygame.mixer.Sound(sound3_path)
sound4 = pygame.mixer.Sound(sound4_path)
sound5 = pygame.mixer.Sound(sound5_path)
sound6 = pygame.mixer.Sound(sound6_path)
sound7 = pygame.mixer.Sound(sound7_path)
sound8 = pygame.mixer.Sound(sound8_path)
sound9 = pygame.mixer.Sound(sound9_path)
sound10 = pygame.mixer.Sound(sound10_path)
sound11 = pygame.mixer.Sound(sound11_path)

# Basic Mechanics
# Toggle electricity on/off
def electricity():
    global elec
    if random.random() < 0.25:
        elec = False
class Generator():
    # Basic generator class
    def __init__(self, gen_level):
        self.gen_level = gen_level
        self.running = True
        self.off = False
        self.safe_until = 0  # Grace period after fix
        self.start_generating()

    def start_generating(self):
        current_time = time.time()

        if self.running:
            # Only try breaking if cooldown expired
            if current_time >= self.safe_until:
                if random.random() < 0.05:  # 5% chance to break
                    self.running = False
                    return

            elif elec is False:
                self.off = True
                return

            if self.off:
                self.running = False
                return

            global g
            g += g_given1
            g_label.config(text=f"{g:,.2f}G")  # Two decimals, commas for thousands
            gain_exp(g_given1)
            root.after(1000, self.start_generating)

    def lvlup(self):
        self.gen_level += 1
        global g_given1
        g_given1 = int(g_given1 * 1.15)
        return g_given1

    def mark_fixed(self):
        # Give 1–10 min cooldown after repair
        self.safe_until = time.time() + random.randint(60, 600)
        self.running = True
        self.off = False
        self.start_generating()


class BetterGenerator():
    # Massive generator - more powerful
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
                if random.random() < 0.05:
                    self.running = False
                    return

            elif elec is False:
                self.off = True
                return

            if self.off:
                self.running = False
                return

            global g
            g += g_given2
            g_label.config(text=f"{g:,.2f}G")  # Two decimals, commas for thousands
            gain_exp(g_given2)
            root.after(1000, self.start_generating)

    def lvlup(self):
        self.gen_level += 1
        global g_given2
        g_given2 = int(g_given2 * 1.15)
        return g_given2

    def mark_fixed(self):
        self.safe_until = time.time() + random.randint(60, 600)
        self.running = True
        self.off = False
        self.start_generating()


class IndusGenerator():
    # Industrial generator - high output (treasure class)
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
                if random.random() < 0.05:
                    self.running = False
                    return

            elif elec is False:
                self.off = True
                return

            if self.off:
                self.running = False
                return

            global g
            g += g_given3
            gain_exp(g_given3)
            g_label.config(text=f"{g:,.2f}G")  # Two decimals, commas for thousands
            root.after(1000, self.start_generating)
class RandGenerator():
    # Random chance generator - rare
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
                if random.random() < 0.05:
                    self.running = False
                    return

            elif elec is False:
                self.off = True
                return

            if self.off:
                self.running = False
                return

            global g, gen_chance
            if random.random() <= gen_chance:
                x = random.randint(1, g_given4)
                g += x
                gain_exp(x)
                add_log(f"G increased by chance by {x}")
            g_label.config(text=f"{g:,.2f}G")  # Two decimals, commas for thousands
            root.after(1000, self.start_generating)

    def lvlup(self):
        global g_given4, gen_chance
        g_given4 = int(g_given4 * 1.15)
        gen_chance *= 1.20
        return g_given4

    def mark_fixed(self):
        self.safe_until = time.time() + random.randint(60, 600)
        self.running = True
        self.off = False
        self.start_generating()   


class NuclearGenerator():
    # Nuclear generator - high output with wire connection minigame
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
                if random.random() < 0.05:
                    self.running = False
                    return

            elif elec is False:
                self.off = True
                return

            if self.off:
                self.running = False
                return

            global g, total_g_earned
            g += g_given5
            total_g_earned += g_given5
            gain_exp(g_given5)
            g_label.config(text=f"{g:,.2f}G")
            root.after(1000, self.start_generating)

    def lvlup(self):
        global g_given5
        g_given5 = int(g_given5 * 1.2)
        return g_given5

    def mark_fixed(self):
        self.safe_until = time.time() + random.randint(60, 600)
        self.running = True
        self.off = False
        self.start_generating()


class QuantumGenerator():
    # Quantum generator - very high output with code breaker minigame
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
                if random.random() < 0.05:
                    self.running = False
                    return

            elif elec is False:
                self.off = True
                return

            if self.off:
                self.running = False
                return

            global g, total_g_earned
            g += g_given6
            total_g_earned += g_given6
            gain_exp(g_given6)
            g_label.config(text=f"{g:,.2f}G")
            root.after(1000, self.start_generating)

    def lvlup(self):
        global g_given6
        g_given6 = int(g_given6 * 1.25)
        return g_given6

    def mark_fixed(self):
        self.safe_until = time.time() + random.randint(60, 600)
        self.running = True
        self.off = False
        self.start_generating()


class FusionGenerator():
    # Fusion generator - extreme output with timing puzzle minigame
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
                if random.random() < 0.05:
                    self.running = False
                    return

            elif elec is False:
                self.off = True
                return

            if self.off:
                self.running = False
                return

            global g, total_g_earned
            g += g_given7
            total_g_earned += g_given7
            gain_exp(g_given7)
            g_label.config(text=f"{g:,.2f}G")
            root.after(1000, self.start_generating)

    def lvlup(self):
        global g_given7
        g_given7 = int(g_given7 * 1.3)
        return g_given7

    def mark_fixed(self):
        self.safe_until = time.time() + random.randint(60, 600)
        self.running = True
        self.off = False
        self.start_generating()


# Shop interface for buying generators
def shop():
    global gen_price, gen_shop_amnt, gen_amnt
    global gen_stock, bgen_stock, igen_stock, randgen_stock, ngen_stock, qgen_stock, fgen_stock
    global bgen_price, bgen_shop_amnt, bgen_amnt
    global igen_price, igen_shop_amnt, igen_amnt
    global randgen_price, randgen_amnt, randgen_shop_amnt
    global ngen_price, ngen_amnt, ngen_shop_amnt
    global qgen_price, qgen_amnt, qgen_shop_amnt
    global fgen_price, fgen_amnt, fgen_shop_amnt
    global gen_list, bgen_list, igen_list, randgen_list, ngen_list, qgen_list, fgen_list
    global firstshop
    if firstshop == False:
        firstshop = True
        gen_stock = 15
        import random
        if random.random() < 0.5:
            bgen_stock = random.randint(1, 10)
        else:
            bgen_stock = 0
        if random.random() < 0.3:
            igen_stock = random.randint(1, 5)
        else:
            igen_stock = 0
        if random.random() < 0.777:
            randgen_stock = random.randint(1, 5)
        else:
            randgen_stock = 0
        if random.random() < 0.2:
            ngen_stock = random.randint(1, 3)
        else:
            ngen_stock = 0
        if random.random() < 0.1:
            qgen_stock = random.randint(1, 2)
        else:
            qgen_stock = 0
        if random.random() < 0.05:
            fgen_stock = 1
        else:
            fgen_stock = 0

    def increase():
        nonlocal shop_amnt
        global gen_shop_amnt, gen_stock
        if gen_shop_amnt < gen_stock:
            gen_shop_amnt += 1
            shop_amnt.config(text = f"amount: {gen_shop_amnt}")
    def decrease():
        nonlocal shop_amnt
        global gen_shop_amnt, gen_stock
        if gen_shop_amnt != 1 and gen_shop_amnt > 0:
            gen_shop_amnt -= 1
            shop_amnt.config(text = f"amount: {gen_shop_amnt}")
    def buy():
        nonlocal shop_g, shop_amnt, gen_shop_amnt_label, gen_stock_label
        global g, gen_price, gen_shop_amnt, gen_amnt, gen_stock

        if g >= gen_price * gen_shop_amnt and gen_shop_amnt <= gen_stock:
            g -= gen_price * gen_shop_amnt
            g_label.config(text=f"{g:,.2f}G")  # Two decimals, commas for thousands
            shop_g.config(text = f"{format(g)}G")
            for i in range(gen_shop_amnt):
                global newgen 
                newgen = Generator(gen_lvl)
                gen_list.append(newgen)
            gen_amnt += gen_shop_amnt
            gen_stock -= gen_shop_amnt  # Reduce stock
            gen_shop_amnt = 1
            gen_price = round(gen_price * 1.15)
            gen_shop_price_label.config(text = f"Price: {gen_price}G")
            shop_amnt.config(text = f"amount: {gen_shop_amnt}")
            gen_shop_amnt_label.config(text = f"Current amount: {len(gen_list)}", font = ("Arial", 14))
            gen_stock_label.config(text=f"Stock: {gen_stock}")
            gen_price = int(gen_price * 1.15)
    def bincrease():
        nonlocal bshop_amnt
        global bgen_shop_amnt, bgen_stock
        if bgen_shop_amnt < bgen_stock:
            bgen_shop_amnt += 1
            bshop_amnt.config(text = f"amount: {bgen_shop_amnt}")
    def bdecrease():
        nonlocal bshop_amnt
        global bgen_shop_amnt, bgen_stock
        if bgen_shop_amnt != 1 and bgen_shop_amnt > 0:
            bgen_shop_amnt -= 1
            bshop_amnt.config(text = f"amount: {bgen_shop_amnt}")

    def bbuy():
        nonlocal shop_g, bshop_amnt, bgen_shop_amnt_label, bgen_stock_label
        global g, bgen_price, bgen_shop_amnt, bgen_amnt, bgen_stock

        if g >= bgen_price * bgen_shop_amnt and bgen_shop_amnt <= bgen_stock:
            g -= bgen_price * bgen_shop_amnt
            g_label.config(text=f"{g:,.2f}G")  # Two decimals, commas for thousands
            shop_g.config(text = f"{format(g)}G")
            for i in range(bgen_shop_amnt):
                global newgen2
                newgen2 = BetterGenerator(gen_lvl2)
                gen_list.append(newgen2)
                bgen_list.append(newgen2)
            bgen_amnt += bgen_shop_amnt
            bgen_stock -= bgen_shop_amnt  # Reduce stock
            bgen_shop_amnt = 1
            bshop_amnt.config(text = f"amount: {bgen_shop_amnt}")
            bgen_shop_amnt_label.config(text = f"Current amount: {len(bgen_list)}", font = ("Arial", 14))
            bgen_stock_label.config(text=f"Stock: {bgen_stock}")
            bgen_price = int(bgen_price * 1.15)
    def iincrease():
        nonlocal ishop_amnt
        global igen_shop_amnt, igen_stock
        if igen_shop_amnt < igen_stock:
            igen_shop_amnt += 1
            ishop_amnt.config(text = f"amount: {igen_shop_amnt}")
    def idecrease():
        nonlocal ishop_amnt
        global igen_shop_amnt, igen_stock
        if igen_shop_amnt != 1 and igen_shop_amnt > 0:
            igen_shop_amnt -= 1
            ishop_amnt.config(text = f"amount: {igen_shop_amnt}")

    def ibuy():
        nonlocal shop_g, ishop_amnt, igen_shop_amnt_label, igen_stock_label
        global g, igen_price, igen_shop_amnt, igen_amnt, igen_stock

        if g >= igen_price * igen_shop_amnt and igen_shop_amnt <= igen_stock:
            g -= igen_price * igen_shop_amnt
            g_label.config(text=f"{g:,.2f}G")  # Two decimals, commas for thousands
            shop_g.config(text = f"{format(g)}G")
            for i in range(igen_shop_amnt):
                global newgen3
                newgen3 = IndusGenerator(gen_lvl3)
                gen_list.append(newgen3)
                igen_list.append(newgen3)
            igen_amnt += igen_shop_amnt
            igen_stock -= igen_shop_amnt  # Reduce stock
            igen_shop_amnt = 1
            ishop_amnt.config(text = f"amount: {igen_shop_amnt}")
            igen_shop_amnt_label.config(text = f"Current amount: {len(igen_list)}", font = ("Arial", 14))
            igen_stock_label.config(text=f"Stock: {igen_stock}")
            igen_price = int(igen_price * 1.15)
    def randincrease():
        global randgen_shop_amnt, randgen_stock
        if randgen_shop_amnt < randgen_stock:
            randgen_shop_amnt += 1
            randgen_shop_amnt_label.config(text = f"amount: {randgen_shop_amnt}")
    def randdecrease():
        global randgen_shop_amnt, randgen_stock
        if randgen_shop_amnt != 1 and randgen_shop_amnt > 0:
            randgen_shop_amnt -= 1
            randgen_shop_amnt_label.config(text = f"amount: {randgen_shop_amnt}")

    def randbuy():
        nonlocal shop_g, igen_shop_amnt_label, igen_stock_label
        global g, randgen_price, randgen_shop_amnt, randgen_amnt, randgen_stock

        if g >= randgen_price * randgen_shop_amnt and randgen_shop_amnt <= randgen_stock:
            g -= randgen_price * randgen_shop_amnt
            g_label.config(text=f"{g:,.2f}G")  # Two decimals, commas for thousands
            shop_g.config(text = f"{format(g)}G")
            for i in range(randgen_shop_amnt):
                global newgen4
                newgen4 = RandGenerator(gen_lvl4)
                gen_list.append(newgen4)
                randgen_list.append(newgen4)
            randgen_amnt += randgen_shop_amnt
            randgen_stock -= randgen_shop_amnt  # Reduce stock
            randgen_shop_amnt = 1
            randgen_shop_amnt_label.config(text = f"amount: {randgen_shop_amnt}")
            randgen_shop_amnt_label.config(text = f"Current amount: {len(randgen_list)}", font = ("Arial", 14))
            randgen_stock_label.config(text=f"Stock: {randgen_stock}")
            randgen_price = int(randgen_price * 1.15)
    def restock():
        nonlocal gen_stock_label, bgen_stock_label, randgen_stock_label
        global gen_stock, bgen_stock, igen_stock, randgen_stock
        global g
        if g < 100:
            return
        g -= 100
        gen_stock = 15
            # Random chance for BetterGenerators and Industrial Generators to be in stock
        import random
        if random.random() < 0.5:  # 50% chance to appear
            bgen_stock = random.randint(1, 10)  # 1 or 2 in stock
        else:
            bgen_stock = 0  # Not available this time
        if random.random() < 0.3:  # 30% chance to appear
            igen_stock = random.randint(1, 5)  # 1 or 2 in stock
        else:
            igen_stock = 0  # Not available this time
        if random.random() < 0.777:  # 77.7% chance to appear
            randgen_stock = random.randint(1, 5)  # 1 or 2 in stock
        else:
            randgen_stock = 0  # Not available this time
        gen_stock_label.config(text=f"Stock: {gen_stock}")
        bgen_stock_label.config(text=f"Stock: {bgen_stock}")
        igen_stock_label.config(text = f"Stock: {igen_stock}")

    shop_window = tk.Toplevel(root)
    shop_window.title("Shop Menu")
    shop_window.geometry("900x700")
    shop_window.attributes('-fullscreen', True)  # Make shop fullscreen
    
    def exit():
        shop_window.destroy()
    shop_window.bind('<F4>', exit)
    header = tk.Label(shop_window, text="SHOP", font=("Cascadia Code", 36, "bold"))
    header.pack(pady=20)
    shop_g = tk.Label(shop_window, text=f"{g}G\npress F4 to exit", font=("Cascadia Code", 30))
    shop_g.pack(pady=10)
    def update_shop_g():
        shop_g.config(text=f"{format(g)}G")
        shop_window.after(200, update_shop_g)
    update_shop_g()
    def exit_fullscreen1(event=None):
        shop_window.destroy()
    shop_window.bind('<Escape>', exit_fullscreen1)
    
    # Create canvas and scrollbar for scrolling
    canvas = tk.Canvas(shop_window, bg="white")
    scrollbar = ttk.Scrollbar(shop_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")
    
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Update scroll region when frame size changes
    def on_frame_configure(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
        # Make frame match canvas width
        canvas.itemconfig(canvas_window, width=canvas.winfo_width())
    
    scrollable_frame.bind("<Configure>", on_frame_configure)
    
    # Pack canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Bind mousewheel to canvas for scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    # --- Standard Generator Section ---
    std_frame = tk.LabelFrame(scrollable_frame, text="Standard G Generator", font=("Arial", 18, "bold"), padx=20, pady=10)
    std_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    gen_item = tk.Label(std_frame, text="Standard G generator (1g/s)", font=("Arial", 16))
    gen_item.grid(row=0, column=0, sticky="w")
    shop_amnt = tk.Label(std_frame, text=f"amount: {gen_shop_amnt}", font=("Arial", 16))
    shop_amnt.grid(row=0, column=1, padx=20)
    gen_shop_amnt_label = tk.Label(std_frame, text=f"Current amount: {len(gen_list)}", font=("Arial", 16))
    gen_shop_amnt_label.grid(row=1, column=0, sticky="w")
    gen_shop_price_label = tk.Label(std_frame, text=f"Price: {gen_price}G", font=("Arial", 16))
    gen_shop_price_label.grid(row=1, column=1)
    gen_stock_label = tk.Label(std_frame, text=f"Stock: {gen_stock}", font=("Arial", 16))
    gen_stock_label.grid(row=1, column=2, padx=20)
    buy_amnt_inc = ttk.Button(std_frame, text="+1", command=increase)
    buy_amnt_inc.grid(row=0, column=2)
    buy_amnt_dec = ttk.Button(std_frame, text="-1", command=decrease)
    buy_amnt_dec.grid(row=0, column=3)
    buy_button = ttk.Button(std_frame, text="BUY", command=buy)
    buy_button.grid(row=2, column=0, pady=10)

    # --- Massive Generator Section ---
    bgen_frame = tk.LabelFrame(scrollable_frame, text="Massive G Generator", font=("Arial", 18, "bold"), padx=20, pady=10)
    bgen_frame.pack(fill="both", expand=True, padx=20, pady=10)

    bgen_item = tk.Label(bgen_frame, text="Massive G generator (10g/s)", font=("Arial", 16))
    bgen_item.grid(row=0, column=0, sticky="w")
    bshop_amnt = tk.Label(bgen_frame, text=f"amount: {bgen_shop_amnt}", font=("Arial", 16))
    bshop_amnt.grid(row=0, column=1, padx=20)
    bgen_shop_amnt_label = tk.Label(bgen_frame, text=f"Current amount: {len(bgen_list)}", font=("Arial", 16))
    bgen_shop_amnt_label.grid(row=1, column=0, sticky="w")
    bgen_shop_price_label = tk.Label(bgen_frame, text=f"Price: {bgen_price}G", font=("Arial", 16))
    bgen_shop_price_label.grid(row=1, column=1)
    bgen_stock_label = tk.Label(bgen_frame, text=f"Stock: {bgen_stock}", font=("Arial", 16))
    bgen_stock_label.grid(row=1, column=2, padx=20)
    bbuy_amnt_inc = ttk.Button(bgen_frame, text="+1", command=bincrease)
    bbuy_amnt_inc.grid(row=0, column=2)
    bbuy_amnt_dec = ttk.Button(bgen_frame, text="-1", command=bdecrease)
    bbuy_amnt_dec.grid(row=0, column=3)
    bbuy_button = ttk.Button(bgen_frame, text="BUY", command=bbuy)
    bbuy_button.grid(row=2, column=0, pady=10)

    # --- Industrial Generator Section ---
    igen_frame = tk.LabelFrame(scrollable_frame, text="Industrial G Generator", font=("Arial", 18, "bold"), padx=20, pady=10)
    igen_frame.pack(fill="both", expand=True, padx=20, pady=10)

    igen_item = tk.Label(igen_frame, text="Industrial G generator (100g/s)", font=("Arial", 16))
    igen_item.grid(row=0, column=0, sticky="w")
    ishop_amnt = tk.Label(igen_frame, text=f"amount: {igen_shop_amnt}", font=("Arial", 16))
    ishop_amnt.grid(row=0, column=1, padx=20)
    igen_shop_amnt_label = tk.Label(igen_frame, text=f"Current amount: {len(igen_list)}", font=("Arial", 16))
    igen_shop_amnt_label.grid(row=1, column=0, sticky="w")
    igen_shop_price_label = tk.Label(igen_frame, text=f"Price: {igen_price}G", font=("Arial", 16))
    igen_shop_price_label.grid(row=1, column=1)
    igen_stock_label = tk.Label(igen_frame, text=f"Stock: {igen_stock}", font=("Arial", 16))
    igen_stock_label.grid(row=1, column=2, padx=20)
    ibuy_amnt_inc = ttk.Button(igen_frame, text="+1", command=iincrease)
    ibuy_amnt_inc.grid(row=0, column=2)
    ibuy_amnt_dec = ttk.Button(igen_frame, text="-1", command=idecrease)
    ibuy_amnt_dec.grid(row=0, column=3)
    ibuy_button = ttk.Button(igen_frame, text="BUY", command=ibuy)
    ibuy_button.grid(row=2, column=0, pady=10)

    # --- Randomized Generator Section ---
    randgen_frame = tk.LabelFrame(scrollable_frame, text="Randomized G Generator", font=("Arial", 18, "bold"), padx=20, pady=10)
    randgen_frame.pack(fill="both", expand=True, padx=20, pady=10)

    randgen_item = tk.Label(randgen_frame, text=f"Randomized G Generator (1-{g_given4}G/s)", font=("Arial", 16))
    randgen_item.grid(row=0, column=0, sticky="w")
    ishop_amnt = tk.Label(randgen_frame, text=f"amount: {randgen_shop_amnt}", font=("Arial", 16))
    ishop_amnt.grid(row=0, column=1, padx=20)
    randgen_shop_amnt_label = tk.Label(randgen_frame, text=f"Current amount: {len(randgen_list)}", font=("Arial", 16))
    randgen_shop_amnt_label.grid(row=1, column=0, sticky="w")
    randgen_shop_price_label = tk.Label(randgen_frame, text=f"Price: {randgen_price}G", font=("Arial", 16))
    randgen_shop_price_label.grid(row=1, column=1)
    randgen_stock_label = tk.Label(randgen_frame, text=f"Stock: {randgen_stock}", font=("Arial", 16))
    randgen_stock_label.grid(row=1, column=2, padx=20)
    randbuy_amnt_inc = ttk.Button(randgen_frame, text="+1", command=randincrease)
    randbuy_amnt_inc.grid(row=0, column=2)
    randbuy_amnt_dec = ttk.Button(randgen_frame, text="-1", command=randdecrease)
    randbuy_amnt_dec.grid(row=0, column=3)
    randbuy_button = ttk.Button(randgen_frame, text="BUY", command=randbuy)
    randbuy_button.grid(row=2, column=0, pady=10)

    # --- Plasma Generator Section (High Output - 2500G/s) ---
    plasma_frame = tk.LabelFrame(scrollable_frame, text="Plasma Generator", font=("Arial", 18, "bold"), padx=20, pady=10)
    plasma_frame.pack(fill="both", expand=True, padx=20, pady=10)

    plasma_item = tk.Label(plasma_frame, text="Plasma Generator (2500G/s)", font=("Arial", 16))
    plasma_item.grid(row=0, column=0, sticky="w")
    plasma_shop_amnt_label = tk.Label(plasma_frame, text=f"Current amount: {len(plasma_list)}", font=("Arial", 16))
    plasma_shop_amnt_label.grid(row=2, column=0, sticky="w")
    plasma_shop_price_label = tk.Label(plasma_frame, text=f"Price: {format(plasma_price)}G", font=("Arial", 16))
    plasma_shop_price_label.grid(row=2, column=1)
    plasma_stock_label = tk.Label(plasma_frame, text=f"Stock: {plasma_stock}", font=("Arial", 16))
    plasma_stock_label.grid(row=2, column=2, padx=20)
    
    def plasmabuy():
        global g, plasma_price, plasma_amnt, plasma_stock
        if g >= plasma_price and plasma_stock > 0:
            g -= plasma_price
            g_label.config(text=f"{format(g)}G")
            shop_g.config(text=f"{format(g)}G")
            new_plasma = PlasmaGenerator(gen_lvl8)
            plasma_list.append(new_plasma)
            plasma_amnt += 1
            plasma_stock -= 1
            plasma_price = int(plasma_price * 1.4)
            plasma_shop_price_label.config(text=f"Price: {format(plasma_price)}G")
            plasma_shop_amnt_label.config(text=f"Current amount: {len(plasma_list)}")
            plasma_stock_label.config(text=f"Stock: {plasma_stock}")
    
    plasma_buy_button = ttk.Button(plasma_frame, text="BUY", command=plasmabuy)
    plasma_buy_button.grid(row=3, column=0, pady=10)

    # --- Steam Generator Section (500G/s but breaks easily) ---
    steam_frame = tk.LabelFrame(scrollable_frame, text="Steam Generator", font=("Arial", 18, "bold"), padx=20, pady=10)
    steam_frame.pack(fill="both", expand=True, padx=20, pady=10)

    steam_item = tk.Label(steam_frame, text="Steam Generator (500G/s)", font=("Arial", 16))
    steam_item.grid(row=0, column=0, sticky="w")
    steaminfo_label = tk.Label(steam_frame, text="High break chance (25%)", font=("Arial", 12), fg="red")
    steaminfo_label.grid(row=1, column=0, sticky="w")
    steam_shop_amnt_label = tk.Label(steam_frame, text=f"Current amount: {len(steam_list)}", font=("Arial", 16))
    steam_shop_amnt_label.grid(row=2, column=0, sticky="w")
    steam_shop_price_label = tk.Label(steam_frame, text=f"Price: {format(steam_price)}G", font=("Arial", 16))
    steam_shop_price_label.grid(row=2, column=1)
    steam_stock_label = tk.Label(steam_frame, text=f"Stock: {steam_stock}", font=("Arial", 16))
    steam_stock_label.grid(row=2, column=2, padx=20)
    
    def steambuy():
        global g, steam_price, steam_amnt, steam_stock
        if g >= steam_price and steam_stock > 0:
            g -= steam_price
            g_label.config(text=f"{format(g)}G")
            shop_g.config(text=f"{format(g)}G")
            new_steam = SteamGenerator(gen_lvl11)
            steam_list.append(new_steam)
            steam_amnt += 1
            steam_stock -= 1
            steam_price = int(steam_price * 1.3)
            steam_shop_price_label.config(text=f"Price: {format(steam_price)}G")
            steam_shop_amnt_label.config(text=f"Current amount: {len(steam_list)}")
            steam_stock_label.config(text=f"Stock: {steam_stock}")
    
    steam_buy_button = ttk.Button(steam_frame, text="BUY", command=steambuy)
    steam_buy_button.grid(row=3, column=0, pady=10)

    # --- Void Generator Section (Extreme Output - 10000G/s) ---
    void_frame = tk.LabelFrame(scrollable_frame, text="Void Generator", font=("Arial", 18, "bold"), padx=20, pady=10)
    void_frame.pack(fill="both", expand=True, padx=20, pady=10)

    void_item = tk.Label(void_frame, text="Void Generator (10000G/s) (Hard to fix)", font=("Arial", 16))
    void_item.grid(row=0, column=0, sticky="w")
    void_shop_amnt_label = tk.Label(void_frame, text=f"Current amount: {len(void_list)}", font=("Arial", 16))
    void_shop_amnt_label.grid(row=2, column=0, sticky="w")
    void_shop_price_label = tk.Label(void_frame, text=f"Price: {format(void_price)}G", font=("Arial", 16))
    void_shop_price_label.grid(row=2, column=1)
    void_stock_label = tk.Label(void_frame, text=f"Stock: {void_stock}", font=("Arial", 16))
    void_stock_label.grid(row=2, column=2, padx=20)
    
    def voidbuy():
        global g, void_price, void_amnt, void_stock
        if g >= void_price and void_stock > 0:
            g -= void_price
            g_label.config(text=f"{format(g)}G")
            shop_g.config(text=f"{format(g)}G")
            new_void = VoidGenerator(gen_lvl9)
            void_list.append(new_void)
            void_amnt += 1
            void_stock -= 1
            void_price = int(void_price * 1.5)
            void_shop_price_label.config(text=f"Price: {format(void_price)}G")
            void_shop_amnt_label.config(text=f"Current amount: {len(void_list)}")
            void_stock_label.config(text=f"Stock: {void_stock}")
    
    void_buy_button = ttk.Button(void_frame, text="BUY", command=voidbuy)
    void_buy_button.grid(row=3, column=0, pady=10)

    # --- Chronos Generator Section (Ultimate Output - 50000G/s) ---
    chronos_frame = tk.LabelFrame(scrollable_frame, text="Chronos Generator", font=("Arial", 18, "bold"), padx=20, pady=10)
    chronos_frame.pack(fill="both", expand=True, padx=20, pady=10)

    chronos_item = tk.Label(chronos_frame, text="Chronos Generator (50000G/s)", font=("Arial", 16))
    chronos_item.grid(row=0, column=0, sticky="w")
    chronos_shop_amnt_label = tk.Label(chronos_frame, text=f"Current amount: {len(chronos_list)}", font=("Arial", 16))
    chronos_shop_amnt_label.grid(row=2, column=0, sticky="w")
    chronos_shop_price_label = tk.Label(chronos_frame, text=f"Price: {format(chronos_price)}G", font=("Arial", 16))
    chronos_shop_price_label.grid(row=2, column=1)
    chronos_stock_label = tk.Label(chronos_frame, text=f"Stock: {chronos_stock}", font=("Arial", 16))
    chronos_stock_label.grid(row=2, column=2, padx=20)
    
    def chronosbuy():
        global g, chronos_price, chronos_amnt, chronos_stock
        if g >= chronos_price and chronos_stock > 0:
            g -= chronos_price
            g_label.config(text=f"{format(g)}G")
            shop_g.config(text=f"{format(g)}G")
            new_chronos = ChronosGenerator(gen_lvl10)
            chronos_list.append(new_chronos)
            chronos_amnt += 1
            chronos_stock -= 1
            chronos_price = int(chronos_price * 1.6)
            chronos_shop_price_label.config(text=f"Price: {format(chronos_price)}G")
            chronos_shop_amnt_label.config(text=f"Current amount: {len(chronos_list)}")
            chronos_stock_label.config(text=f"Stock: {chronos_stock}")
    
    chronos_buy_button = ttk.Button(chronos_frame, text="BUY", command=chronosbuy)
    chronos_buy_button.grid(row=3, column=0, pady=10)

    # --- Restock Button ---
    restock_button = ttk.Button(scrollable_frame, text="Restock (100G)", command=restock)
    restock_button.pack(pady=30)
    
    # Reset scroll to top after all content is added
    shop_window.update_idletasks()
    canvas.yview_moveto(0)

    close_button = ttk.Button(shop_window, text="Close Shop", command=shop_window.destroy)
    close_button.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)  # Top right corner with padding
# Manage upgrades and generator repairs
def upgrade_and_stats():
    global gen_lvl, gen_lvl2, gen_lvl3
    def fix_generators(gen_list_to_fix, start_method_name, wrong_labels):
        if not gen_list_to_fix:
            messagebox.showinfo("No Generators", "You have no generators to fix!")
            return

        clicks_needed = 5
        clicks = [0]
        time_left = [15]

        maint_win = tk.Toplevel(root)
        maint_win.geometry("400x300")
        maint_win.title("Fix the Generators!")
        maint_win.grab_set()

        progress_bar = ttk.Progressbar(
            maint_win, orient="horizontal", mode="determinate",
            length=200, maximum=clicks_needed
        )
        progress_bar.pack(pady=20)

        tk.Label(maint_win, text="Click the moving button 5 times to fix!", font=("Arial", 12)).pack(pady=10)
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
            sound1.play()
            clicks[0] += 1
            progress_bar['value'] = clicks[0]
            if clicks[0] >= clicks_needed:
                for gobj in gen_list_to_fix:
                    gobj.running = True
                    gobj.off = False
                    gobj.mark_fixed()
                    getattr(gobj, start_method_name)()
                gen_update()
                maint_win.destroy()
            else:
                move_buttons()

        def on_wrong_click():
            sound2.play()
            if clicks[0] > 0:
                clicks[0] -= 1
                progress_bar['value'] = clicks[0]
            move_buttons()

        def move_buttons():
            positions = []
            while len(positions) < len(wrong_labels) + 1:
                x = random.randint(50, 300)
                y = random.randint(80, 220)
                if all(abs(x - px) >= 60 or abs(y - py) >= 40 for px, py in positions):
                    positions.append((x, y))
            fix_button.place(x=positions[0][0], y=positions[0][1])
            for btn, pos in zip(wrong_buttons, positions[1:]):
                btn.place(x=pos[0], y=pos[1])

        # Create buttons
        fix_button = ttk.Button(maint_win, text="fix", command=on_correct_click)
        wrong_buttons = [ttk.Button(maint_win, text=label, command=on_wrong_click) for label in wrong_labels]

        move_buttons()
        update_timer()


    # Wrappers for each generator type
    def generator_fix():
        fix_generators(gen_list, "start_generating", ["xif"])

    def bgenerator_fix():
        fix_generators(bgen_list, "start_generating", ["xif", "ifx"])

    def igenerator_fix():
        fix_generators(igen_list, "start_generating", ["xif", "ifx", "reconstruct"])
    
    # Wait a minute...a custom skillcheck for randomized generators?

    def randgen_fix():
        global randgen_list
        if not randgen_list:
            messagebox.showinfo("No Generators", "You have no random generators to fix!")
            return

        success_needed = 5
        success = [0]
        time_left = [20]

        maint_win = tk.Toplevel(root)
        maint_win.geometry("400x300")
        maint_win.title("Probability Recalibration Console")
        maint_win.grab_set()

        timer_label = tk.Label(
            maint_win,
            text=f"Time left: {time_left[0]}s",
            font=("Arial", 12),
            fg="red"
        )
        timer_label.pack(pady=(5, 0))  # Less bottom padding

        # Instructions next
        tk.Label(
            maint_win,
            text="Hit the middle 5 times to fix!",
            font=("Arial", 12)
        ).pack(pady=(5, 10))  # Tighter spacing

        # Progressbar
        progress_bar = ttk.Progressbar(
            maint_win,
            orient="horizontal",
            mode="determinate",
            length=200
        )
        progress_bar.pack(pady=(5, 0))  # No bottom padding
        progress_bar['maximum'] = 200

        # Carat directly under progress bar
        tk.Label(
            maint_win,
            text="^",
            font=("Arial", 12)
        ).pack(anchor="center", pady=(0, 10))  # Small gap only

    # --- Advanced Generator Fix Functions ---
    def plasma_fix_wrapper():
        # Import the plasma fix function from advanced_generators
        from advanced_generators import plasma_fix
        plasma_fix(plasma_list)
    
    def steam_fix_wrapper():
        from advanced_generators import steam_fix_minigame
        steam_fix_minigame(steam_list)
    
    def void_fix_wrapper():
        from advanced_generators import void_fix
        void_fix(void_list)
    
    def chronos_fix_wrapper():
        from advanced_generators import chronos_fix
        chronos_fix(chronos_list)


        def update_timer():
            if success[0] >= success_needed:
                return
            time_left[0] -= 1
            timer_label.config(text=f"Time left: {time_left[0]}s")
            if time_left[0] <= 0:
                messagebox.showerror('Aw man!', 'Probability unsuccessfully calibrated.')
                maint_win.destroy()
            else:
                maint_win.after(1000, update_timer)
        update_timer()

        direction = 1

        def progressbar():
            nonlocal direction

            # Stop if widget was destroyed
            if not progress_bar.winfo_exists():
                return

            value = progress_bar['value']
            maximum = progress_bar['maximum']

            # Update value based on direction
            value += 10 * direction
            progress_bar['value'] = value

            # Reverse direction at limits
            if value >= maximum:
                direction = -1
            elif value <= 0:
                direction = 1

            root.after(150, progressbar)
        progressbar()
        def skillcheck():
            if progress_bar['value'] == progress_bar['maximum']/2:
                success[0] += 1
                progress_bar['value'] = 0
                skillcheck_label.config(text = f"Calibrations: {success[0]}")
            else:
                progress_bar['value'] = 0
        def checker():
            if success[0] == success_needed:
                # Fix the random generators
                for gobj in randgen_list:
                    gobj.running = True
                    gobj.off = False
                    gobj.mark_fixed()
                    gobj.start_generating()
                gen_update()
                maint_win.destroy()
            root.after(100, checker)
        skillcheck_button = ttk.Button(maint_win, text = "Calibrate", command = skillcheck)
        skillcheck_button.pack(anchor = "center", pady = 10)
        skillcheck_label = tk.Label(maint_win, text = f"Calibrations: {success[0]}", font = ("Cascadia Code", 14))
        skillcheck_label.pack(anchor = "center", pady = 10)
        checker()
        def on_close():
            maint_win.destroy()
        maint_win.protocol("WM_DELETE_WINDOW", on_close)
        

    def elec_fix():
        global elec
        if elec:
            return
        import elec_fixer
        elec_fixer.start_elec_fix(root, on_repair_complete=set_elec_true)

    def set_elec_true():
        global elec
        elec = True        
            
    win = tk.Toplevel(root)
    win.title("Upgrades & Generator Status")
    win.geometry("700x600")
    win.attributes("-fullscreen", True)
        # --- Make notebook tabs more obvious ---
    style = ttk.Style(win)
    style.configure("TNotebook.Tab", font=("Cascadia Code", 16, "bold"), padding=[20, 10])
    style.map("TNotebook.Tab",
              background=[("selected", "#d1eaff"), ("!selected", "#b0b0b0")],
              foreground=[("selected", "#000000"), ("!selected", "#444444")])
    style.configure("TNotebook", background="#f0f0f0", tabmargins=[10, 5, 10, 5])
    notebook = ttk.Notebook(win)
    notebook.pack(fill="both", expand=True)

    # --- Upgrade Tab ---
    upgrade_tab = ttk.Frame(notebook)
    notebook.add(upgrade_tab, text="Upgrades")

    g_upgrade_label = tk.Label(upgrade_tab, text=f"{format(g)}G", font=("Cascadia Code", 25))
    g_upgrade_label.pack(padx=50, pady=10, anchor="nw")
    def update_g_upgr_label():
        g_upgrade_label.config(text=f"{format(g)}G")
        win.after(200, update_g_upgr_label)
    update_g_upgr_label()

    # Standard Generator Upgrade
    stdgen_frame = tk.LabelFrame(upgrade_tab, text="Standard Generator", font=("Arial", 14, "bold"), padx=20, pady=10)
    stdgen_frame.pack(fill="x", padx=40, pady=10)
    stdgen_label = tk.Label(stdgen_frame, text=f"Level: {gen_lvl}", font=("Arial", 16))
    stdgen_label.grid(row=0, column=0, sticky="w")
    def upgrader():
        global gen_lvl, upgrade_cost, g_given1, level
        if level < 2:
            stdgen_button.config(text="Not enough levels")
            root.after(200, lambda: stdgen_button.config(text=f"UPGRADE (2 Levels)"))
        else:
            level -= 2
            if len(gen_list) == 0:
                return
            for newgen in gen_list:
                newgen.lvlup()
            gen_lvl += 1
            upgrade_cost = int(upgrade_cost * 1.75)
            if level >= 25:
                level_label.config(text=f"Level: {level} (I)")
            elif level >= 50:
                level_label.config(text=f"Level: {level} (II)")
            elif level >= 75:
                level_label.config(text=f"Level: {level} (III)")
            elif level >= 100:
                level_label.config(text=f"Level: {level} (IV)")
            else:
                level_label.config(text=f"Level: {level}")
            stdgen_label.config(text=f"Level: {gen_lvl}")
            stdgen_button.config(text=f"UPGRADE (2 Levels)")
    stdgen_button = ttk.Button(stdgen_frame, text=f"UPGRADE (2 Levels)", command=upgrader)
    stdgen_button.grid(row=0, column=1, padx=20)

    # Massive Generator Upgrade
    bgen_frame = tk.LabelFrame(upgrade_tab, text="Massive Generator", font=("Arial", 14, "bold"), padx=20, pady=10)
    bgen_frame.pack(fill="x", padx=40, pady=10)
    bgen_label = tk.Label(bgen_frame, text=f"Level: {gen_lvl2}", font=("Arial", 16))
    bgen_label.grid(row=0, column=0, sticky="w")
    def upgrader2():
        global gen_lvl2, upgrade_cost2, g_given2, level
        if level < 3:
            bgen_button.config(text="Not enough levels")
            root.after(200, lambda: bgen_button.config(text=f"UPGRADE (3 Levels)"))
        else:
            level -= 3
            if len(bgen_list) == 0:
                return
            for newgen2 in bgen_list:
                newgen2.lvlup()
            gen_lvl2 += 1
            upgrade_cost2 = int(upgrade_cost2 * 2.5)
            if level >= 25:
                level_label.config(text=f"Level: {level} (I)")
            elif level >= 50:
                level_label.config(text=f"Level: {level} (II)")
            elif level >= 75:
                level_label.config(text=f"Level: {level} (III)")
            elif level >= 100:
                level_label.config(text=f"Level: {level} (IV)")
            else:
                level_label.config(text=f"Level: {level}")
            bgen_label.config(text=f"Level: {gen_lvl2}")
            bgen_button.config(text=f"UPGRADE (3 Levels)")
    bgen_button = ttk.Button(bgen_frame, text=f"UPGRADE (3 Levels)", command=upgrader2)
    bgen_button.grid(row=0, column=1, padx=20)

    # Industrial Generator Upgrade
    igen_frame = tk.LabelFrame(upgrade_tab, text="Industrial Generator", font=("Arial", 14, "bold"), padx=20, pady=10)
    igen_frame.pack(fill="x", padx=40, pady=10)
    igen_label = tk.Label(igen_frame, text=f"Level: {gen_lvl3}", font=("Arial", 16))
    igen_label.grid(row=0, column=0, sticky="w")
    def upgrader3():
        global gen_lvl3, upgrade_cost3, g_given3, level
        if level < 5:
            igen_button.config(text="Not enough levels")
            root.after(200, lambda: igen_button.config(text=f"UPGRADE (5 Levels)"))
        else:
            level -= 5
            if len(igen_list) == 0:
                return
            for igen in igen_list:
                igen.lvlup()
            gen_lvl3 += 1
            upgrade_cost3 = int(upgrade_cost3 * 3)
            if level >= 25:
                level_label.config(text=f"Level: {level} (I)")
            elif level >= 50:
                level_label.config(text=f"Level: {level} (II)")
            elif level >= 75:
                level_label.config(text=f"Level: {level} (III)")
            elif level >= 100:
                level_label.config(text=f"Level: {level} (IV)")
            else:
                level_label.config(text=f"Level: {level}")
            igen_label.config(text=f"Level: {gen_lvl3}")
            igen_button.config(text=f"UPGRADE (5 Levels)")
    igen_button = ttk.Button(igen_frame, text=f"UPGRADE (5 Levels)", command=upgrader3)
    igen_button.grid(row=0, column=1, padx=20)

    # Randomized Generator Upgrade
    randgen_frame = tk.LabelFrame(upgrade_tab, text="Random Generator", font=("Arial", 14, "bold"), padx=20, pady=10)
    randgen_frame.pack(fill="x", padx=40, pady=10)
    randgen_label = tk.Label(randgen_frame, text=f"Level: {gen_lvl4}", font=("Arial", 16))
    randgen_label.grid(row=0, column=0, sticky="w")
    def upgrader4():
        global gen_lvl4, upgrade_cost4, g_given4, level
        if level < 5:
            randgen_button.config(text="Not enough levels")
            root.after(200, lambda: randgen_button.config(text=f"UPGRADE (5 Levels)"))
        else:
            level -= 5
            if len(randgen_list) == 0:
                return
            for randgen in randgen_list:
                randgen.lvlup()
            gen_lvl4 += 1
            upgrade_cost4 = int(upgrade_cost4 * 3)
            if level >= 25:
                level_label.config(text=f"Level: {level} (I)")
            elif level >= 50:
                level_label.config(text=f"Level: {level} (II)")
            elif level >= 75:
                level_label.config(text=f"Level: {level} (III)")
            elif level >= 100:
                level_label.config(text=f"Level: {level} (IV)")
            else:
                level_label.config(text=f"Level: {level}")
            randgen_label.config(text=f"Level: {gen_lvl4}")
            randgen_button.config(text=f"UPGRADE (5 Levels)")
    randgen_button = ttk.Button(randgen_frame, text=f"UPGRADE (5 Levels)", command=upgrader4)
    randgen_button.grid(row=0, column=1, padx=20)

    # --- Advanced Generator Upgrades ---
    
    # Plasma Generator Upgrade
    plasma_upgr_frame = tk.LabelFrame(upgrade_tab, text="Plasma Generator", font=("Arial", 14, "bold"), padx=20, pady=10)
    plasma_upgr_frame.pack(fill="x", padx=40, pady=10)
    plasma_upgr_label = tk.Label(plasma_upgr_frame, text=f"Level: {gen_lvl8}", font=("Arial", 16))
    plasma_upgr_label.grid(row=0, column=0, sticky="w")
    def upgrader_plasma():
        global gen_lvl8, upgrade_cost8, g_given8, level
        # consume player levels instead of gold
        if level >= upgrade_cost8:
            level -= upgrade_cost8
            # refresh the main level label with tier suffix
            if level >= 25:
                level_label.config(text=f"Level: {level} (I)")
            elif level >= 50:
                level_label.config(text=f"Level: {level} (II)")
            elif level >= 75:
                level_label.config(text=f"Level: {level} (III)")
            elif level >= 100:
                level_label.config(text=f"Level: {level} (IV)")
            else:
                level_label.config(text=f"Level: {level}")
            gen_lvl8 += 1
            upgrade_cost8 = int(upgrade_cost8 * 1.5)
            g_given8 = int(g_given8 * 1.35)
            plasma_upgr_label.config(text=f"Level: {gen_lvl8}")
            plasma_upgr_button.config(text=f"UPGRADE ({upgrade_cost8} Levels)")
        else:
            messagebox.showerror("Not Enough Levels", f"You need {upgrade_cost8} levels to upgrade!")
    plasma_upgr_button = ttk.Button(plasma_upgr_frame, text=f"UPGRADE ({upgrade_cost8} Levels)", command=upgrader_plasma)
    plasma_upgr_button.grid(row=0, column=1, padx=20)

    # Steam Generator Upgrade
    steam_upgr_frame = tk.LabelFrame(upgrade_tab, text="Steam Generator", font=("Arial", 14, "bold"), padx=20, pady=10)
    steam_upgr_frame.pack(fill="x", padx=40, pady=10)
    steam_upgr_label = tk.Label(steam_upgr_frame, text=f"Level: {gen_lvl11}", font=("Arial", 16))
    steam_upgr_label.grid(row=0, column=0, sticky="w")
    def upgrader_steam():
        global gen_lvl11, upgrade_cost11, g_given11, level
        if level >= upgrade_cost11:
            level -= upgrade_cost11
            if level >= 25:
                level_label.config(text=f"Level: {level} (I)")
            elif level >= 50:
                level_label.config(text=f"Level: {level} (II)")
            elif level >= 75:
                level_label.config(text=f"Level: {level} (III)")
            elif level >= 100:
                level_label.config(text=f"Level: {level} (IV)")
            else:
                level_label.config(text=f"Level: {level}")
            gen_lvl11 += 1
            upgrade_cost11 = int(upgrade_cost11 * 1.5)
            g_given11 = int(g_given11 * 1.25)
            steam_upgr_label.config(text=f"Level: {gen_lvl11}")
            steam_upgr_button.config(text=f"UPGRADE ({upgrade_cost11} Levels)")
        else:
            messagebox.showerror("Not Enough Levels", f"You need {upgrade_cost11} levels to upgrade!")
    steam_upgr_button = ttk.Button(steam_upgr_frame, text=f"UPGRADE ({upgrade_cost11} Levels)", command=upgrader_steam)
    steam_upgr_button.grid(row=0, column=1, padx=20)

    # Void Generator Upgrade
    void_upgr_frame = tk.LabelFrame(upgrade_tab, text="Void Generator", font=("Arial", 14, "bold"), padx=20, pady=10)
    void_upgr_frame.pack(fill="x", padx=40, pady=10)
    void_upgr_label = tk.Label(void_upgr_frame, text=f"Level: {gen_lvl9}", font=("Arial", 16))
    void_upgr_label.grid(row=0, column=0, sticky="w")
    def upgrader_void():
        global gen_lvl9, upgrade_cost9, g_given9, level
        if level >= upgrade_cost9:
            level -= upgrade_cost9
            if level >= 25:
                level_label.config(text=f"Level: {level} (I)")
            elif level >= 50:
                level_label.config(text=f"Level: {level} (II)")
            elif level >= 75:
                level_label.config(text=f"Level: {level} (III)")
            elif level >= 100:
                level_label.config(text=f"Level: {level} (IV)")
            else:
                level_label.config(text=f"Level: {level}")
            gen_lvl9 += 1
            upgrade_cost9 = int(upgrade_cost9 * 1.5)
            g_given9 = int(g_given9 * 1.4)
            void_upgr_label.config(text=f"Level: {gen_lvl9}")
            void_upgr_button.config(text=f"UPGRADE ({upgrade_cost9} Levels)")
        else:
            messagebox.showerror("Not Enough Levels", f"You need {upgrade_cost9} levels to upgrade!")
    void_upgr_button = ttk.Button(void_upgr_frame, text=f"UPGRADE ({upgrade_cost9} Levels)", command=upgrader_void)
    void_upgr_button.grid(row=0, column=1, padx=20)

    # Chronos Generator Upgrade
    chronos_upgr_frame = tk.LabelFrame(upgrade_tab, text="Chronos Generator", font=("Arial", 14, "bold"), padx=20, pady=10)
    chronos_upgr_frame.pack(fill="x", padx=40, pady=10)
    chronos_upgr_label = tk.Label(chronos_upgr_frame, text=f"Level: {gen_lvl10}", font=("Arial", 16))
    chronos_upgr_label.grid(row=0, column=0, sticky="w")
    def upgrader_chronos():
        global gen_lvl10, upgrade_cost10, g_given10, level
        if level >= upgrade_cost10:
            level -= upgrade_cost10
            if level >= 25:
                level_label.config(text=f"Level: {level} (I)")
            elif level >= 50:
                level_label.config(text=f"Level: {level} (II)")
            elif level >= 75:
                level_label.config(text=f"Level: {level} (III)")
            elif level >= 100:
                level_label.config(text=f"Level: {level} (IV)")
            else:
                level_label.config(text=f"Level: {level}")
            gen_lvl10 += 1
            upgrade_cost10 = int(upgrade_cost10 * 1.5)
            g_given10 = int(g_given10 * 1.45)
            chronos_upgr_label.config(text=f"Level: {gen_lvl10}")
            chronos_upgr_button.config(text=f"UPGRADE ({upgrade_cost10} Levels)")
        else:
            messagebox.showerror("Not Enough Levels", f"You need {upgrade_cost10} levels to upgrade!")
    chronos_upgr_button = ttk.Button(chronos_upgr_frame, text=f"UPGRADE ({upgrade_cost10} Levels)", command=upgrader_chronos)
    chronos_upgr_button.grid(row=0, column=1, padx=20)

    close_button = ttk.Button(upgrade_tab, text="Close Window", command=win.destroy)
    close_button.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)

    # --- Generator Status Tab ---
    stats_tab = ttk.Frame(notebook)
    notebook.add(stats_tab, text="Generator Status")

    # Standard Generator
    stdgen_status_frame = tk.LabelFrame(
    stats_tab,
    text="Standard Generator",
    font=("Arial", 14, "bold"),
    padx=20,
    pady=10
    )
    stdgen_status_frame.pack(fill="x", padx=40, pady=10)

    gen_stats = tk.Label(
        stdgen_status_frame,
        text=f"Produces {g_given1}/s",
        font=("Arial", 16)
    )
    gen_stats.grid(row=0, column=0, sticky="w")

    fix_button = ttk.Button(
        stdgen_status_frame,
        text="fix gens",
        command=generator_fix   # 🔴 unchanged
    )
    fix_button.grid(row=0, column=1, padx=20)

    gen_status_label = tk.Label(
        stdgen_status_frame,
        text="",
        font=("Arial", 13)
    )
    gen_status_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 0))

    # Massive Generator
    massgen_status_frame = tk.LabelFrame(
    stats_tab,
    text="Massive Generator",
    font=("Arial", 14, "bold"),
    padx=20,
    pady=10
    )
    massgen_status_frame.pack(fill="x", padx=40, pady=10)

    gen_stats2 = tk.Label(
        massgen_status_frame,
        text=f"Produces {g_given2}/s",
        font=("Arial", 16)
    )
    gen_stats2.grid(row=0, column=0, sticky="w")

    fix_button2 = ttk.Button(
        massgen_status_frame,
        text="fix gens",
        command=bgenerator_fix   # unchanged
    )
    fix_button2.grid(row=0, column=1, padx=20)

    gen_status2_label = tk.Label(
        massgen_status_frame,
        text="",
        font=("Arial", 13)
    )
    gen_status2_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 0))

    # Industrial Generator
    indgen_status_frame = tk.LabelFrame(
    stats_tab,
    text="Industrial Generator",
    font=("Arial", 14, "bold"),
    padx=20,
    pady=10
    )
    indgen_status_frame.pack(fill="x", padx=40, pady=10)

    gen_stats3 = tk.Label(
        indgen_status_frame,
        text=f"Produces {g_given3}/s",
        font=("Arial", 16)
    )
    gen_stats3.grid(row=0, column=0, sticky="w")

    fix_button3 = ttk.Button(
        indgen_status_frame,
        text="fix gens",
        command=igenerator_fix   # unchanged
    )
    fix_button3.grid(row=0, column=1, padx=20)

    gen_status3_label = tk.Label(
        indgen_status_frame,
        text="",
        font=("Arial", 13)
    )
    gen_status3_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 0))


    # Randomized Generator
    randgen_status_frame = tk.LabelFrame(
    stats_tab,
    text="Randomized Generator",
    font=("Arial", 14, "bold"),
    padx=20,
    pady=10
    )
    randgen_status_frame.pack(fill="x", padx=40, pady=10)

    gen_stats4 = tk.Label(
        randgen_status_frame,
        text=f"Produces 1–{g_given4}/s",
        font=("Arial", 16)
    )
    gen_stats4.grid(row=0, column=0, sticky="w")

    fix_button4 = ttk.Button(
        randgen_status_frame,
        text="fix gens",
        command=randgen_fix   # unchanged
    )
    fix_button4.grid(row=0, column=1, padx=20)

    gen_status4_label = tk.Label(
        randgen_status_frame,
        text="",
        font=("Arial", 13)
    )
    gen_status4_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 0))

    # --- Plasma Generator Status ---
    plasma_status_frame = tk.LabelFrame(
        stats_tab,
        text="Plasma Generator",
        font=("Arial", 14, "bold"),
        padx=20,
        pady=10
    )
    plasma_status_frame.pack(fill="x", padx=40, pady=10)

    plasma_gen_stats = tk.Label(
        plasma_status_frame,
        text=f"Produces {g_given8}/s",
        font=("Arial", 16)
    )
    plasma_gen_stats.grid(row=0, column=0, sticky="w")

    plasma_fix_button = ttk.Button(
        plasma_status_frame,
        text="fix gens",
        command=plasma_fix_wrapper
    )
    plasma_fix_button.grid(row=0, column=1, padx=20)

    plasma_status_label = tk.Label(
        plasma_status_frame,
        text="",
        font=("Arial", 13)
    )
    plasma_status_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 0))

    # --- Steam Generator Status ---
    steam_status_frame = tk.LabelFrame(
        stats_tab,
        text="Steam Generator",
        font=("Arial", 14, "bold"),
        padx=20,
        pady=10
    )
    steam_status_frame.pack(fill="x", padx=40, pady=10)

    steam_gen_stats = tk.Label(
        steam_status_frame,
        text=f"Produces {g_given11}/s",
        font=("Arial", 16)
    )
    steam_gen_stats.grid(row=0, column=0, sticky="w")

    steam_fix_button = ttk.Button(
        steam_status_frame,
        text="fix gens",
        command=steam_fix_wrapper
    )
    steam_fix_button.grid(row=0, column=1, padx=20)

    steam_status_label = tk.Label(
        steam_status_frame,
        text="",
        font=("Arial", 13)
    )
    steam_status_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 0))

    # --- Void Generator Status ---
    void_status_frame = tk.LabelFrame(
        stats_tab,
        text="Void Generator",
        font=("Arial", 14, "bold"),
        padx=20,
        pady=10
    )
    void_status_frame.pack(fill="x", padx=40, pady=10)

    void_gen_stats = tk.Label(
        void_status_frame,
        text=f"Produces {g_given9}/s",
        font=("Arial", 16)
    )
    void_gen_stats.grid(row=0, column=0, sticky="w")

    void_fix_button = ttk.Button(
        void_status_frame,
        text="fix gens",
        command=void_fix_wrapper
    )
    void_fix_button.grid(row=0, column=1, padx=20)

    void_status_label = tk.Label(
        void_status_frame,
        text="",
        font=("Arial", 13)
    )
    void_status_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 0))

    # --- Chronos Generator Status ---
    chronos_status_frame = tk.LabelFrame(
        stats_tab,
        text="Chronos Generator",
        font=("Arial", 14, "bold"),
        padx=20,
        pady=10
    )
    chronos_status_frame.pack(fill="x", padx=40, pady=10)

    chronos_gen_stats = tk.Label(
        chronos_status_frame,
        text=f"Produces {g_given10}/s",
        font=("Arial", 16)
    )
    chronos_gen_stats.grid(row=0, column=0, sticky="w")

    chronos_fix_button = ttk.Button(
        chronos_status_frame,
        text="fix gens",
        command=chronos_fix_wrapper
    )
    chronos_fix_button.grid(row=0, column=1, padx=20)

    chronos_status_label = tk.Label(
        chronos_status_frame,
        text="",
        font=("Arial", 13)
    )
    chronos_status_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 0))

    # Electricity Status
    elec_status_frame = tk.LabelFrame(
    stats_tab,
    text="Electricity",
    font=("Arial", 14, "bold"),
    padx=20,
    pady=10
    )
    elec_status_frame.pack(fill="x", padx=40, pady=10)

    elec_label = tk.Label(
        elec_status_frame,
        text="Electricity Status:",
        font=("Arial", 14)
    )
    elec_label.grid(row=0, column=0, sticky="w")

    elec_fix_button = ttk.Button(
        elec_status_frame,
        text="Restart Elec",
        command=elec_fix   # unchanged
    )
    elec_fix_button.grid(row=0, column=1, padx=20)

    # Exit Button
    exit_button = ttk.Button(stats_tab, text="Exit Menu", command=win.destroy)
    exit_button.pack()

    # Helper function to get status for a list
    def get_gen_status(gen_list):
        if not gen_list:
            return "Status: N/A"
        
        broken_count = sum(1 for gen in gen_list if not getattr(gen, "running", False))
        
        if broken_count > 0:
            return f"Status: BROKEN ({broken_count} broken)"
        else:
            return f"Status: RUNNING ({len(gen_list)} running)"

    def gen_update():
        # Update production rates
        gen_stats.config(text=f"Standard Generator\nProduces {g_given1}/s")
        gen_stats2.config(text=f"Massive Generator\nProduces {g_given2}/s")
        gen_stats3.config(text=f"Industrial Generator\nProduces {g_given3}/s")
        gen_status_label.config(text=get_gen_status(gen_list))
        gen_status2_label.config(text=get_gen_status(bgen_list))
        gen_status3_label.config(text=get_gen_status(igen_list))
        gen_status4_label.config(text=get_gen_status(randgen_list))
        
        # Update advanced generator statuses
        plasma_gen_stats.config(text=f"Plasma Generator\nProduces {g_given8}/s")
        plasma_status_label.config(text=get_gen_status(plasma_list))
        steam_gen_stats.config(text=f"Steam Generator\nProduces {g_given11}/s")
        steam_status_label.config(text=get_gen_status(steam_list))
        void_gen_stats.config(text=f"Void Generator\nProduces {g_given9}/s")
        void_status_label.config(text=get_gen_status(void_list))
        chronos_gen_stats.config(text=f"Chronos Generator\nProduces {g_given10}/s")
        chronos_status_label.config(text=get_gen_status(chronos_list))

        # Schedule again
        win.after(500, gen_update)

    def elec_update():
        if not elec:
            elec_label.config(text="Electricity Status: NOT FINE")
            elec_fix_button.config(state=tk.NORMAL)
            gen_status_label.config(text=f"Status: NO POWER ({len(gen_list)} affected)")
            gen_status2_label.config(text=f"Status: NO POWER ({len(bgen_list)} affected)")
            gen_status3_label.config(text=f"Status: NO POWER ({len(igen_list)} affected)")
            gen_status4_label.config(text=f"Status: NO POWER ({len(igen_list)} affected)")
        else:
            elec_label.config(text="Electricity Status: FINE")
            elec_fix_button.config(state=tk.DISABLED)
            # Update status again (in case power was off before)
            gen_status_label.config(text=get_gen_status(gen_list))
            gen_status2_label.config(text=get_gen_status(bgen_list))
            gen_status3_label.config(text=get_gen_status(igen_list))

        # Schedule again
        win.after(500, elec_update)
    gen_update()
    elec_update()
def options():
    def darktheme():
        global click2
        click2 += 1
        if click2 % 2 == 1:  # Odd clicks: Enable dark mode
            sv_ttk.set_theme("dark")
            style.configure("TButton",
                            foreground="white",  # white text for dark mode
                            font=("Arial", 12),
                            padding=(5,10,5,10))
            darktheme_button.config(text="Enable Dark Theme: On")
        else:  # Even clicks: back to light mode
            sv_ttk.set_theme("light")
            style.configure("TButton",
                            foreground="black",  # default/dark text for light mode
                            font=("Arial", 12),
                            padding=(5,10,5,10))
            darktheme_button.config(text="Enable Dark Theme: Off")

    settings_window = tk.Toplevel(root)
    settings_window.geometry("500x400")
    darktheme_button = ttk.Button(settings_window, text = "Enable Dark Theme", command = darktheme)
    darktheme_button.place(relx=0.5, y=50, anchor='center')

root = tk.Tk()
root.title("MONOCLICKER")
root.attributes('-fullscreen', True)

# Configure button theme
style = ttk.Style()
style.configure("TButton", foreground="black", font=("Arial", 12), padding=(5, 10, 5, 10))

# Exit/enter fullscreen on ESC press
def exit_fullscreen(event=None):
    root.attributes('-fullscreen', False)

def enter_fullscreen(event=None):
    root.attributes('-fullscreen', True)

root.bind('<Escape>', exit_fullscreen)
root.bind('<F11>', enter_fullscreen)

# Main container with left and right panels
main_container = tk.Frame(root)
main_container.pack(fill="both", expand=True, padx=10)

# --- LEFT PANEL: Player Stats ---
left_panel = tk.Frame(main_container)
left_panel.pack(side="left", fill="y", padx=10)

player_stats_frame = tk.LabelFrame(left_panel, text="Player Stats", font=("Cascadia Code", 14, "bold"), padx=15, pady=10)
player_stats_frame.pack(fill="both", expand=True)

# Player stats labels
stats_g_label = tk.Label(player_stats_frame, text=f"Gold: {format(g)}G", font=("Arial", 14))
stats_g_label.pack(anchor="w", pady=2)

stats_gps_label = tk.Label(player_stats_frame, text=f"GPS: {format(round(g_given1 + g_given2 + g_given3, 2))}G/s", font=("Arial", 12))
stats_gps_label.pack(anchor="w", pady=2)

stats_level_label = tk.Label(player_stats_frame, text=f"Level: {level}", font=("Arial", 12))
stats_level_label.pack(anchor="w", pady=2)

stats_exp_label = tk.Label(player_stats_frame, text=f"EXP: {int(current_exp)}/{int(next_level_exp)}", font=("Arial", 12))
stats_exp_label.pack(anchor="w", pady=2)

stats_click_label = tk.Label(player_stats_frame, text=f"Click Power: {clickg}G", font=("Arial", 12))
stats_click_label.pack(anchor="w", pady=2)

stats_total_g_label = tk.Label(player_stats_frame, text=f"Total Earned: {format(total_g_earned)}G", font=("Arial", 12))
stats_total_g_label.pack(anchor="w", pady=2)

stats_total_clicks_label = tk.Label(player_stats_frame, text=f"Total Clicks: {total_clicks}", font=("Arial", 12))
stats_total_clicks_label.pack(anchor="w", pady=2)

# Generator counts
stats_gen_label = tk.Label(player_stats_frame, text=f"Standard Gens: {len(gen_list)}", font=("Arial", 11))
stats_gen_label.pack(anchor="w", pady=2)

stats_bgen_label = tk.Label(player_stats_frame, text=f"Massive Gens: {len(bgen_list)}", font=("Arial", 11))
stats_bgen_label.pack(anchor="w", pady=2)

stats_igen_label = tk.Label(player_stats_frame, text=f"Industrial Gens: {len(igen_list)}", font=("Arial", 11))
stats_igen_label.pack(anchor="w", pady=2)

stats_randgen_label = tk.Label(player_stats_frame, text=f"Random Gens: {len(randgen_list)}", font=("Arial", 11))
stats_randgen_label.pack(anchor="w", pady=2)

stats_ngen_label = tk.Label(player_stats_frame, text=f"Random Gens: {len(ngen_list)}", font=("Arial", 11))
stats_ngen_label.pack(anchor="w", pady=2)

stats_qgen_label = tk.Label(player_stats_frame, text=f"Random Gens: {len(qgen_list)}", font=("Arial", 11))
stats_qgen_label.pack(anchor="w", pady=2)

stats_fgen_label = tk.Label(player_stats_frame, text=f"Random Gens: {len(fgen_list)}", font=("Arial", 11))
stats_fgen_label.pack(anchor="w", pady=2)

stats_plasmagen_label = tk.Label(player_stats_frame, text=f"Random Gens: {len(plasma_list)}", font=("Arial", 11))
stats_plasmagen_label.pack(anchor="w", pady=2)

stats_steamgen_label = tk.Label(player_stats_frame, text=f"Random Gens: {len(steam_list)}", font=("Arial", 11))
stats_steamgen_label.pack(anchor="w", pady=2)

stats_voidgen_label = tk.Label(player_stats_frame, text=f"Random Gens: {len(void_list)}", font=("Arial", 11))
stats_voidgen_label.pack(anchor="w", pady=2)

stats_chrongen_label = tk.Label(player_stats_frame, text=f"Random Gens: {len(chronos_list)}", font=("Arial", 11))
stats_chrongen_label.pack(anchor="w", pady=2)


# Function to update player stats
def update_player_stats():
    stats_g_label.config(text=f"Gold: {format(g)}G")
    total_gps = sum([x.running for x in gen_list if isinstance(x, Generator)]) * g_given1
    total_gps += sum([x.running for x in gen_list if isinstance(x, BetterGenerator)]) * g_given2
    total_gps += sum([x.running for x in gen_list if isinstance(x, IndusGenerator)]) * g_given3
    total_gps += sum([x.running for x in gen_list if isinstance(x, RandGenerator)]) * g_given4 * gen_chance
    stats_gps_label.config(text=f"GPS: {format(round(total_gps, 2))}G/s")
    stats_level_label.config(text=f"Level: {level}")
    stats_exp_label.config(text=f"EXP: {int(current_exp)}/{int(next_level_exp)}")
    stats_click_label.config(text=f"Click Power: {clickg}G")
    stats_total_g_label.config(text=f"Total Earned: {format(total_g_earned)}G")
    stats_total_clicks_label.config(text=f"Total Clicks: {total_clicks}")
    stats_gen_label.config(text=f"Standard Gens: {len(gen_list)}")
    stats_bgen_label.config(text=f"Massive Gens: {len(bgen_list)}")
    stats_igen_label.config(text=f"Industrial Gens: {len(igen_list)}")
    stats_randgen_label.config(text=f"Random Gens: {len(randgen_list)}")
    root.after(500, update_player_stats)

# --- RIGHT PANEL: Rotating Upgrades ---
right_panel = tk.Frame(main_container)
right_panel.pack(side="right", fill="y", padx=10)

rotating_upgrades_frame = tk.LabelFrame(right_panel, text="Rotating Upgrades", font=("Cascadia Code", 14, "bold"), padx=15, pady=10)
rotating_upgrades_frame.pack(fill="both", expand=True)

# Rotation timer label
rotation_timer_label = tk.Label(rotating_upgrades_frame, text="Next rotation: 10:00", font=("Arial", 11), fg="blue")
rotation_timer_label.pack(pady=5)

# Container for upgrade buttons
upgrades_container = tk.Frame(rotating_upgrades_frame)
upgrades_container.pack(fill="both", expand=True)

# Current rotating upgrades display
current_upgrade_labels = []

def get_current_rotations():
    """Get the current set of upgrades to display based on rotation"""
    global next_rotation_time, current_rotation_index
    rotations = []
    current_time = time.time()
    
    if next_rotation_time == 0 or current_time >= next_rotation_time:
        # Time to rotate
        next_rotation_time = current_time + 600  # 10 minutes from now
        current_rotation_index = random.randint(0, len(rotating_upgrades) - 1)
    
    # Show 3 consecutive upgrades starting from current index
    for i in range(3):
        idx = (current_rotation_index + i) % len(rotating_upgrades)
        rotations.append(rotating_upgrades[idx])
    
    return rotations

def purchase_upgrade(upgrade_index):
    """Purchase a rotating upgrade"""
    global g, music_player_unlocked
    current_rotations = get_current_rotations()
    if upgrade_index >= len(current_rotations):
        return
    
    upgrade = current_rotations[upgrade_index]
    cost = upgrade["cost"]
    
    if g >= cost:
        g -= cost
        g_label.config(text=f"{format(g)}G")
        
        # Special handling for Music Player Unlock
        if upgrade["name"] == "Music Player Unlock":
            if music_player_unlocked:
                messagebox.showinfo("Already Unlocked", "You already have the Music Player!")
                g += cost  # Refund
                g_label.config(text=f"{format(g)}G")
                return
            music_player_unlocked = True
            add_log("Music Player unlocked!")
            messagebox.showinfo("Music Player Unlocked!", "Congratulations! You can now use the music player in the settings menu.")
        else:
            # Regular timed upgrade
            active_upgrades.append({
                "name": upgrade["name"],
                "effect": upgrade["effect"],
                "end_time": time.time() + upgrade["duration"] if upgrade["duration"] > 0 else 0
            })
            add_log(f"Purchased upgrade: {upgrade['name']}")
            messagebox.showinfo("Upgrade Purchased!", f"{upgrade['name']}\n\nEffect: {upgrade['effect']}")
    else:
        messagebox.showerror("Not Enough Gold", f"You need {format(cost)}G to purchase this upgrade!")

def update_rotating_upgrades_display():
    """Update the rotating upgrades display"""
    current_time = time.time()
    
    # Update rotation timer
    if next_rotation_time > current_time:
        time_left = int(next_rotation_time - current_time)
        minutes = time_left // 60
        seconds = time_left % 60
        rotation_timer_label.config(text=f"Next rotation: {minutes:02d}:{seconds:02d}")
    else:
        rotation_timer_label.config(text="Next rotation: 00:00")
    
    # Clear old upgrade widgets
    for widget in upgrades_container.winfo_children():
        widget.destroy()
    
    # Get and display current rotations
    current_rotations = get_current_rotations()
    
    for i, upgrade in enumerate(current_rotations):
        upgrade_frame = tk.Frame(upgrades_container, relief="ridge", bd=2, padx=5, pady=5)
        upgrade_frame.pack(fill="x", pady=3)
        
        name_label = tk.Label(upgrade_frame, text=upgrade["name"], font=("Arial", 11, "bold"), wraplength=150)
        name_label.pack(anchor="w")
        
        effect_label = tk.Label(upgrade_frame, text=upgrade["effect"], font=("Arial", 9), wraplength=150, fg="gray")
        effect_label.pack(anchor="w")
        
        cost_label = tk.Label(upgrade_frame, text=f"Cost: {format(upgrade['cost'])}G", font=("Arial", 10, "bold"), fg="green")
        cost_label.pack(anchor="w")
        
        buy_button = ttk.Button(upgrade_frame, text="BUY", command=lambda idx=i: purchase_upgrade(idx))
        buy_button.pack(pady=3)
    
    # Schedule next update
    root.after(1000, update_rotating_upgrades_display)

# --- CENTER PANEL: Main Game ---
center_panel = tk.Frame(main_container)
center_panel.pack(side="left", fill="both", expand=True, padx=10)

# Disabled buttons when elec is down
def elec_checker():
    global elec
    if elec == False:
        button.config(state = tk.DISABLED)
        shop_button.config(state = tk.DISABLED)
    else:
        button.config(state = tk.NORMAL)
        shop_button.config(state = tk.NORMAL)
    root.after(100, lambda: elec_checker())

# Header
header = ttk.Label(center_panel, text="MONOCLICKER", font=("Cascadia Code", 19, "bold"))
header.pack(pady=(20, 10))

# Function to increase g
def click():
    global g, total_clicks, total_g_earned
    global clickg
    total_clicks += 1
    g += clickg
    total_g_earned += clickg
    add_log(f"Increased G by {clickg}")
    gain_exp(clickg)
    g_label.config(text=f"{g:,.2f}G")  # Two decimals, commas for thousands

# Taxes mechanic labels
tax_frame = tk.Frame(center_panel, bg=root.cget('bg'), highlightthickness=0, bd=0)

message_label = tk.Label(tax_frame, text = "TIME LEFT BEFORE TAXES", font = ("Arial",14), fg = "#FF0000")
message_label.pack(anchor = "center", pady = (3, 0))

tax_time_label = tk.Label(tax_frame, text = f"", font = ("Arial",16), fg = "#FF0000")
tax_time_label.pack(anchor = "center", pady = (4, 0))

tax_frame.pack(side="top", anchor="n", pady=(10, 0))
#tax functions
def tax_collect():
    global g
    messagebox.showerror('Taxes', 'Haha money go bye bye')
    g -= g * 0.25  # Decrease g by 15%
    g = int(g)      # Optional: convert to integer if needed
    g_label.config(text = f"{format(g)}G")
# Log
log_console = tk.Text(center_panel, height=10, width=100, state='disabled',
                      bg='black', fg='white', font=("Consolas", 10))
log_console.pack_forget()  # Hide in main window

def add_log(message):
    timestamp = time.strftime("[%H:%M:%S]")
    log_console.config(state='normal')
    log_console.insert('end', f"{timestamp} {message}\n")
    log_console.see('end')
    log_console.config(state='disabled')

add_log("Game initialized. Waiting for player actions...")

# --- LOG WINDOW FUNCTION ---
def open_log_window():
    log_window = tk.Toplevel(root)
    log_window.title("Game Log")
    log_window.geometry("600x400")
    log_display = tk.Text(log_window, height=15, width=80, state='disabled',
                          bg='black', fg='white', font=("Consolas", 10))
    log_display.pack(padx=10, pady=10)

    def update_log_display():
        log_display.config(state='normal')
        log_display.delete(1.0, tk.END)
        log_display.insert(tk.END, log_console.get(1.0, tk.END))  # Sync logs
        log_display.config(state='disabled')
        log_window.after(1000, update_log_display)  # Update every second
    update_log_display()

    log_quit = ttk.Button(log_window, text = "Stop Logging", command = log_window.destroy)
    log_quit.pack(padx = 10, pady = 10)

    root.after(100, lambda: log_window.deiconify())

# --- LOG BUTTON ---
log_button = ttk.Button(center_panel, text="View Log", command=open_log_window)
log_button.place(x=20, y=20)

# G display
# A function that formats the G display
def format(value):
    suffixes = [
        (1_000_000_000_000_000_000, "Qn"),  # Quintillion
        (1_000_000_000_000_000, "Q"),       # Quadrillion
        (1_000_000_000_000, "T"),           # Trillion
        (1_000_000_000, "B"),               # Billion
        (1_000_000, "M"),                   # Million
        (1_000, "K"),                       # Thousand
    ]
    for threshold, suffix in suffixes:
        if value >= threshold:
            return f"{value / threshold:.2f}{suffix}"
    return f"{value:.2f}"

g_frame = tk.Frame(center_panel, bg=root.cget('bg'), highlightthickness=0, bd=0)
g_frame.pack(pady=(0, 10))
g_label = tk.Label(g_frame, text=f"{format(g)}G", font=("Cascadia Code", 50))
g_label.pack(anchor="center")
gps_label = tk.Label(g_frame, text=f"{format(round(g_given1 + g_given2 + g_given3, 2))}G/s", font=("Arial", 16))
gps_label.pack(anchor="center", pady=(2, 0))
def update_gps():
    total = len([x for x in gen_list if isinstance(x, Generator) and x.running]) * g_given1
    total += len([x for x in gen_list if isinstance(x, BetterGenerator) and x.running]) * g_given2
    total += len([x for x in gen_list if isinstance(x, IndusGenerator) and x.running]) * g_given3
    # Randomly fluctuate g_given4 by ±20% each update
    fluctuated_g4 = g_given4 * random.uniform(0.8, 1.2)
    total += len([x for x in gen_list if isinstance(x, RandGenerator) and x.running]) * fluctuated_g4
    gps_label.config(text=f"{format(round(total, 2))}G/s")
    root.after(500, update_gps)
update_gps()

# TAX TIMER
timer_job = None  # Store job reference

def update_timer():
    global taxtime, mus, g, elec, timer_job
    if taxtime > 0:
        minutes, seconds = divmod(taxtime, 60)
        tax_time_label.config(text=f"{minutes:02d}:{seconds:02d}")
        if taxtime % 50 == 0:
            add_log(f"current TaxTime: {minutes:02d}:{seconds:02d}")
        if taxtime == 8:
            sound4.play()
        taxtime -= 1
        timer_job = root.after(1000, update_timer)
    else:
        tax_collect()
        add_log(f"Tax collected. Taken: {g - g*0.25} Remaining: {g}")
        tax_time_label.config(text="00:00")

        def reset_timer():
            global taxtime
            taxtime = 5 * 60
            tax_time_label.config(text="05:00")
            update_timer()
        timer_job = root.after(1000, reset_timer)
update_timer()
# Main action buttons
# --- Main button frame ---
main_frame = tk.Frame(center_panel, highlightthickness=0, bd=0)
main_frame.pack(pady=10, anchor="center", expand=True)

button = ttk.Button(main_frame, text=f"Increase G ({clickg})", command=click, style = "Custom.TButton")
button.grid(row=0, column=2, padx=10, pady=5)

# Helper function for shop button
def shop_decision():
    if 'shop_window' in globals() and shop_window.winfo_exists():
        shop_button.config(command=shop_window.deiconify)
    else:
        shop_button.config(command=shop)
    root.after(200, shop_decision)

shop_button = ttk.Button(main_frame, text="Shop", command=shop)
shop_button.grid(row=2, column=1, padx=10, pady=10)


stats_button = ttk.Button(main_frame, text="Gen Status & Upgrades", command=upgrade_and_stats)
stats_button.grid(row=2, column=2, padx=10, pady=10)

settings_button = ttk.Button(main_frame, text="Settings", command=options)
settings_button.grid(row=2, column=3, padx=10, pady=10)
# Music player button
def music_player():
        # Import and launch the AudioGUI from custom_mus module
        from custom_mus import AudioGUI
        # Create a new window for the music player
        music_window = tk.Toplevel(root)
        # Initialize the GUI in the new window
        gui = AudioGUI(music_window)
        # Handle the window close event through the GUI's on_closing method
        music_window.protocol("WM_DELETE_WINDOW", gui.on_closing)
def if_mus_unlock():
    if not music_player_unlocked:
        custom_mus_button.config(state=tk.DISABLED,text = "Music Player Locked")
    else:
        custom_mus_button.config(state=tk.ACTIVE,text = "Open Dedicated Music Player")
custom_mus_button = ttk.Button(main_frame, text = "Open Dedicated Music Player", command = music_player)
custom_mus_button.grid(row=3,column=2,padx=10,pady=10)
quit_button = ttk.Button(main_frame, text="Quit Game", command=root.destroy)
quit_button.grid(row=4, column=2, padx=10, pady=10)

# Exp labels and stuff

level_frame = tk.Frame(center_panel, bg=root.cget('bg'), highlightthickness=0, bd=0)
level_frame.pack(pady=(0, 10))

level_label = tk.Label(level_frame, text=f"Level: {level}", font=("Cascadia Code", 20))
level_label.pack()

level_amnt_label = tk.Label(level_frame, text = f"{current_exp}/{next_level_exp}", font = ("Cascadia Code", 16))
level_amnt_label.pack()

level_vis = ttk.Progressbar(level_frame, orient="horizontal", mode="determinate", length=300)
level_vis.pack()

level_vis['maximum'] = next_level_exp
level_vis['value'] = current_exp
g = 10
def gain_exp(amount):
    global current_exp, next_level_exp, level
    current_exp = round(current_exp + amount, 2)  # Prevent tail growth

    # Update progress bar and label (2 decimals)
    level_vis['value'] = current_exp
    level_amnt_label.config(text=f"{int(current_exp)}/{int(next_level_exp)}")

    # Level-up check
    if current_exp >= next_level_exp:
        current_exp -= next_level_exp
        level += 1
        next_level_exp = level * 100
        if level >= 25:
            level_label.config(text=f"Level: {level} (I)")
        elif level >= 50:
            level_label.config(text=f"Level: {level} (II)")
        elif level >= 75:
            level_label.config(text=f"Level: {level} (III)")
        elif level >= 100:
            level_label.config(text=f"Level: {level} (IV)")
        else:
            level_label.config(text=f"Level: {level}")
        level_vis['maximum'] = next_level_exp
        level_vis['value'] = current_exp
def check_value(amount):
    global current_exp, next_level_exp, level
    current_exp = round(current_exp + amount, 2)  # Prevent tail growth

    # Update progress bar and label (2 decimals)
    level_vis['value'] = current_exp
    level_amnt_label.config(text=f"{int(current_exp)}/{int(next_level_exp)}")

    # Level-up check
    if current_exp >= next_level_exp:
        current_exp -= next_level_exp
        level += 1
        next_level_exp = level * 100
        if level >= 25:
            level_label.config(text=f"Level: {level} (I)")
        elif level >= 50:
            level_label.config(text=f"Level: {level} (II)")
        elif level >= 75:
            level_label.config(text=f"Level: {level} (III)")
        elif level >= 100:
            level_label.config(text=f"Level: {level} (IV)")
        else:
            level_label.config(text=f"Level: {level}")
        level_vis['maximum'] = next_level_exp
        level_vis['value'] = current_exp

# Pro tip at the bottom
pro_tip = ttk.Label(center_panel, text="Pro Tip:", font=("Cascadia Code", 10))
pro_tip.pack(side="bottom", pady=10)

def pro_tip_text():
    tips = [
        "Generators need to be fixed twice after a blackout.",
        "Dont gamble, its bad.",
        "Upgrade your generators for better production.",
        "Check the generator status in the stats menu.",
        "Restock your shop to buy more generators.",
        "Use the settings menu to toggle dark mode and music.",
        "Also try Cookie Clicker!",
        "Jibrael, if ur reading this, check for bugs ty :>",
        "Its very easy to mod this game, just read the code!",
        "Cheated G isnt good G.",
        "If you dont see your save progress, press the load button.",
        "If you're wondering, yes, you can edit your save file.",
        "Touch. Grass.",
        "I actually cant check the time, maybe Bastijn might add that soon...",
        "Also try Game Dev Tycoon!",
        "This game takes a while to complete.",
        "This video is sponsored by Raid Shadow Legends. Raid Shadow Legends is a free-to-play turn-based RPG with over 600 champions to collect and upgrade. Download it now using the link in the description!",
        "ERR: Variable 'iq' not found. Please check your mindset.",
        "Achievements are coming soon!",
        "If the Generator Status is still BROKEN, keep on fixing!",
        "Remember to SAVE (and load) your game!",
        "Man, I sure do hope lyrics from a niche Japanese song don't show up!",
        "This Game is JIBRAEL Approved :D",
        "Bastijn Please Give us a background - jib",
        "Does this count as helping? - jib",
        """沈むように溶けてゆくように
        二人だけの空が広がる夜に
        「さよなら」だけだった
        その一言で全てが分かった
        日が沈み出した空と君の姿
        フェンス越しに重なっていた
        初めて会った日から
        僕の心の全てを奪った
        どこか儚い空気を纏う君は
        寂しい目をしてたんだ
        いつだってチックタックと
        鳴る世界で何度だってさ
        触れる心無い言葉うるさい声に
        涙が零れそうでも
        ありきたりな喜びきっと二人なら見つけられる
        騒がしい日々に笑えない君に
        思い付く限り眩しい明日を
        明けない夜に落ちてゆく前に
        僕の手を掴んでほら
        忘れてしまいたくて閉じ込めた日々も
        抱きしめた温もりで溶かすから
        怖くないよいつか日が昇るまで
        二人でいよう
        君にしか見えない
        何かを見つめる君が嫌いだ
        見惚れているかのような恋するような
        そんな顔が嫌いだ
        信じていたいけど信じれないこと
        そんなのどうしたってきっと
        これからだって いくつもあって
        そのたんび怒って 泣いていくの
        それでもきっといつかはきっと 僕らはきっと
        分かり合えるさ 信じてるよ
        もう嫌だって疲れたんだって
        がむしゃらに差し伸べた 僕の手を振り払う君
        もう嫌だって 疲れたよなんて
        本当は僕も言いたいんだ
        Ah ほらまたチックタックと
        鳴る世界で何度だってさ
        君の為に用意した言葉 どれも届かない
        「終わりにしたい」 だなんてさ
        釣られて言葉にした時
        君は初めて笑った
        騒がしい日々に笑えなくなっていた
        僕の目に映る君は綺麗だ
        明けない夜に零れた涙も
        君の笑顔に溶けていく
        変わらない日々に泣いていた僕を
        君は優しく終わりへと誘う
        沈むように溶けてゆくように
        染み付いた霧が晴れる
        忘れてしまいたくて閉じ込めた日々に
        差し伸べてくれた君の手を取る
        涼しい風が空を泳ぐように今 吹き抜けていく
        繋いだ手を離さないでよ
        二人いま 夜に駆け出していく - Jibrael """,
        "Hello I am Jibby-Rael, the raeliest.",
        "We love capitalism, can you say you love capitalism?",
        "Toilet of Skibidi Perhaps?",
        "Check out the new music player in the settings! Its buggy tho..."
    ]
    tip = random.choice(tips)
    pro_tip.config(text=f"Pro tip: {tip}")
    root.after(5000, pro_tip_text)
def save_game():
    global taxtime, g, clickg, gen_price, gen_shop_amnt, gen_amnt, g_given1, gen_lvl, upgrade_cost
    global bgen_price, bgen_shop_amnt, bgen_amnt, g_given2, gen_lvl2, upgrade_cost2
    global gen_stock, bgen_stock, igen_stock, randgen_stock
    global gen_list, bgen_list, igen_list, randgen_list
    global gen_lvl3, g_given3, upgrade_cost3, igen_price, igen_shop_amnt, igen_amnt
    global level, next_level_exp, current_exp
    global randgen_price, randgen_shop_amnt, randgen_amnt, g_given4, gen_lvl4, upgrade_cost4, gen_chance
    global total_g_earned, total_clicks, next_rotation_time, current_rotation_index, active_upgrades, music_player_unlocked
    save_data = {
        "g": g,
        "current_exp": current_exp,
        "next_level_exp": next_level_exp,
        "level": level,
        "taxtime": taxtime,
        "clickg": clickg,
        "gen_price": gen_price,
        "gen_shop_amnt": gen_shop_amnt,
        "gen_amnt": gen_amnt,
        "g_given1": g_given1,
        "gen_lvl": gen_lvl,
        "upgrade_cost": upgrade_cost,
        "bgen_price": bgen_price,
        "bgen_shop_amnt": bgen_shop_amnt,
        "bgen_amnt": bgen_amnt,
        "g_given2": g_given2,
        "gen_lvl2": gen_lvl2,
        "upgrade_cost2": upgrade_cost2,
        "gen_stock": gen_stock,
        "bgen_stock": bgen_stock,
        "igen_stock": igen_stock,
        "gen_count": len(gen_list),
        "bgen_count": len(bgen_list),
        "igen_count": len(igen_list),
        "gen_lvl3": gen_lvl3,
        "g_given3": g_given3,
        "upgrade_cost3": upgrade_cost3,
        "igen_price": igen_price,
        "igen_shop_amnt": igen_shop_amnt,
        "igen_amnt": igen_amnt,
        "randgen_amnt": randgen_amnt,
        "randgen_count": len(randgen_list),
        "randgen_price": randgen_price,
        "randgen_shop_amnt": randgen_shop_amnt,
        "randgen_stock": randgen_stock,
        "g_given4": g_given4,
        "gen_lvl4": gen_lvl4,
        "upgrade_cost4": upgrade_cost4,
        "gen_chance": gen_chance,
        "total_g_earned": total_g_earned,
        "total_clicks": total_clicks,
        "next_rotation_time": next_rotation_time,
        "current_rotation_index": current_rotation_index,
        "active_upgrades": active_upgrades,
        "music_player_unlocked": music_player_unlocked
    }
    save_path = os.path.join(BASE_DIR, "savegame.json")
    try:
        with open(save_path, "w") as f:
            json.dump(save_data, f)
        save_label.config(text="Game saved!")
        root.after(1000, lambda: save_label.config(text = ""))
    except Exception as e:
        save_label.config(text=f"Save failed: {str(e)}")
        add_log(f"Save error: {str(e)}")

def load_game():
    global g, clickg, gen_price, gen_shop_amnt, gen_amnt, g_given1, gen_lvl, upgrade_cost
    global bgen_price, bgen_shop_amnt, bgen_amnt, g_given2, gen_lvl2, upgrade_cost2
    global gen_stock, bgen_stock, igen_stock
    global gen_list, bgen_list, igen_list
    global gen_lvl3, g_given3, upgrade_cost3, igen_price, igen_shop_amnt, igen_amnt
    global level, next_level_exp, current_exp
    global randgen_price, randgen_shop_amnt, randgen_amnt, randgen_list, g_given4, gen_lvl4, upgrade_cost4, gen_chance, randgen_stock
    global total_g_earned, total_clicks, next_rotation_time, current_rotation_index, active_upgrades
    global plasma_list, steam_list, void_list, chronos_list, music_player_unlocked

    # Stop all existing generators to prevent EXP exploit from orphaned callbacks
    for gen in gen_list:
        gen.running = False
    for gen in bgen_list:
        gen.running = False
    for gen in igen_list:
        gen.running = False
    for gen in randgen_list:
        gen.running = False
    for gen in plasma_list:
        gen.running = False
    for gen in steam_list:
        gen.running = False
    for gen in void_list:
        gen.running = False
    for gen in chronos_list:
        gen.running = False

    gen_list = []
    bgen_list = []
    igen_list = []
    randgen_list = []

    save_path = os.path.join(BASE_DIR, "savegame.json")
    if os.path.exists(save_path):
        with open(save_path, "r") as f:
            save_data = json.load(f)

        # Restore values
        g = save_data.get("g", 0)
        taxtime = save_data.get("taxtime", 300)
        clickg = save_data.get("clickg", 1)
        gen_price = save_data.get("gen_price", 10)
        gen_shop_amnt = save_data.get("gen_shop_amnt", 1)
        gen_amnt = save_data.get("gen_amnt", 0)
        g_given1 = save_data.get("g_given1", 1)
        gen_lvl = save_data.get("gen_lvl", 1)
        upgrade_cost = save_data.get("upgrade_cost", 100)
        bgen_price = save_data.get("bgen_price", 100)
        bgen_shop_amnt = save_data.get("bgen_shop_amnt", 1)
        bgen_amnt = save_data.get("bgen_amnt", 0)
        g_given2 = save_data.get("g_given2", 10)
        gen_lvl2 = save_data.get("gen_lvl2", 1)
        upgrade_cost2 = save_data.get("upgrade_cost2", 200)
        gen_stock = save_data.get("gen_stock", 15)
        bgen_stock = save_data.get("bgen_stock", 10)
        igen_stock = save_data.get("igen_stock", 10)
        gen_lvl3 = save_data.get("gen_lvl3", 1)
        g_given3 = save_data.get("g_given3", 100)
        upgrade_cost3 = save_data.get("upgrade_cost3", 200)
        igen_price = save_data.get("igen_price", 250)
        igen_shop_amnt = save_data.get("igen_shop_amnt", 1)
        igen_amnt = save_data.get("igen_amnt", 0)
        current_exp = save_data.get("current_exp", 0) - save_data.get("current_exp", 0)
        next_level_exp = save_data.get("next_level_exp", 100)
        level = save_data.get("level", 1)
        randgen_price = save_data.get("randgen_price", 77.7)
        randgen_shop_amnt = save_data.get("randgen_shop_amnt", 1)
        randgen_amnt = save_data.get("randgen_amnt", 0)
        g_given4 = save_data.get("g_given4", 100)
        gen_lvl4 = save_data.get("gen_lvl4", 1)
        upgrade_cost4 = save_data.get("upgrade_cost4", 777)
        gen_chance = save_data.get("gen_chance", 0.25)
        randgen_stock = save_data.get("randgen_stock", 7)
        total_g_earned = save_data.get("total_g_earned", 0)
        total_clicks = save_data.get("total_clicks", 0)
        next_rotation_time = save_data.get("next_rotation_time", 0)
        current_rotation_index = save_data.get("current_rotation_index", 0)
        active_upgrades = save_data.get("active_upgrades", [])
        music_player_unlocked = save_data.get("music_player_unlocked", False)
        
        level_label.config(text=f"Level: {level}")
        level_vis['maximum'] = next_level_exp
        level_vis['value'] = current_exp
        stats_exp_label.config(text=f"EXP: {int(current_exp)}/{int(next_level_exp)}")
        level_amnt_label.config(text=f"{int(current_exp)}/{int(next_level_exp)}")
        root.update()  # Force UI refresh to show loaded progress bar values
        # Re-create generators
        for _ in range(save_data.get("gen_count", 0)):
            gen_list.append(Generator(gen_lvl))
        for _ in range(save_data.get("bgen_count", 0)):
            bgen_list.append(BetterGenerator(gen_lvl2))
        for _ in range(save_data.get("igen_count", 0)):
            igen_list.append(IndusGenerator(gen_lvl3))
        for _ in range(save_data.get("randgen_count", 0)):
            randgen_list.append(RandGenerator(gen_lvl4))

        # --- UPDATE ALL LABELS ---
        g_label.config(text=f"{g:,.2f}G")  # Two decimals, commas for thousands
        gps_label.config(text=f"{(len(gen_list)*g_given1) + (len(bgen_list)*g_given2) + (len(igen_list)*g_given3)}G/s")
        
        # Update player stats panel if it exists
        if 'player_stats_frame' in globals():
            update_player_stats()
        
        # Update rotating upgrades if panel exists
        if 'rotating_upgrades_frame' in globals():
            update_rotating_upgrades_display()

        # If your shop or upgrade menu is open, update their labels too
        try:
            if 'gen_shop_price_label' in globals():
                gen_shop_price_label.config(text=f"Price: {gen_price}G")
            if 'bgen_shop_price_label' in globals():
                bgen_shop_price_label.config(text=f"Price: {bgen_price}G")
            if 'igen_shop_price_label' in globals():
                igen_shop_price_label.config(text=f"Price: {igen_price}G")
            if 'randgen_shop_price_label' in globals():
                randgen_shop_price_label.config(text=f"Price: {randgen_price}G")

            if 'gen_shop_amnt_label' in globals():
                gen_shop_amnt_label.config(text=f"Current amount: {len(gen_list)}")
            if 'bgen_shop_amnt_label' in globals():
                bgen_shop_amnt_label.config(text=f"Current amount: {len(bgen_list)}")
            if 'igen_shop_amnt_label' in globals():
                igen_shop_amnt_label.config(text=f"Current amount: {len(igen_list)}")
            if 'randgen_shop_amnt_label' in globals():
                randgen_shop_amnt_label.config(text=f"Current amount: {len(randgen_list)}")

            if 'gen_stock_label' in globals():
                gen_stock_label.config(text=f"Stock: {gen_stock}")
            if 'bgen_stock_label' in globals():
                bgen_stock_label.config(text=f"Stock: {bgen_stock}")
            if 'igen_stock_label' in globals():
                igen_stock_label.config(text=f"Stock: {igen_stock}")
            if 'randgen_stock_label' in globals():
                randgen_stock_label.config(text=f"Stock: {randgen_stock}")
        except NameError:
            pass  # Shop might not be open yet

        try:
            if 'stdgen_label' in globals():
                stdgen_label.config(text=f"Level: {gen_lvl}")
            if 'bgen_label' in globals():
                bgen_label.config(text=f"Level: {gen_lvl2}")
            if 'igen_label' in globals():
                igen_label.config(text=f"Level: {gen_lvl3}")
            if 'randgen_label' in globals():
                randgen_label.config(text=f"Level: {gen_lvl4}")

            if 'stdgen_button' in globals():
                stdgen_button.config(text=f"UPGRADE ({upgrade_cost}G)")
            if 'bgen_button' in globals():
                bgen_button.config(text=f"UPGRADE ({upgrade_cost2}G)")
            if 'igen_button' in globals():
                igen_button.config(text=f"UPGRADE ({upgrade_cost3}G)")
            if 'randgen_button' in globals():
                randgen_button.config(text=f"UPGRADE ({upgrade_cost4}G)")
        except NameError:
            pass  # Upgrade menu might not be open yet
        
        # Refresh the tax time
        minutes, seconds = divmod(taxtime, 60)
        tax_time_label.config(text=f"{minutes:02d}:{seconds:02d}")

        # Refresh Progress Exp
        check_value(g)
        save_label.config(text="Game loaded!")
        root.after(1000, lambda: save_label.config(text=""))

# Save/Load
save_frame = ttk.Frame(center_panel)

save_button = ttk.Button(save_frame, text="Save", command=save_game)
save_button.grid(row=0, column=0, padx=5)

load_button = ttk.Button(save_frame, text="Load", command=load_game)
load_button.grid(row=0, column=1, padx=5)

save_label = tk.Label(save_frame, text="", font=("Cascadia Code", 11))
save_label.grid(row=0, column=2, padx=5)

# Place in bottom-right corner with padding
save_frame.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

def toggle_mus():
    global mus, clicky, music_player_unlocked
    clicky += 1
    if not music_player_unlocked:
        messagebox.showinfo("Music Player Locked", "Unlock the Music Player upgrade first!")
        return
    if mus:
        mus = False
    else:
        mus = True
    if clicky == 2:
        clicky = 0

# Initialize PopupManager (after all UI elements are created)
popup_manager = None

def initialize_popup_manager():
    global popup_manager
    
    def get_money():
        return g

    def set_money(amount):
        global g
        g = amount
        g_label.config(text=f"{g:,.2f}G")

    def get_level():
        return level

    def set_level(new_level):
        global level
        level = new_level
        if level >= 25:
            level_label.config(text=f"Level: {level} (I)")
        elif level >= 50:
            level_label.config(text=f"Level: {level} (II)")
        elif level >= 75:
            level_label.config(text=f"Level: {level} (III)")
        elif level >= 100:
            level_label.config(text=f"Level: {level} (IV)")
        else:
            level_label.config(text=f"Level: {level}")

    popup_manager = PopupManager(root, get_money, set_money, get_level, set_level, sound8, sound9, sound10, sound11, root)
    popup_manager.schedule_popups()
# Initialize the electricity loop
electricity()
# Intialize the pro tip text
pro_tip_text()
load_game()  # Load da game at start
# Check that electricity
elec_checker()
initialize_popup_manager()  # Initialize popup system after all UI is ready

# Initialize player stats and rotating upgrades panels
update_player_stats()
update_rotating_upgrades_display()

# Check if player unlocked music player
if_mus_unlock()


root.mainloop()
