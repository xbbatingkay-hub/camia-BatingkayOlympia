import tkinter as tk
import random
import playsound
import json
import os
#guide for adding a new item:
#add its variables first: (price, shop amount, how much g it gives, its list, its starting lvl, and cost)
#add it as a buy option in shop()
#add it as an upgrade option in upgrade()

#starting g
g = 0
#g per click
clickg = 1
#standard generators
gen_price = 10
gen_shop_amnt = 1
gen_list = []
gen_amnt = 0
g_given1 = 1
gen_lvl = 1
upgrade_cost = 100
#massive generators
bgen_price = 100
bgen_shop_amnt = 1
bgen_amnt = 0
bgen_list = []
g_given2 = 10
gen_lvl2 = 1
upgrade_cost2 = 200
#industrial generators
igen_price = 250
igen_shop_amnt = 1
igen_amnt = 0
igen_list = []
g_given3 = 100
gen_lvl3 = 1
upgrade_cost3 = 200
# Add stock variables at the top
gen_stock = 15        # Stock for standard generators
bgen_stock = 10        # Stock for massive generators
igen_stock = 10       # Stock for industrial generators
class Generator():
    def __init__(self, gen_level):
        self.gen_level = gen_level
        self.running = True
        self.start_generating()

    def start_generating(self):
        if self.running:
            global g
            g += g_given1
            g_label.config(text=f"{g}G", font=("Cascadia Code", 25))
            root.after(1000, self.start_generating)
    
    def lvlup(self):
        global upgrade_cost
        upgrade_cost *= 1.5
        self.gen_level += 1
        global g_given1
        g_given1 *= 2
        
class BetterGenerator():
    def __init__(self, gen_level):
        self.gen_level = gen_level
        self.running = True
        self.startmaking()
    def startmaking(self):
        if self.running:
            global g
            g += g_given2
            g_label.config(text=f"{g}G", font=("Cascadia Code", 25))
            root.after(1000, self.startmaking)
    def lvlup(self):
        global upgrade_cost2
        upgrade_cost2 *= 1.5
        self.gen_level += 1
        global g_given2
        g_given2 *= 1.5
class IndusGenerator():
    def __init__(self, gen_level):
        self.gen_level = gen_level
        self.running = True
        self.startmaking()
    def startmaking(self):
        if self.running:
            global g
            g += g_given3
            g_label.config(text=f"{g}G", font=("Cascadia Code", 25))
            root.after(1000, self.startmaking)
    def lvlup(self):
        global upgrade_cost3
        upgrade_cost3 *= 1.5
        self.gen_level += 1
        global g_given3
        g_given3 *= 1.5
def click():
    global g
    global clickg
    g += clickg
    g_label.config(text=f"{g}G", font = ("Cascadia Code", 25))
    
def shop():
    global gen_price, gen_shop_amnt, gen_amnt
    global gen_stock, bgen_stock

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
            g_label.config(text=f"{g}G", font = ("Cascadia Code", 25))
            shop_g.config(text = f"{g}G", font = ("Cascadia Code",25))
            for i in range(gen_shop_amnt):
                global newgen 
                newgen = Generator(gen_lvl)
                gen_list.append(newgen)
            gen_amnt += gen_shop_amnt
            gen_stock -= gen_shop_amnt  # Reduce stock
            gen_shop_amnt = 1
            shop_amnt.config(text = f"amount: {gen_shop_amnt}")
            gen_shop_amnt_label.config(text = f"Current amount: {len(gen_list)}", font = ("Arial", 14))
            gen_stock_label.config(text=f"Stock: {gen_stock}")
        increase_clickg()
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
            g_label.config(text=f"{g}G", font = ("Cascadia Code", 25))
            shop_g.config(text = f"{g}G", font = ("Cascadia Code",25))
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
            increase_clickg()
    
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
            g_label.config(text=f"{g}G", font = ("Cascadia Code", 25))
            shop_g.config(text = f"{g}G", font = ("Cascadia Code",25))
            for i in range(igen_shop_amnt):
                global newgen3
                newgen3 = IndusGenerator(gen_lvl3)
                gen_list.append(newgen3)
                bgen_list.append(newgen3)
                igen_list.append(newgen3)
            igen_amnt += igen_shop_amnt
            igen_stock -= igen_shop_amnt  # Reduce stock
            igen_shop_amnt = 1
            ishop_amnt.config(text = f"amount: {igen_shop_amnt}")
            igen_shop_amnt_label.config(text = f"Current amount: {len(igen_list)}", font = ("Arial", 14))
            igen_stock_label.config(text=f"Stock: {igen_stock}")
            increase_clickg()
    def restock():
        nonlocal gen_stock_label, bgen_stock_label
        global gen_stock, bgen_stock, igen_stock
        global g
        if g < 100:
            return
        g -= 100
        gen_stock = 15
        # Randomize BetterGenerator stock on restock
        if random.random() < 0.5:
            bgen_stock = random.randint(1, 10)
        else:
            bgen_stock = 0
        if random.random() < 0.3:
            igen_stock = random.randint(1, 5)
        else:
            igen_stock = 0
        gen_stock_label.config(text=f"Stock: {gen_stock}")
        bgen_stock_label.config(text=f"Stock: {bgen_stock}")
        igen_stock_label.config(text = f"Stock: {igen_stock}")

    shop_window = tk.Toplevel(root)
    shop_window.title("Shop Menu")
    shop_window.geometry("500x550")
    shop_g = tk.Label(shop_window, text = f"{g}G", font = ("Cascadia Code",25))
    shop_g.place(x = 30, y = 10)
    def update_shop_g():
        shop_g.config(text=f"{g}G")
        shop_window.after(200, update_shop_g)
    update_shop_g()
    gen_item = tk.Label(shop_window, text = f"Standard G generator (1g/s)", font = ("Arial",14))
    gen_item.place(x = 50, y = 100)
    shop_amnt = tk.Label(shop_window, text = f"amount: {gen_shop_amnt}", font = ("Arial", 14)) 
    shop_amnt.place(x = 300, y = 100)
    gen_shop_amnt_label = tk.Label(shop_window, text = f"Current amount: {len(gen_list)}", font = ("Arial", 14))
    gen_shop_amnt_label.place(x = 50, y = 125)
    gen_shop_price_label = tk.Label(shop_window, text = f"Price: {gen_price}G", font = ("Arial",16))
    gen_shop_price_label.place(x = 250, y = 125)
    gen_stock_label = tk.Label(shop_window, text=f"Stock: {gen_stock}", font=("Arial", 14))
    gen_stock_label.place(x=400, y=150)
    buy_amnt = tk.Button(shop_window, text = f"+1", command = increase, font = ("Arial", 14))
    buy_amnt.place(x = 400, y = 100)
    buy_amnt = tk.Button(shop_window, text = f"-1", command = decrease, font = ("Arial", 14))
    buy_amnt.place(x = 430, y = 100)
    buy_button = tk.Button(shop_window, text = "BUY", command = buy, font = ("Cascadia Code", 14))
    buy_button.place(x = 50, y = 150)
    #bigger G generator
    bgen_item = tk.Label(shop_window, text = f"Massive G generator (10g/s)", font = ("Arial",14))
    bgen_item.place(x = 50, y = 200)
    bshop_amnt = tk.Label(shop_window, text = f"amount: {bgen_shop_amnt}", font = ("Arial", 14)) 
    bshop_amnt.place(x = 300, y = 200)
    bgen_shop_amnt_label = tk.Label(shop_window, text = f"Current amount: {len(bgen_list)}", font = ("Arial", 14))
    bgen_shop_amnt_label.place(x = 50, y = 225)
    bgen_shop_price_label = tk.Label(shop_window, text = f"Price: {bgen_price}G", font = ("Arial",16))
    bgen_shop_price_label.place(x = 250, y = 225)
    bgen_stock_label = tk.Label(shop_window, text=f"Stock: {bgen_stock}", font=("Arial", 14))
    bgen_stock_label.place(x=400, y=250)
    bbuy_amnt = tk.Button(shop_window, text = f"+1", command = bincrease, font = ("Arial", 14))
    bbuy_amnt.place(x = 400, y = 200)
    bbuy_amnt_decr = tk.Button(shop_window, text = f"-1", command = bdecrease, font = ("Arial", 14))
    bbuy_amnt_decr.place(x = 430, y = 200)
    bbuy_button = tk.Button(shop_window, text = "BUY", command = bbuy, font = ("Cascadia Code", 14))
    bbuy_button.place(x = 50, y = 250)
    #industrial G generator
    igen_item = tk.Label(shop_window, text = f"Industrial G generator (10g/s)", font = ("Arial",14))
    igen_item.place(x = 50, y = 300)
    ishop_amnt = tk.Label(shop_window, text = f"amount: {igen_shop_amnt}", font = ("Arial", 14)) 
    ishop_amnt.place(x = 300, y = 300)
    igen_shop_amnt_label = tk.Label(shop_window, text = f"Current amount: {len(igen_list)}", font = ("Arial", 14))
    igen_shop_amnt_label.place(x = 50, y = 325)
    igen_shop_price_label = tk.Label(shop_window, text = f"Price: {igen_price}G", font = ("Arial",16))
    igen_shop_price_label.place(x = 250, y = 325)
    igen_stock_label = tk.Label(shop_window, text=f"Stock: {igen_stock}", font=("Arial", 14))
    igen_stock_label.place(x=400, y=350)
    ibuy_amnt = tk.Button(shop_window, text = f"+1", command = iincrease, font = ("Arial", 14))
    ibuy_amnt.place(x = 400, y = 300)
    ibuy_amnt_decr = tk.Button(shop_window, text = f"-1", command = idecrease, font = ("Arial", 14))
    ibuy_amnt_decr.place(x = 430, y = 300)
    ibuy_button = tk.Button(shop_window, text = "BUY", command = ibuy, font = ("Cascadia Code", 14))
    ibuy_button.place(x = 50, y = 350)
    #restock button
    restock_button = tk.Button(shop_window, text="Restock (100G)", command=restock, font=("Arial", 14))
    restock_button.place(x=200, y=500)

def gamble():
    global g
    g = g
    roll = 5
    entry_paid = False  # <-- Add this flag

    def gambling():
        global g
        g=g
        nonlocal roll, entry_paid
        # Play sound in a non-blocking way
        try:
            playsound.playsound('slot-machine.wav', block=False)
        except TypeError:
            import threading
            threading.Thread(target=playsound.playsound, args=('slot-machine.wav',), daemon=True).start()
        # Deduct entry fee only on first roll
        if not entry_paid:
            if g < 100:
                msg_label.config(text="100G needed")
                return
            g_label.config(text=f"{g}G", font=("Cascadia Code", 25))
            entry_paid = True  # <-- Set flag so fee is only paid once
        g -= roll
        select_button.config(text=f"roll [${roll}]")
        select_button.config(state="disabled")
        msg_label.place(x=154, y=60)
        slot1 = ["0", "#", "?", "7"]
        slot2 = ["0", "#", "?", "7"]
        slot3 = ["0", "#", "?", "7"]
        unluck = ["poor :>", "taxes >:>", "compensation!", "no prize :P"]
        selected_item1 = random.choice(slot1)
        selected_item2 = random.choice(slot2)
        selected_item3 = random.choice(slot3)
        result_label.config(text=f"[{selected_item1}]")
        root.after(200, lambda: result_label2.config(text=f"[{selected_item2}]"))
        root.after(400, lambda: result_label3.config(text=f"[{selected_item3}]"))
        def after_slots():
            nonlocal roll
            if selected_item1 == selected_item2 and selected_item1 == selected_item3:
                if selected_item1 == "0":
                    msg_label.config(text="unlucky!")
                    x = random.choice(unluck)
                    root.after(1000, lambda: msg_label.config(text=f"{x}"))
                    if x == "poor :>":
                        g = 0
                    elif x == "taxes >:>":
                        g //= 2
                    elif x == "compensation!":
                        g += 50
                elif selected_item1 == "#":
                    msg_label.config(text="free reroll!")
                    roll = 0
                    root.after(1000, lambda: select_button.config(text=f"roll [${roll}]"))
                    root.after(1000, lambda: msg_label.config(text=""))
                elif selected_item1 == "7":
                    msg_label.config(text="!7!7! JACKPOT !7!7!")
                    msg_label.place(x=80, y=60)
                    root.after(1000, lambda: msg_label.config(text=""))
                    g += 777
            money_label.config(text=f"${g}")
            root.after(1000, lambda: result_label.config(text=f"[ ]"))
            root.after(1200, lambda: result_label2.config(text=f"[ ]"))
            root.after(1400, lambda: result_label3.config(text=f"[ ]"))
            root.after(1500, lambda: select_button.config(state="normal"))
        root.after(600, after_slots)
        money_label.config(text=f"${g}")

    # Create the main window
    root2 = tk.Toplevel(root)
    root2.title("GAMBLETIME")
    root2.geometry("320x200")

    # Create a label to display the result
    result_label = tk.Label(root2, text="[  ]", font=("Arial", 14))
    result_label2 = tk.Label(root2, text="[  ]", font=("Arial", 14))
    result_label3 = tk.Label(root2, text="[  ]", font=("Arial", 14))
    msg_label = tk.Label(root2, text="", font=("Arial", 14))
    money_label = tk.Label(root2, text=f"${gambleg}", font=("Arial", 14))
    result_label.place(x=100, y=30)
    result_label2.place(x=150, y=30)
    result_label3.place(x=200, y=30)
    msg_label.place(x=154, y=60)
    money_label.place(relx=0.7, rely=0.7, anchor='nw')

    # Create a button to trigger the random selection
    select_button = tk.Button(root2, text=f"roll [${roll}]", command=gambling, font=("Arial", 12))
    select_button.pack(pady=10)
    select_button.place(relx=0.5, rely=0.5, anchor='center')

    quit_button = tk.Button(root2, text=f"quit", command=root2.destroy, font=("Arial", 12))
    quit_button.pack(relx = 0.5, rely=0.8, anchor="center")
    

    # Add winnings to main currency when window closes
    def on_close():
        global g
        if gambleg == 100:
            g_label.config(text=f"{g}G", font=("Cascadia Code", 25))
            root2.destroy()
        else:
            g += gambleg
            g_label.config(text=f"{g}G", font=("Cascadia Code", 25))
            root2.destroy()
    root2.protocol("WM_DELETE_WINDOW", on_close)
def upgrade():
    global gen_lvl, gen_lvl2, gen_lvl3
    def upgrader():
        global gen_lvl, upgrade_cost, g_given1
        if len(gen_list) == 0:
            return
        for gen in gen_list:
            gen.lvlup()
        gen_lvl += 1
        root.after(200, lambda: stdgen_label.config(text = f"Standard Generator LVL:{gen_lvl}"))
        root.after(400, lambda: stdgen_button.config(text = f"UPGRADE ({upgrade_cost}G)"))
    def upgrader2():
        global gen_lvl2, upgrade_cost2, g_given2
        if len(bgen_list) == 0:
            return
        for bgen in bgen_list:
            bgen.lvlup()
        gen_lvl2 += 1
        root.after(200, lambda: bgen_label.config(text = f"Massive Generator LVL:{gen_lvl2}"))
        root.after(400, lambda: bgen_button.config(text = f"UPGRADE ({upgrade_cost2}G)"))
    def upgrader3():
        global gen_lvl3, upgrade_cost3, g_given3
        if len(igen_list) == 0:
            return
        for igen in igen_list:
            igen.lvlup()
        gen_lvl3 += 1
        root.after(200, lambda: bgen_label.config(text = f"Industrial Generator LVL:{gen_lvl3}"))
        root.after(400, lambda: bgen_button.config(text = f"UPGRADE ({upgrade_cost3}G)"))
    upgrade_win = tk.Toplevel(root)
    upgrade_win.title("Upgrade Window")
    upgrade_win.geometry("400x400")

    g_upgrade_label = tk.Label(upgrade_win, text = f"{g}g", font = ("Cascadia Code", 16))
    g_upgrade_label.pack(padx = 50, pady = 0.2, anchor="nw")
    stdgen_label = tk.Label(upgrade_win, text = f"Standard Generator LVL:{gen_lvl}", font = ("Cascadia Code", 16))
    stdgen_label.place(x = 50, y = 50)
    stdgen_button = tk.Button(upgrade_win, text = f"UPGRADE ({upgrade_cost}G)", command = upgrader, font = ("Arial", 12))
    stdgen_button.place(x = 50, y = 80)
    bgen_label = tk.Label(upgrade_win, text = f"Massive Generator LVL:{gen_lvl2}", font = ("Cascadia Code", 16))
    bgen_label.place(x = 50, y = 120)
    bgen_button = tk.Button(upgrade_win, text = f"UPGRADE ({upgrade_cost2}G)", command = upgrader2, font = ("Arial", 12))
    bgen_button.place(x = 50, y = 150)
    bgen_label = tk.Label(upgrade_win, text = f"Industrial Generator LVL:{gen_lvl3}", font = ("Cascadia Code", 16))
    bgen_label.place(x = 50, y = 190)
    bgen_button = tk.Button(upgrade_win, text = f"UPGRADE ({upgrade_cost3}G)", command = upgrader3, font = ("Arial", 12))
    bgen_button.place(x = 50, y = 220)

    close_button = tk.Button(upgrade_win, text = "close window", command = upgrade_win.destroy, font = ("Arial", 16))
    close_button.place(x = 50, y = 290)
def increase_clickg():
    global clickg
    clickg = 1 + len(gen_list) + len(bgen_list)
    button.config(text=f"increase G ({clickg})")

root = tk.Tk()
root.title("tycoon game")
root.geometry("400x350")

g_label = tk.Label(root, text=f"{g}G", font = ("Cascadia Code", 25))
g_label.place(relx=0.5, y=50, anchor='center')

button = tk.Button(root, text=f"increase G ({clickg})", command=click, font=("Arial", 12))
button.place(relx=0.5, y=120, anchor='center')

shop_button = tk.Button(root, text="click to shop", command=shop, font=("Arial", 12))
shop_button.place(relx=0.5, y=170, anchor='center')

gamble_button = tk.Button(root, text="gamble", command=gamble, font = ("Arial",12))
gamble_button.place(relx=0.5, y=220, anchor='center')

upgrade_button = tk.Button(root, text="upgrade", command=upgrade, font = ("Arial",12))
upgrade_button.place(relx=0.5, y=270, anchor='center')

upgrade_button = tk.Button(root, text="quit game", command=root.destroy, font = ("Arial",12))
upgrade_button.place(relx=0.5, y=320, anchor='center')


def save_game():
    save_data = {
        "g": g,
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
        "igen_amnt": igen_amnt
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
    gen_list = []
    bgen_list = []
    igen_list = []
    if os.path.exists("savegame.json"):
        with open("savegame.json", "r") as f:
            save_data = json.load(f)
        g = save_data.get("g", 0)
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

        # Re-create generators
        gen_list = []
        for _ in range(save_data.get("gen_count", 0)):
            gen_list.append(Generator(gen_lvl))
        bgen_list = []
        for _ in range(save_data.get("bgen_count", 0)):
            bgen_list.append(BetterGenerator(gen_lvl2))
        igen_list = []
        for _ in range(save_data.get("igen_count", 0)):
            igen_list.append(IndusGenerator(gen_lvl3))

        save_label.config(text="Game loaded!")
        root.after(1000, lambda: save_label.config(text = ""))

save_button = tk.Button(root, text="Save", command=save_game, font=("Arial", 12))
save_button.pack(padx=10, pady=10, anchor="nw")
load_button = tk.Button(root, text="Load", command=load_game, font=("Arial", 12))
load_button.pack(padx=10, pady=10, anchor="nw")
save_label = tk.Label(root, text="", font = ("Cascadia Code", 11))
save_label.pack(padx = 10, pady = 10, anchor = "nw")
#for autosave
root.after(60000, save_game)
increase_clickg()
root.mainloop()