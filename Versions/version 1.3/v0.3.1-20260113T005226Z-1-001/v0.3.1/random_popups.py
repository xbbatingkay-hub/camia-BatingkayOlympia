"""
Random Pop-ups Module for Tycoon Game
Includes three types of pop-ups:
1. Math minigame popup
2. Virus popup (multiplying)
3. Generic clickbait ad
"""

import tkinter as tk
from tkinter import messagebox
import random
import pygame
import time

# Import from main game for access to game state
# These will be set by the main game file
game_state = {}


class MathPopup(tk.Toplevel):
    """Math minigame popup that boosts money if answered correctly"""
    
    def __init__(self, parent, on_correct, on_wrong, sound10, sound11):
        super().__init__(parent)
        self.title("Jibrael's Totally Awesome Math Quiz!")
        self.geometry("400x300")
        self.resizable(False, False)
        self.on_correct = on_correct
        self.on_wrong = on_wrong
        self.sound10 = sound10
        self.sound11 = sound11
                # Center popup on parent window
        self.update_idletasks()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        popup_x = parent_x + (parent_width // 2) - 200
        popup_y = parent_y + (parent_height // 2) - 150
        self.geometry(f"+{popup_x}+{popup_y}")
                # Play math sound
        self.sound10.play()
        
        # Generate random math problem
        num1 = random.randint(5, 1500)
        num2 = random.randint(5, 1500)
        self.operator = random.choice(['+', '-', '*', '/'])
        
        if self.operator == '+':
            self.correct_answer = num1 + num2
        elif self.operator == '-':
            self.correct_answer = num1 - num2
        elif self.operator == '/':
            self.correct_answer = num1 / num2
        else:  # '*'
            self.correct_answer = num1 * num2
        
        # Title
        title_label = tk.Label(self, text="Solve This Math Problem - Jibrael!", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Problem display
        problem_label = tk.Label(self, text=f"{num1} {self.operator} {num2} = ?", font=("Arial", 24, "bold"))
        problem_label.pack(pady=20)
        
        # Input field
        self.answer_entry = tk.Entry(self, font=("Arial", 14), width=20, justify="center")
        self.answer_entry.pack(pady=10)
        self.answer_entry.focus()
        self.answer_entry.bind("<Return>", lambda e: self.check_answer())
        
        # Button frame
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)
        
        submit_button = tk.Button(button_frame, text="Submit", command=self.check_answer, font=("Arial", 12), width=10)
        submit_button.grid(row=0, column=0, padx=5)
        
        skip_button = tk.Button(button_frame, text="Skip", command=self.on_skip, font=("Arial", 12), width=10)
        skip_button.grid(row=0, column=1, padx=5)
        
        self.attributes('-topmost', True)
    
    def check_answer(self):
        try:
            user_answer = int(self.answer_entry.get())
            if user_answer == self.correct_answer:
                messagebox.showinfo("Correct!", "WOW YOU EXIST! +500G and +50 EXP!")
                self.on_correct()
                self.destroy()
            else:
                if self.operator == "/":
                    if user_answer == round(self.correct_answer,2):
                        messagebox.showinfo("Correct!", "WOW YOU EXIST! +500G and +50 EXP!")
                        self.on_correct()
                        self.destroy()
                else:
                    messagebox.showerror("INCORRECT!", f"I HEAR MATH THAT BAD! The correct answer was {self.correct_answer}.\n-500G!")
                    self.on_wrong()
                    self.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a number!")
    
    def on_skip(self):
        self.destroy()


class VirusPopup(tk.Toplevel):
    """Virus popup with ragebait that multiplies if you say no"""
    
    def __init__(self, parent, on_yes, on_no, sound8, virus_count=1):
        super().__init__(parent)
        self.title(" WARNING!")
        self.geometry("450x250")
        self.resizable(False, False)
        self.on_yes = on_yes
        self.on_no = on_no
        self.sound8 = sound8
        self.virus_count = virus_count
        
        # Center popup on parent window
        self.update_idletasks()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        popup_x = parent_x + (parent_width // 2) - 225
        popup_y = parent_y + (parent_height // 2) - 125
        self.geometry(f"+{popup_x}+{popup_y}")
        
        
        # Ragebait messages
        ragebait_messages = [
            "YOUR COMPUTER HAS A VIRUS!",
            "CRITICAL ALERT: System Compromise Detected!",
            "OMG! You won't BELIEVE what happened next!",
            "Doctors HATE this ONE WEIRD TRICK!",
            "This ANCIENT SECRET will SHOCK you!",
            "BREAKING: Scientists Discover TRUTH!",
            "This Video is SO DISTURBING it was BANNED!",
            "will you wake up tomorrow?",
            "L E A V E",
            "Is Bastijn a cool guy or nah?",
            "Jibraelli Donelli",
            "Put the pineapple on the pizza.",
            "Is anyone there?",
            "HEY PAY ATTENTION TO ME",
            "This message is sponsored by Jibrael",
            
        ]
        
        message = random.choice(ragebait_messages)
        
        # Title
        title_label = tk.Label(self, text=message, font=("Arial", 16, "bold"), fg="red")
        title_label.pack(pady=20)
        
        # Button frame
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)
        
        yes_button = tk.Button(button_frame, text="YES", command=self.on_yes_click, 
                               font=("Arial", 12), width=10, bg="green", fg="white")
        yes_button.grid(row=0, column=0, padx=10)
        
        no_button = tk.Button(button_frame, text="NO", command=self.on_no_click, 
                              font=("Arial", 12), width=10, bg="red", fg="white")
        no_button.grid(row=0, column=1, padx=10)
        
        self.attributes('-topmost', True)
    
    def on_yes_click(self):
        self.on_yes()
        # Play virus sound
        self.sound8.play()
        self.destroy()
    
    def on_no_click(self):
        # Create another virus popup (multiply!)
        self.on_no(self.virus_count + 1)
        # Play virus sound
        self.sound8.play()


class ClickbaitPopup(tk.Toplevel):
    """Generic clickbait ad popup"""
    
    def __init__(self, parent, on_close, sound9):
        super().__init__(parent)
        self.title("💰 CLICK HERE!")
        self.geometry("400x300")
        self.resizable(False, False)
        self.on_close = on_close
        self.sound9 = sound9
        
        # Center popup on parent window
        self.update_idletasks()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        popup_x = parent_x + (parent_width // 2) - 200
        popup_y = parent_y + (parent_height // 2) - 150
        self.geometry(f"+{popup_x}+{popup_y}")
        
        # Play clickbait sound
        self.sound9.play()
        
        # Clickbait messages
        clickbait_messages = [
            "Single moms in YOUR AREA want to meet YOU!",
            "CLICK HERE for FREE MONEY!",
            "You WON'T BELIEVE what happened next!",
            "Doctors HATE this ONE WEIRD TRICK!",
            "Hot Singles in YOUR AREA!",
            "You have 1000000 unclaimed WINNINGS!",
            "EXCLUSIVE: This video is TOO SPICY for YouTube!",
        ]
        
        message = random.choice(clickbait_messages)
        
        # Title
        title_label = tk.Label(self, text=message, font=("Arial", 14, "bold"), fg="blue")
        title_label.pack(pady=30)
        
        # Subtext
        subtext = tk.Label(self, text="(Click the X to close this ad)", font=("Arial", 10, "italic"), fg="gray")
        subtext.pack(pady=10)
        
        # Button
        close_button = tk.Button(self, text="CLOSE AD", command=self.on_close_click, 
                                font=("Arial", 12), width=20, bg="orange", fg="white")
        close_button.pack(pady=30)
        
        self.attributes('-topmost', True)
    
    def on_close_click(self):
        self.on_close()
        self.destroy()


class PopupManager:
    """Manages random popup events"""
    
    def __init__(self, parent, get_money, set_money, get_level, set_level, sound8, sound9, sound10, sound11, root):
        self.parent = parent
        self.get_money = get_money
        self.set_money = set_money
        self.get_level = get_level
        self.set_level = set_level
        self.sound8 = sound8
        self.sound9 = sound9
        self.sound10 = sound10
        self.sound11 = sound11
        self.root = root
        self.popup_active = False
        self.virus_count = 0
        self.last_popup_time = 0  # Track when last popup appeared
        self.popup_cooldown = 15  # Cooldown period in seconds (15 seconds before next popup)
        
    def trigger_random_popup(self):
        """Randomly trigger a popup event"""
        if self.popup_active:
            return
        
        # Check if cooldown period has passed
        current_time = time.time()
        if current_time - self.last_popup_time < self.popup_cooldown:
            return  # Still in cooldown
        
        # 5% chance to trigger a popup
        if random.random() < 0.05:
            self.popup_active = True
            self.last_popup_time = current_time  # Set new cooldown start
            popup_type = random.choice(['math', 'virus', 'clickbait'])
            
            if popup_type == 'math':
                self._trigger_math_popup()
            elif popup_type == 'virus':
                self._trigger_virus_popup()
            else:  # clickbait
                self._trigger_clickbait_popup()
    
    def _trigger_math_popup(self):
        """Trigger math minigame popup"""
        def on_correct():
            self.set_money(self.get_money() + 500)
            from tkinter import Label
            # Can add a visual feedback here if needed
        
        def on_wrong():
            # Decrease money by large amount
            current = self.get_money()
            loss = min(current * 0.25, current - 1)  # Lose 25% or leave with 1G
            self.set_money(current - loss)
        
        MathPopup(self.root, on_correct, on_wrong, self.sound10, self.sound11)
        self.popup_active = False
    
    def _trigger_virus_popup(self):
        """Trigger virus popup"""
        self.virus_count = 1
        
        def on_yes():
            # Cost is now based on level
            current_level = self.get_level()
            if current_level > 1:
                self.set_level(current_level - 1)
            self.popup_active = False
        
        def on_no(count):
            # Create another virus popup
            self.virus_count = count
            VirusPopup(self.root, on_yes, on_no, self.sound8, count)
        
        VirusPopup(self.root, on_yes, on_no, self.sound8, self.virus_count)
    
    def _trigger_clickbait_popup(self):
        """Trigger clickbait ad popup"""
        def on_close():
            # Just close the popup, no effect
            self.popup_active = False
        
        ClickbaitPopup(self.root, on_close, self.sound9)
    
    def schedule_popups(self):
        """Schedule random popups to trigger periodically"""
        self.trigger_random_popup()
        self.root.after(5000, self.schedule_popups)  # Check every 5 seconds
