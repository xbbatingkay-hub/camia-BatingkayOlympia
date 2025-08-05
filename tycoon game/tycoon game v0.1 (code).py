import tkinter as tk
import random
import playsound

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
# Add stock variables at the top
gen_stock = 10        # Stock for standard generators
bgen_stock = 5        # Stock for massive generators

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
        g_given1 *= 1.5
        
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
        g_given2 *= 1.2
def click():
    global g
    global clickg
    g += clickg
    g_label.config(text=f"{g}G", font = ("Cascadia Code", 25))
    
def shop():
    global gen_price, gen_shop_amnt, gen_amnt
    global gen_stock, bgen_stock

    # Random chance for BetterGenerators to be in stock
    import random
    if random.random() < 0.3:  # 30% chance to appear
        bgen_stock = random.randint(1, 2)  # 1 or 2 in stock
    else:
        bgen_stock = 0  # Not available this time

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
    def restock():
        nonlocal gen_stock_label, bgen_stock_label
        global gen_stock, bgen_stock
        global g
        g -= 100
        gen_stock = 10
        # Randomize BetterGenerator stock on restock
        if random.random() < 0.3:
            bgen_stock = random.randint(1, 5)
        else:
            bgen_stock = 0
        gen_stock_label.config(text=f"Stock: {gen_stock}")
        bgen_stock_label.config(text=f"Stock: {bgen_stock}")

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
    #restock button
    restock_button = tk.Button(shop_window, text="Restock (100G)", command=restock, font=("Arial", 14))
    restock_button.place(x=200, y=500)

def gamble():
    global g
    gambleg = 100
    roll = 5
    entry_paid = False  # <-- Add this flag

    def gambling():
        global g
        g=g
        nonlocal gambleg, roll, entry_paid
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
            g -= 100
            g_label.config(text=f"{g}G", font=("Cascadia Code", 25))
            entry_paid = True  # <-- Set flag so fee is only paid once
        gambleg -= roll
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
            nonlocal gambleg, roll
            if selected_item1 == selected_item2 and selected_item1 == selected_item3:
                if selected_item1 == "0":
                    msg_label.config(text="unlucky!")
                    x = random.choice(unluck)
                    root.after(1000, lambda: msg_label.config(text=f"{x}"))
                    if x == "poor :>":
                        gambleg = 0
                    elif x == "taxes >:>":
                        gambleg //= 2
                    elif x == "compensation!":
                        gambleg += 50
                elif selected_item1 == "#":
                    msg_label.config(text="free reroll!")
                    roll = 0
                    root.after(1000, lambda: select_button.config(text=f"roll [${roll}]"))
                    root.after(1000, lambda: msg_label.config(text=""))
                elif selected_item1 == "7":
                    msg_label.config(text="!7!7! JACKPOT !7!7!")
                    msg_label.place(x=80, y=60)
                    root.after(1000, lambda: msg_label.config(text=""))
                    gambleg += 777
            money_label.config(text=f"${gambleg}")
            root.after(1000, lambda: result_label.config(text=f"[ ]"))
            root.after(1200, lambda: result_label2.config(text=f"[ ]"))
            root.after(1400, lambda: result_label3.config(text=f"[ ]"))
            root.after(1500, lambda: select_button.config(state="normal"))
        root.after(600, after_slots)
        money_label.config(text=f"${gambleg}")

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

    # Add winnings to main currency when window closes
    def on_close():
        global g
        g += gambleg
        g_label.config(text=f"{g}G", font=("Cascadia Code", 25))
        root2.destroy()
    root2.protocol("WM_DELETE_WINDOW", on_close)
def upgrade():
    global gen_lvl, gen_lvl2
    global newgen
    def upgrader():
        global gen_lvl
        newgen.lvlup()
        gen_lvl += 1
        root.after(200, lambda: stdgen_label.config(text = f"Standard Generator LVL:{gen_lvl}"))
    def upgrader2():
        global gen_lvl2
        newgen2.lvlup()
        gen_lvl2 += 1
        root.after(200, lambda: stdgen_label.config(text = f"Massive Generator LVL:{gen_lvl}"))
    upgrade_win = tk.Toplevel(root)
    upgrade_win.title("Upgrade Window")
    upgrade_win.geometry("400x300")

    stdgen_label = tk.Label(upgrade_win, text = f"Standard Generator LVL:{gen_lvl}", font = ("Cascadia Code", 16))
    stdgen_label.place(x = 50, y = 100)
    stdgen_button = tk.Button(upgrade_win, text = f"UPGRADE ({upgrade_cost}G)", command = upgrader, font = ("Arial", 12))
    stdgen_button.place(x = 50, y = 130)
    bgen_label = tk.Label(upgrade_win, text = f"Massive Generator LVL:{gen_lvl}", font = ("Cascadia Code", 16))
    bgen_label.place(x = 50, y = 170)
    bgen_button = tk.Button(upgrade_win, text = f"UPGRADE ({upgrade_cost}G)", command = upgrader2, font = ("Arial", 12))
    bgen_button.place(x = 50, y = 200)
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


increase_clickg()
root.mainloop()

