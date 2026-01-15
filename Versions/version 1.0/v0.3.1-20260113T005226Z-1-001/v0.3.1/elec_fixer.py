import tkinter as tk
import random
from tkinter import ttk
import os
import pygame

# --- Initialize Sounds ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pygame.mixer.init()

def load_sound(filename):
    path = os.path.join(BASE_DIR, "sounds", filename)
    return pygame.mixer.Sound(path) if os.path.exists(path) else None

sound5 = load_sound("energy1.mp3")    # success
sound6 = load_sound("energy2.mp3")    # fail
sound7 = load_sound("buttonpress1.mp3")  # button press


def start_elec_fix(root, on_repair_complete):
    """
    Opens the electricity repair puzzle in a Toplevel window.
    Calls on_repair_complete() when puzzle is solved.
    """
    elec_fix_win = tk.Toplevel(root)
    elec_fix_win.title("Electricity Repair Utility")
    elec_fix_win.geometry("400x400")

    # Title
    title_label = ttk.Label(elec_fix_win, text="ELECTRICITY REPAIR UTILITY",
                            font=("Cascadia Code", 16))
    title_label.pack(anchor="center", pady=(5, 0))

    # Progress bar
    elec_pb = ttk.Progressbar(elec_fix_win, orient="horizontal",
                              mode='determinate', length=200)
    elec_pb.pack(anchor="center", pady=(5, 0))
    elec_pb['value'] = 0
    elec_pb['maximum'] = 200

    # Display label for sequence
    seq_label = ttk.Label(elec_fix_win, text="", font=("Cascadia Code", 16))
    seq_label.pack(anchor="center", pady=(5, 0))

    # Button frame
    btn_frame = ttk.Frame(elec_fix_win)
    btn_frame.pack(anchor="center", pady=(10, 0))

    # Game state
    rounds_completed = [0]
    elec_switches_rand = []
    elec_switch_choice = []
    elec_switches_need = 3
    buttons = []

    # --- Game Logic ---
    def new_sequence():
        nonlocal elec_switches_rand, elec_switch_choice
        numbers = [str(i) for i in range(1, 10)]
        random.shuffle(numbers)
        elec_switches_rand = numbers[:elec_switches_need]
        elec_switch_choice.clear()
        enable_all_buttons()
        show_order()

    def show_order(index=0):
        if index < len(elec_switches_rand):
            seq_label.config(text=elec_switches_rand[index])
            elec_fix_win.after(500, lambda: show_order(index + 1))
        else:
            seq_label.config(text="Repeat the order!")

    def switch(value, btn):
        elec_switch_choice.append(value)
        if sound7: sound7.play()
        btn.state(["disabled"])
        if len(elec_switch_choice) == len(elec_switches_rand):
            check_guess()

    def enable_all_buttons():
        for b in buttons:
            b.state(["!disabled"])

    def animate_progress(target_value):
        current_value = elec_pb['value']
        if current_value < target_value:
            elec_pb['value'] = min(target_value, current_value + 2)
            elec_fix_win.after(20, lambda: animate_progress(target_value))

    def check_guess():
        nonlocal elec_switches_need
        enable_all_buttons()
        if elec_switch_choice == elec_switches_rand:
            rounds_completed[0] += 1
            elec_switches_need += 1
            if sound5: sound5.play()
            target = elec_pb['value'] + elec_pb['maximum'] / 3
            animate_progress(target)
            if rounds_completed[0] >= 3:
                seq_label.config(text="Electricity Restored!")
                elec_fix_win.after(1500, lambda: (
                    elec_fix_win.destroy(),
                    on_repair_complete()  # Callback to main game
                ))
            else:
                elec_fix_win.after(700, new_sequence)
        else:
            if sound6: sound6.play()
            seq_label.config(text="Wrong! New sequence...")
            elec_fix_win.after(1000, new_sequence)

    # Build keypad
    for num in range(1, 10):
        btn = ttk.Button(btn_frame, text=str(num))
        btn.configure(command=lambda n=str(num), b=btn: switch(n, b))
        btn.grid(row=(num-1)//3, column=(num-1)%3, padx=5, pady=5)
        buttons.append(btn)

    new_sequence()