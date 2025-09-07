import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sv_ttk
import random
import json
import os
import music
import pygame
import time
from datetime import datetime, timedelta
clicky = 0
#guide for adding a new item:
#add its variables first: (price, shop amount, how much g it gives, its list, its starting lvl, and cost)
#add it as a buy option in shop()
#add it as an upgrade option in upgrade()
#add it to the generator stats in gen_stats()
#for music
mus = True
#starting g
g = 0
#g per click
clickg = 1
#time before tax is taken (5 minutes default)
taxtime = 300
#standard generators
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
randgen_price = 77.7
randgen_shop_amnt = 1
randgen_amnt = 0
randgen_list = []
g_given4 = 100
gen_lvl4 = 1
upgrade_cost4 = 777
gen_chance = 0.25
# Add stock variables at the top
gen_stock = 15        # Stock for standard generators
bgen_stock = 10        # Stock for massive generators
igen_stock = 10       # Stock for industrial generators
randgen_stock = 7     # Stock for chance_based generators
# thing to make the dark theme button work
click2 = 0
fixeth = 20 # amount of clicks needed to fix a generator
elec = True # electricity
firstshop = False # for first time shopping

# Exp for levels
level = 1
current_exp = 0
next_level_exp = 100  # G required for next level

# Get the absolute path to the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build paths for the sound files
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
pygame.mixer.init() #for sfx
sound1 = pygame.mixer.Sound(sound1_path)
sound2 = pygame.mixer.Sound(sound2_path)
sound3 = pygame.mixer.Sound(sound3_path)
sound4 = pygame.mixer.Sound(sound4_path)
sound5 = pygame.mixer.Sound(sound5_path)
sound6 = pygame.mixer.Sound(sound6_path)
sound7 = pygame.mixer.Sound(sound7_path)
# Basic Mechanics
def electricity():
    global elec
    if random.random() < 0.25:
        elec = False
class Generator():
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
            add_log(f"increased G by {g_given3}")
            root.after(1000, self.start_generating)

    def lvlup(self):
        global g_given3
        g_given3 = int(g_given3 * 1.15)
        return g_given3

    def mark_fixed(self):
        self.safe_until = time.time() + random.randint(60, 600)
        self.running = True
        self.off = False
        self.start_generating()

class RandGenerator():
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
            if random.random() < gen_chance:
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
def shop():
    global gen_price, gen_shop_amnt, gen_amnt
    global gen_stock, bgen_stock, igen_stock, randgen_stock
    global bgen_price, bgen_shop_amnt, bgen_amnt
    global igen_price, igen_shop_amnt, igen_amnt
    global randgen_price, randgen_amnt, randgen_shop_amnt
    global gen_list, bgen_list, igen_list, randgen_list
    global firstshop
    if firstshop == False:
        firstshop = True
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
        if random.random() < 0.777: # 77.7 chance to appear
            randgen_stock = random.randint(1, 5) # 1 or 2 in stock 
        else:
            randgen_stock = 0

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
        global g, randgen_price, randgen_shop_amnt, randgen_amnt, randgen_stock

        if g >= randgen_price * randgen_shop_amnt and randgen_shop_amnt <= randgen_stock:
            g -= randgen_price * randgen_shop_amnt
            g_label.config(text=f"{g:,.2f}G")  # Two decimals, commas for thousands
            shop_g.config(text=f"{format(g)}G")

            for i in range(randgen_shop_amnt):
                global newgen4
                newgen4 = RandGenerator(gen_lvl4)
                gen_list.append(newgen4)
                randgen_list.append(newgen4)

            randgen_amnt += randgen_shop_amnt
            randgen_stock -= randgen_shop_amnt  # Reduce stock
            randgen_shop_amnt = 1

            # Update labels properly
            randgen_shop_amnt_label.config(text=f"amount: {randgen_shop_amnt}")
            randgen_current_label.config(text=f"Current amount: {len(randgen_list)}", font=("Arial", 14))
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
    # --- Standard Generator Section ---
    std_frame = tk.LabelFrame(shop_window, text="Standard G Generator", font=("Arial", 18, "bold"), padx=20, pady=10)
    std_frame.pack(fill="x", padx=40, pady=10)
    
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
    bgen_frame = tk.LabelFrame(shop_window, text="Massive G Generator", font=("Arial", 18, "bold"), padx=20, pady=10)
    bgen_frame.pack(fill="x", padx=40, pady=10)

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
    igen_frame = tk.LabelFrame(shop_window, text="Industrial G Generator", font=("Arial", 18, "bold"), padx=20, pady=10)
    igen_frame.pack(fill="x", padx=40, pady=10)

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
    randgen_frame = tk.LabelFrame(shop_window, text="Randomized G Generator", font=("Arial", 18, "bold"), padx=20, pady=10)
    randgen_frame.pack(fill="x", padx=40, pady=10)

    randgen_item = tk.Label(randgen_frame, text=f"Randomized G Generator (1-{g_given4}G/s)", font=("Arial", 16))
    randgen_item.grid(row=0, column=0, sticky="w")

    def update_randgen_item():
        randgen_item.config(text=f"Randomized G Generator (1-{g_given4}G/s)")
        shop_window.after(500, update_randgen_item)

    update_randgen_item()
    ishop_amnt = tk.Label(randgen_frame, text=f"amount: {randgen_shop_amnt}", font=("Arial", 16))
    ishop_amnt.grid(row=0, column=1, padx=20)
    randgen_current_label = tk.Label(randgen_frame, text=f"Current amount: {len(randgen_list)}", font=("Arial", 16))
    randgen_current_label.grid(row=1, column=0, sticky="w")
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
    

    # --- Restock Button ---
    restock_button = ttk.Button(shop_window, text="Restock (100G)", command=restock)
    restock_button.pack(pady=30)

    close_button = ttk.Button(shop_window, text="Close Shop", command=shop_window.destroy)
    close_button.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)  # Top right corner with padding
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


        def update_timer():
            if success[0] >= success_needed:
                return
            time_left[0] -= 1
            timer_label.config(text=f"Time left: {time_left[0]}s")
            if time_left[0] <= 0:
                messagebox.ERROR('Aw man!', 'Probability unsuccessfully calibrated.')
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
        global gen_lvl, upgrade_cost, g_given1, g
        if g < upgrade_cost:
            stdgen_button.config(text="Not enough money")
            root.after(200, lambda: stdgen_button.config(text=f"UPGRADE ({upgrade_cost}G)"))
        else:
            g -= upgrade_cost
            if len(gen_list) == 0:
                return
            for newgen in gen_list:
                newgen.lvlup()
            gen_lvl += 1
            upgrade_cost = int(upgrade_cost * 1.75)
            g_label.config(text=f"{g:,.2f}G")  # Two decimals, commas for thousands
            stdgen_label.config(text=f"Level: {gen_lvl}")
            stdgen_button.config(text=f"UPGRADE ({upgrade_cost}G)")
    stdgen_button = ttk.Button(stdgen_frame, text=f"UPGRADE ({upgrade_cost}G)", command=upgrader)
    stdgen_button.grid(row=0, column=1, padx=20)

    # Massive Generator Upgrade
    bgen_frame = tk.LabelFrame(upgrade_tab, text="Massive Generator", font=("Arial", 14, "bold"), padx=20, pady=10)
    bgen_frame.pack(fill="x", padx=40, pady=10)
    bgen_label = tk.Label(bgen_frame, text=f"Level: {gen_lvl2}", font=("Arial", 16))
    bgen_label.grid(row=0, column=0, sticky="w")
    def upgrader2():
        global gen_lvl2, upgrade_cost2, g_given2, g
        if g < upgrade_cost2:
            bgen_button.config(text="Not enough money")
            root.after(200, lambda: bgen_button.config(text=f"UPGRADE ({upgrade_cost2}G)"))
        else:
            g -= upgrade_cost2
            if len(bgen_list) == 0:
                return
            for newgen2 in bgen_list:
                newgen2.lvlup()
            gen_lvl2 += 1
            upgrade_cost2 = int(upgrade_cost2 * 2.5)
            g_label.config(text=f"{g:,.2f}G")  # Two decimals, commas for thousands
            bgen_label.config(text=f"Level: {gen_lvl2}")
            bgen_button.config(text=f"UPGRADE ({upgrade_cost2}G)")
    bgen_button = ttk.Button(bgen_frame, text=f"UPGRADE ({upgrade_cost2}G)", command=upgrader2)
    bgen_button.grid(row=0, column=1, padx=20)

    # Industrial Generator Upgrade
    igen_frame = tk.LabelFrame(upgrade_tab, text="Industrial Generator", font=("Arial", 14, "bold"), padx=20, pady=10)
    igen_frame.pack(fill="x", padx=40, pady=10)
    igen_label = tk.Label(igen_frame, text=f"Level: {gen_lvl3}", font=("Arial", 16))
    igen_label.grid(row=0, column=0, sticky="w")
    def upgrader3():
        global gen_lvl3, upgrade_cost3, g_given3, g
        if g < upgrade_cost3:
            igen_button.config(text="Not enough G")
            root.after(200, lambda: igen_button.config(text=f"UPGRADE ({upgrade_cost3}G)"))
        else:
            g -= upgrade_cost3
            if len(igen_list) == 0:
                return
            for igen in igen_list:
                igen.lvlup()
            gen_lvl3 += 1
            upgrade_cost3 = int(upgrade_cost3 * 3)
            g_label.config(text=f"{g:,.2f}G")  # Two decimals, commas for thousands
            igen_label.config(text=f"Level: {gen_lvl3}")
            igen_button.config(text=f"UPGRADE ({upgrade_cost3}G)")
    igen_button = ttk.Button(igen_frame, text=f"UPGRADE ({upgrade_cost3}G)", command=upgrader3)
    igen_button.grid(row=0, column=1, padx=20)

    # Randomized Generator Upgrade
    randgen_frame = tk.LabelFrame(upgrade_tab, text="Randomized Generator", font=("Arial", 14, "bold"), padx=20, pady=10)
    randgen_frame.pack(fill="x", padx=40, pady=10)
    randgen_label = tk.Label(randgen_frame, text=f"Level: {gen_lvl4}", font=("Arial", 16))
    randgen_label.grid(row=0, column=0, sticky="w")
    def upgrader4():
        global gen_lvl4, upgrade_cost4, g_given4, g
        if g < upgrade_cost4:
            randgen_button.config(text="Not enough G")
            root.after(200, lambda: randgen_button.config(text=f"UPGRADE ({upgrade_cost4}G)"))
        else:
            g -= upgrade_cost4
            if len(randgen_list) == 0:
                return
            for randgen in randgen_list:
                randgen.lvlup()
            gen_lvl4 += 1
            upgrade_cost4 = int(upgrade_cost4 * 3)
            g_label.config(text=f"{g:,.2f}G")  # Two decimals, commas for thousands
            randgen_label.config(text=f"Level: {gen_lvl4}")
            randgen_button.config(text=f"UPGRADE ({upgrade_cost4}G)")
    randgen_button = ttk.Button(randgen_frame, text=f"UPGRADE ({upgrade_cost4}G)", command=upgrader4)
    randgen_button.grid(row=0, column=1, padx=20)

    close_button = ttk.Button(upgrade_tab, text="Close Window", command=win.destroy)
    close_button.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)

    # --- Generator Status Tab ---
    stats_tab = ttk.Frame(notebook)
    notebook.add(stats_tab, text="Generator Status")

    # Standard Generator
    gen_stats = ttk.Label(stats_tab, text=f"Standard Generator\nProduces {g_given1}/s", font=("Cascadia Code", 16))
    gen_stats.place(x=50, y=100)
    fix_button = ttk.Button(stats_tab, text="fix gens", command=generator_fix)
    fix_button.place(x=300, y=110)
    gen_status_label = ttk.Label(stats_tab, text="", font=("Arial", 13))
    gen_status_label.place(x=50, y=155)

    # Massive Generator
    gen_stats2 = ttk.Label(stats_tab, text=f"Massive Generator\nProduces {g_given2}/s", font=("Cascadia Code", 16))
    gen_stats2.place(x=50, y=180)
    fix_button2 = ttk.Button(stats_tab, text="fix gens", command=bgenerator_fix)
    fix_button2.place(x=300, y=190)
    gen_status2_label = ttk.Label(stats_tab, text="", font=("Arial", 13))
    gen_status2_label.place(x=50, y=235)

    # Industrial Generator
    gen_stats3 = ttk.Label(stats_tab, text=f"Industrial Generator\nProduces {g_given3}/s", font=("Cascadia Code", 16))
    gen_stats3.place(x=50, y=260)
    fix_button3 = ttk.Button(stats_tab, text="fix gens", command=igenerator_fix)
    fix_button3.place(x=300, y=270)
    gen_status3_label = ttk.Label(stats_tab, text="", font=("Arial", 13))
    gen_status3_label.place(x=50, y=315)

    # Randomized Generator
    gen_stats4 = ttk.Label(stats_tab, text=f"Randomized Generator\nProduces 1-{g_given4}/s", font=("Cascadia Code", 16))
    gen_stats4.place(x=50, y=340)
    fix_button4 = ttk.Button(stats_tab, text="fix gens", command=randgen_fix)
    fix_button4.place(x=300, y=350)
    gen_status4_label = ttk.Label(stats_tab, text="", font=("Arial", 13))
    gen_status4_label.place(x=50, y=395)

    # Electricity Status
    elec_label = ttk.Label(stats_tab, text="Electricity Status:", font=("Cascadia Code", 14))
    elec_label.place(relx=0.3, rely=0.8, anchor="center")
    elec_fix_button = ttk.Button(stats_tab, text="Restart Elec", command=elec_fix)
    elec_fix_button.place(relx=0.7, rely=0.8, anchor="center")

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

        # Schedule again
        win.after(500, gen_update)

    def elec_update():
        if not elec:
            elec_label.config(text="Electricity Status: NOT FINE")
            elec_fix_button.config(state=tk.NORMAL)
            gen_status_label.config(text=f"Status: NO POWER ({len(gen_list)} affected)")
            gen_status2_label.config(text=f"Status: NO POWER ({len(bgen_list)} affected)")
            gen_status3_label.config(text=f"Status: NO POWER ({len(igen_list)} affected)")
            gen_status4_label.config(text=f"Status: NO POWER ({len(randgen_list)} affected)")
        else:
            elec_label.config(text="Electricity Status: FINE")
            elec_fix_button.config(state=tk.DISABLED)
            # Update status again (in case power was off before)
            gen_status_label.config(text=get_gen_status(gen_list))
            gen_status2_label.config(text=get_gen_status(bgen_list))
            gen_status3_label.config(text=get_gen_status(igen_list))
            gen_status4_label.config(text=get_gen_status(randgen_list))

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
        else:  # Even clicks: back to light mode
            sv_ttk.set_theme("light")
            style.configure("TButton",
                            foreground="black",  # default/dark text for light mode
                            font=("Arial", 12),
                            padding=(5,10,5,10))
    def toggle_mus():
        global mus, clicky
        clicky += 1
        if mus:
            mus = False
            music.stop_music()
        else:
            mus = True
            music.play_music()
        if clicky == 2:
            clicky = 0

    settings_window = tk.Toplevel(root)
    settings_window.geometry("500x400")
    darktheme_button = ttk.Button(settings_window, text = "Enable Dark Theme (click again to disable)", command = darktheme)
    darktheme_button.place(relx=0.5, y=50, anchor='center')
    music_button = ttk.Button(settings_window, text="Toggle Music", command=toggle_mus)
    music_button.place(relx=0.5, y=100, anchor='center')

from PIL import Image, ImageTk
root = tk.Tk()
root.title("The Game made to Destroy Boredom: The Game")
root.attributes('-fullscreen', True)

style = ttk.Style()
style.configure("TButton", foreground="black", font=("Arial", 12), padding=(5, 10, 5, 10))

# Add a way to exit/enter fullscreen
def exit_fullscreen(event=None):
    root.attributes('-fullscreen', False)

def enter_fullscreen(event=None):
    root.attributes('-fullscreen', True)

root.bind('<Escape>', exit_fullscreen)
root.bind('<F11>', enter_fullscreen)
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
header = ttk.Label(root, text="The Game Made to Destroy Boredom: The Game", font=("Cascadia Code", 19, "bold"))
header.pack(pady=(20, 10))

# Function to increase g
def click():
    global g
    global clickg
    g += clickg
    add_log(f"Increased G by {clickg}")
    gain_exp(clickg)
    g_label.config(text=f"{g:,.2f}G")  # Two decimals, commas for thousands

# Taxes mechanic labels
tax_frame = ttk.Frame(root)

message_label = tk.Label(tax_frame, text = "TIME LEFT BEFORE TAXES", font = ("Arial",14), fg = "#FF0000")
message_label.pack(anchor = "center", pady = (3, 0))

tax_time_label = tk.Label(tax_frame, text = f"", font = ("Arial",16), fg = "#FF0000")
tax_time_label.pack(anchor = "center", pady = (4, 0))

tax_frame.pack(side="top", anchor="n", pady=(10, 0))
#tax functions
def tax_collect():
    global g
    messagebox.showerror('Taxes', 'Haha money go bye bye')
    g -= g * 0.25  # Decrease g by 25%
    g = int(g)      # Optional: convert to integer if needed
    g_label.config(text = f"{format(g)}G")
# Log
log_console = tk.Text(root, height=10, width=100, state='disabled',
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

    root.after(100, lambda: log_window.deiconify)

# --- LOG BUTTON ---
log_button = ttk.Button(root, text="View Log", command=open_log_window)
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

g_frame = ttk.Frame(root)
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
            music.stop_music()
            sound4.play()
            music.play_music()
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
# --- Transparent frames (no solid color, inherit background) ---
main_frame = tk.Frame(root, bg="", highlightthickness=0, bd=0)
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

quit_button = ttk.Button(main_frame, text="Quit Game", command=root.destroy)
quit_button.grid(row=3, column=2, padx=10, pady=10)

# Exp labels and stuff

level_frame = ttk.Frame(root)
level_frame.pack(pady=(0, 10))

level_label = tk.Label(level_frame, text=f"Level: {level}", font=("Cascadia Code", 20))
level_label.pack()

level_amnt_label = tk.Label(level_frame, text = f"{current_exp}/{next_level_exp}", font = ("Cascadia Code", 16))
level_amnt_label.pack()

level_vis = ttk.Progressbar(level_frame, orient="horizontal", mode="determinate", length=300)
level_vis.pack()

level_vis['maximum'] = next_level_exp
level_vis['value'] = current_exp

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
pro_tip = ttk.Label(root, text="Pro Tip:", font=("Cascadia Code", 10))
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
        "If the Generator Status is still BROKEN, keep on fixing!"
    ]
    tip = random.choice(tips)
    pro_tip.config(text=f"Pro tip: {tip}")
    root.after(5000, pro_tip_text)
def save_game():
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
        "igen_count": len(igen_list),
        "gen_lvl3": gen_lvl3,
        "g_given3": g_given3,
        "upgrade_cost3": upgrade_cost3,
        "igen_price": igen_price,
        "igen_shop_amnt": igen_shop_amnt,
        "igen_amnt": igen_amnt,
        "randgen_amnt": randgen_amnt,
        "randgen_list": randgen_list,
        "randgen_price": randgen_price,
        "randgen_shop_amnt": randgen_shop_amnt,
        "randgen_stock": randgen_stock,
        "g_given4": g_given4,
        "gen_lvl4": gen_lvl4
    }
    with open("savegame.json", "w") as f:
        json.dump(save_data, f)
    save_label.config(text="Game saved!")
    root.after(1000, lambda: save_label.config(text = ""))

def load_game():
    global g, clickg, gen_price, gen_shop_amnt, gen_amnt, g_given1, gen_lvl, upgrade_cost
    global bgen_price, bgen_shop_amnt, bgen_amnt, g_given2, gen_lvl2, upgrade_cost2
    global gen_stock, bgen_stock, igen_stock
    global gen_list, bgen_list, igen_list
    global gen_lvl3, g_given3, upgrade_cost3, igen_price, igen_shop_amnt, igen_amnt
    global level, next_level_exp, current_exp

    gen_list = []
    bgen_list = []
    igen_list = []

    if os.path.exists("savegame.json"):
        with open("savegame.json", "r") as f:
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
        current_exp = save_data.get("current_exp", 0)
        next_level_exp = save_data.get("next_level_exp", 100)
        level = save_data.get("level", 1)
        level_label.config(text=f"Level: {level}")
        level_vis['maximum'] = next_level_exp
        level_vis['value'] = current_exp
        # Re-create generators
        for _ in range(save_data.get("gen_count", 0)):
            gen_list.append(Generator(gen_lvl))
        for _ in range(save_data.get("bgen_count", 0)):
            bgen_list.append(BetterGenerator(gen_lvl2))
        for _ in range(save_data.get("igen_count", 0)):
            igen_list.append(IndusGenerator(gen_lvl3))

        # --- UPDATE ALL LABELS ---
        g_label.config(text=f"{g:,.2f}G")  # Two decimals, commas for thousands
        gps_label.config(text=f"{(len(gen_list)*g_given1) + (len(bgen_list)*g_given2) + (len(igen_list)*g_given3)}G/s")

        # If your shop or upgrade menu is open, update their labels too
        try:
            gen_shop_price_label.config(text=f"Price: {gen_price}G")
            bgen_shop_price_label.config(text=f"Price: {bgen_price}G")
            igen_shop_price_label.config(text=f"Price: {igen_price}G")

            gen_shop_amnt_label.config(text=f"Current amount: {len(gen_list)}")
            bgen_shop_amnt_label.config(text=f"Current amount: {len(bgen_list)}")
            igen_shop_amnt_label.config(text=f"Current amount: {len(igen_list)}")

            gen_stock_label.config(text=f"Stock: {gen_stock}")
            bgen_stock_label.config(text=f"Stock: {bgen_stock}")
            igen_stock_label.config(text=f"Stock: {igen_stock}")
        except NameError:
            pass  # Shop might not be open yet

        try:
            stdgen_label.config(text=f"Level: {gen_lvl}")
            bgen_label.config(text=f"Level: {gen_lvl2}")
            igen_label.config(text=f"Level: {gen_lvl3}")

            stdgen_button.config(text=f"UPGRADE ({upgrade_cost}G)")
            bgen_button.config(text=f"UPGRADE ({upgrade_cost2}G)")
            igen_button.config(text=f"UPGRADE ({upgrade_cost3}G)")
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
save_frame = ttk.Frame(root)

save_button = ttk.Button(save_frame, text="Save", command=save_game)
save_button.grid(row=0, column=0, padx=5)

load_button = ttk.Button(save_frame, text="Load", command=load_game)
load_button.grid(row=0, column=1, padx=5)

save_label = tk.Label(save_frame, text="", font=("Cascadia Code", 11))
save_label.grid(row=0, column=2, padx=5)

# Place in bottom-right corner with padding
save_frame.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
music.play_music()  # Start music and loop forever

def toggle_mus():
    global mus, clicky
    clicky += 1
    if mus:
        mus = False
        music.stop_music()
    else:
        mus = True
        music.play_music()
    if clicky == 2:
        clicky = 0
def music_poll():
    if mus == True:
        music.check_and_advance()
    else:
        pass
    root.after(1000, music_poll)  # Check every second
music.play_music()
electricity()
pro_tip_text()
#for autosave
def autosave_loop():
    root.after(60000, autosave_loop)
    save_game()
autosave_loop()
music_poll()  # Start polling
load_game() # Load da game at start
elec_checker()
root.mainloop()
music.close()