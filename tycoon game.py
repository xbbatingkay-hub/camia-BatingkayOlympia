import tkinter as tk
import random
import playsound
g = 0
clickg = 1
gen_price = 10
gen_shop_amnt = 1
gen_list = []
gen_amnt = 0

class Generator():
    def __init__(self):
        self.running = True
        self.start_generating()

    def start_generating(self):
        if self.running:
            global g
            g += 1
            g_label.config(text=f"{g}G", font=("Cascadia Code", 25))
            root.after(1000, self.start_generating)

def click():
    global g
    global clickg
    g += clickg
    g_label.config(text=f"{g}G", font = ("Cascadia Code", 25))
    
def shop():
    global gen_price
    global gen_shop_amnt
    global gen_amnt

    def increase():
        nonlocal shop_amnt
        global gen_shop_amnt
        gen_shop_amnt += 1
        shop_amnt.config(text = f"amount: {gen_shop_amnt}")

    def buy():
        nonlocal shop_g, shop_amnt, gen_shop_amnt_label
        global g
        global gen_price
        global gen_shop_amnt 
        global gen_amnt

        if g >= gen_price * gen_shop_amnt:
            g -= gen_price * gen_shop_amnt
            g_label.config(text=f"{g}G", font = ("Cascadia Code", 25))
            shop_g.config(text = f"{g}G", font = ("Cascadia Code",25))
            for i in range(gen_shop_amnt):
                newgen = Generator()
                gen_list.append(newgen)
            gen_amnt += gen_shop_amnt
            gen_shop_amnt = 1
            shop_amnt.config(text = f"amount: {gen_shop_amnt}")
            gen_shop_amnt_label.config(text = f"Current amount: {len(gen_list)}", font = ("Arial", 14))

    shop_window = tk.Toplevel(root)
    shop_window.title("Shop Menu")
    shop_window.geometry("500x300")
    shop_g = tk.Label(shop_window, text = f"{g}G", font = ("Cascadia Code",25))
    shop_g.place(x = 30, y = 10)
    gen_item = tk.Label(shop_window, text = f"Standard G generator (1g/s)", font = ("Arial",14))
    gen_item.place(x = 50, y = 100)
    shop_amnt = tk.Label(shop_window, text = f"amount: {gen_shop_amnt}", font = ("Arial", 14)) 
    shop_amnt.place(x = 300, y = 100)
    gen_shop_amnt_label = tk.Label(shop_window, text = f"Current amount: {len(gen_list)}", font = ("Arial", 14))
    gen_shop_amnt_label.place(x = 50, y = 125)
    buy_amnt = tk.Button(shop_window, text = f"+1", command = increase, font = ("Arial", 14))
    buy_amnt.place(x = 400, y = 100)
    buy_button = tk.Button(shop_window, text = "BUY", command = buy, font = ("Cascadia Code", 14))
    buy_button.place(x = 50, y = 150)

def gamble():
    global g
    gambleg = 100
    roll = 5

    def gambling():
        # Play sound in a non-blocking way
        try:
            playsound.playsound('slot-machine.wav', block=False)
        except TypeError:
            import threading
            threading.Thread(target=playsound.playsound, args=('slot-machine.wav',), daemon=True).start()

        nonlocal gambleg, roll
        # Deduct entry fee only on first roll
        if select_button['state'] == "normal":
            if g < 100:
                msg_label.config(text="Not enough G!")
                return
            g -= 100
            g_label.config(text=f"{g}G", font=("Cascadia Code", 25))
            gambleg = 100
            roll = 5

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

root = tk.Tk()
root.title("tycoon game")
root.geometry("400x350")

g_label = tk.Label(root, text=f"{g}G", font = ("Cascadia Code", 25))
g_label.place(x=180, y=50)

button = tk.Button(root, text=f"increase G ({clickg})", command=click, font=("Arial", 12))
button.place(x = 150, y = 150)
shop_button = tk.Button(root, text=f"click to shop", command=shop, font=("Arial", 12))
shop_button.place(x = 155, y = 200)
gamble_button = tk.Button(root, text = "gamble", command = gamble, font = ("Arial",12))
gamble_button.place(x = 160, y = 250)
root.mainloop()

