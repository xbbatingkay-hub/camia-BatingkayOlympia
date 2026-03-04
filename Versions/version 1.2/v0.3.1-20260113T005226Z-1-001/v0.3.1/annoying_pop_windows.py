import tkinter as tk
from tkinter import messagebox
import random
import threading
import time
from PIL import Image, ImageTk
import os
import pygame

# ========== EASY CUSTOMIZATION SECTION ==========
# Define your popup content here! Easy to add/edit text and images
# INSTRUCTIONS:
# 1. "type": Choose "normal" (closes easily), "multiplying" (spawns copies), or "image" (full-screen)
# 2. "text": Your popup message text (only used for "normal" and "multiplying" types)
# 3. "image": Just filename like "meme.png" (looks in custom_images folder automatically!)
# 4. "audio": Just filename like "sound.mp3" (looks in custom_audio folder automatically!)
# 5. "bg_color": Hex color code like "#FF6B6B" for background
# 
# QUICK START:
# - Add image: Change "image": None to "image": "meme.png" (no path needed!)
# - Add audio: Change "audio": None to "audio": "notification.mp3" (no path needed!)
# - Change text: Edit the "text" value
# - Change color: Edit the "bg_color" hex code
#
# EXAMPLE with image and audio:
# {
#     "type": "normal",
#     "text": "Check this out!",
#     "image": "pic.png",
#     "audio": "notification.mp3",
#     "bg_color": "#FF6B6B",
# },

POPUP_CONFIGS = [
    # ===== NORMAL POPUPS - Just close normally =====
    # These popups close with one button and auto-close after 5-15 seconds
    {
        "type": "normal",
        "text": "🎉 CONGRATULATIONS! You've won!",
        "image": None,  # <-- Just use filename like "meme.png" (no path needed!)
        "audio": None,  # <-- Just use filename like "sound.mp3" (no path needed!)
        "bg_color": "#FF6B6B",
    },
    {
        "type": "normal",
        "text": "⚠️ CLICK HERE - Limited Time Offer!",
        "image": None,  # <-- Just use filename like "pic.png"
        "audio": None,  # <-- Just use filename like "ding.mp3"
        "bg_color": "#FFC0CB",
    },
    {
        "type": "normal",
        "text": "💰 FREE MONEY! Don't Miss Out!",
        "image": None,  # <-- Just use filename
        "audio": None,  # <-- Just use filename
        "bg_color": "#FFD700",
    },
    
    # ===== MULTIPLYING POPUPS - Spawns copies when you click Close =====
    # These popups have 2 buttons:
    # - "OK, I Understand" = closes normally
    # - "Close" = spawns 2-3 MORE copies (tricky!)
    {
        "type": "multiplying",
        "text": "🚨 WARNING: Your Computer Needs Attention!",
        "image": None,  # <-- Just use filename
        "audio": None,  # <-- Just use filename
        "bg_color": "#FF4500",
    },
    {
        "type": "multiplying",
        "text": "👑 EXCLUSIVE DEAL - TODAY ONLY!",
        "image": None,  # <-- Just use filename
        "audio": None,  # <-- Just use filename
        "bg_color": "#FF1493",
    },
    {
        "type": "multiplying",
        "text": "📱 Download Now and Get Rich!",
        "image": None,  # <-- Just use filename
        "audio": None,  # <-- Just use filename
        "bg_color": "#00CED1",
    },
    
    # ===== IMAGE POPUPS - Full window image =====
    # These popups show a full-screen image with just a Close button
    # Perfect for memes, screenshots, or custom ads!
    {
        "type": "image",
        "image": None,  # <-- REPLACE with "yourimage.png" (just filename!)
        "audio": None,  # <-- REPLACE with "yoursound.mp3" (optional, just filename!)
        "bg_color": "#000000",
    },
    {
        "type": "image",
        "image": None,  # <-- REPLACE with "yourimage.png" (just filename!)
        "audio": None,  # <-- REPLACE with "yoursound.mp3" (optional, just filename!)
        "bg_color": "#000000",
    },
]

# ========== END CUSTOMIZATION SECTION ==========

# Initialize pygame mixer for audio
try:
    pygame.mixer.init()
except:
    print("Warning: Could not initialize audio. Some popups may not have sound.")

def play_audio(audio_path):
    """Play audio file in a separate thread."""
    try:
        if audio_path:
            # Check if file exists as-is, otherwise look in custom_audio folder
            if not os.path.exists(audio_path):
                audio_path = os.path.join("custom_audio", audio_path)
            
            if os.path.exists(audio_path):
                def play():
                    try:
                        pygame.mixer.music.load(audio_path)
                        pygame.mixer.music.play()
                    except Exception as e:
                        print(f"Error playing audio {audio_path}: {e}")
                
                audio_thread = threading.Thread(target=play, daemon=True)
                audio_thread.start()
    except Exception as e:
        print(f"Error with audio {audio_path}: {e}")

class PopupAdSpawner:
    def __init__(self, master, spawn_interval=random.randint(10,30), max_windows=5):
        """
        Initialize the popup ad spawner.
        
        Args:
            master: The root tkinter window
            spawn_interval: Time in seconds between popup spawns (default: 2)
            max_windows: Maximum number of popups to allow (default: 5)
        """
        self.master = master
        self.spawn_interval = spawn_interval
        self.max_windows = max_windows
        self.active_windows = []
        self.running = False
        
        # Use popup configs from above
        self.popup_configs = POPUP_CONFIGS
        
        # Setup main window
        self.master.title("Popup Ad Spawner")
        self.master.geometry("300x150")
        
        # Create buttons
        self.start_btn = tk.Button(
            self.master, 
            text="Start Spawning Popups", 
            command=self.start_spawning,
            bg="red",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.start_btn.pack(pady=10)
        
        self.stop_btn = tk.Button(
            self.master, 
            text="Stop Spawning", 
            command=self.stop_spawning,
            bg="green",
            fg="white",
            font=("Arial", 10, "bold"),
            state=tk.DISABLED
        )
        self.stop_btn.pack(pady=5)
        
        self.close_all_btn = tk.Button(
            self.master, 
            text="Close All Popups", 
            command=self.close_all_popups,
            bg="orange",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.close_all_btn.pack(pady=5)
        
        self.status_label = tk.Label(
            self.master, 
            text="Status: Idle",
            font=("Arial", 9)
        )
        self.status_label.pack(pady=10)
    
    def start_spawning(self):
        """Start the popup spawning thread."""
        if not self.running:
            self.running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_label.config(text="Status: SPAWNING!", fg="red")
            
            # Start spawning in a separate thread
            spawn_thread = threading.Thread(target=self._spawn_loop, daemon=True)
            spawn_thread.start()
    
    def stop_spawning(self):
        """Stop the popup spawning."""
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Stopped", fg="black")
    
    def _spawn_loop(self):
        """Main loop for spawning popups."""
        while self.running:
            if len(self.active_windows) < self.max_windows:
                self.spawn_popup()
            time.sleep(self.spawn_interval)
    
    def spawn_popup(self):
        """Create and display a random popup window."""
        # Create new popup window
        popup = tk.Toplevel(self.master)
        popup.title("★ AMAZING OFFER ★")
        
        # Random size
        width = random.randint(250, 450)
        height = random.randint(200, 400)
        
        # Random position
        x = random.randint(0, 1200)
        y = random.randint(0, 700)
        
        popup.geometry(f"{width}x{height}+{x}+{y}")
        
        # Select random config
        config = random.choice(self.popup_configs)
        popup.config(bg=config["bg_color"])
        popup_type = config.get("type", "normal")
        
        # Play audio if provided
        if config.get("audio"):
            play_audio(config["audio"])
        
        # ===== IMAGE POPUPS - Full window image =====
        if popup_type == "image":
            image_path = config["image"]
            # Check if file exists as-is, otherwise look in custom_images folder
            if image_path and not os.path.exists(image_path):
                image_path = os.path.join("custom_images", image_path)
            
            if image_path and os.path.exists(image_path):
                try:
                    img = Image.open(image_path)
                    img = img.resize((width, height), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    
                    img_label = tk.Label(popup, image=photo, bg=config["bg_color"])
                    img_label.image = photo
                    img_label.pack(fill=tk.BOTH, expand=True)
                except Exception as e:
                    print(f"Error loading image {image_path}: {e}")
            else:
                # Empty frame placeholder if no image
                placeholder = tk.Label(
                    popup,
                    text="IMAGE PLACEHOLDER\n(Add image path to config)",
                    font=("Arial", 14, "bold"),
                    bg="#444444",
                    fg="white"
                )
                placeholder.pack(fill=tk.BOTH, expand=True)
            
            # For image popups, just a close button
            def close_image():
                if popup in self.active_windows:
                    self.active_windows.remove(popup)
                popup.destroy()
            
            close_btn = tk.Button(popup, text="Close", command=close_image, bg="white", font=("Arial", 9, "bold"))
            close_btn.pack(pady=5)
        
        # ===== NORMAL POPUPS - Just text with normal close =====
        elif popup_type == "normal":
            # Create main frame for content
            content_frame = tk.Frame(popup, bg=config["bg_color"])
            content_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
            
            # Add image if provided
            if config.get("image"):
                image_path = config["image"]
                # Check if file exists as-is, otherwise look in custom_images folder
                if not os.path.exists(image_path):
                    image_path = os.path.join("custom_images", image_path)
                
                if os.path.exists(image_path):
                    try:
                        img = Image.open(image_path)
                        img.thumbnail((200, 200), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(img)
                        
                        img_label = tk.Label(content_frame, image=photo, bg=config["bg_color"])
                        img_label.image = photo
                        img_label.pack(pady=5)
                    except Exception as e:
                        print(f"Error loading image {image_path}: {e}")
            
            # Add message
            message = config.get("text", "Check this out!")
            label = tk.Label(
                content_frame,
                text=message,
                font=("Arial", 12, "bold"),
                bg=config["bg_color"],
                fg="white",
                wraplength=width - 20
            )
            label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
            
            # Normal close button
            button_frame = tk.Frame(popup, bg=config["bg_color"])
            button_frame.pack(pady=10)
            
            def close_normal():
                if popup in self.active_windows:
                    self.active_windows.remove(popup)
                popup.destroy()
            
            close_btn = tk.Button(
                button_frame,
                text="Close",
                command=close_normal,
                bg="white",
                font=("Arial", 9, "bold")
            )
            close_btn.pack(padx=5)
        
        # ===== MULTIPLYING POPUPS - Spawn copies unless acknowledged =====
        elif popup_type == "multiplying":
            # Create main frame for content
            content_frame = tk.Frame(popup, bg=config["bg_color"])
            content_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
            
            # Add image if provided
            if config.get("image"):
                image_path = config["image"]
                # Check if file exists as-is, otherwise look in custom_images folder
                if not os.path.exists(image_path):
                    image_path = os.path.join("custom_images", image_path)
                
                if os.path.exists(image_path):
                    try:
                        img = Image.open(image_path)
                        img.thumbnail((200, 200), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(img)
                        
                        img_label = tk.Label(content_frame, image=photo, bg=config["bg_color"])
                        img_label.image = photo
                        img_label.pack(pady=5)
                    except Exception as e:
                        print(f"Error loading image {image_path}: {e}")
            
            # Add message
            message = config.get("text", "Check this out!")
            label = tk.Label(
                content_frame,
                text=message,
                font=("Arial", 12, "bold"),
                bg=config["bg_color"],
                fg="white",
                wraplength=width - 20
            )
            label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
            
            # Add buttons
            button_frame = tk.Frame(popup, bg=config["bg_color"])
            button_frame.pack(pady=10)
            
            # Acknowledge button (just closes)
            def acknowledge():
                if popup in self.active_windows:
                    self.active_windows.remove(popup)
                popup.destroy()
            
            ack_btn = tk.Button(
                button_frame,
                text="OK, I Understand",
                command=acknowledge,
                bg="lightgreen",
                font=("Arial", 9, "bold")
            )
            ack_btn.pack(side=tk.LEFT, padx=5)
            
            # Close button that spawns MORE (tricky!)
            def spawn_more():
                if popup in self.active_windows:
                    self.active_windows.remove(popup)
                popup.destroy()
                
                # Spawn 2-3 copies
                for _ in range(random.randint(2, 3)):
                    if self.running:
                        self.spawn_popup()
            
            close_btn = tk.Button(
                button_frame,
                text="Close",
                command=spawn_more,
                bg="red",
                fg="white",
                font=("Arial", 9, "bold")
            )
            close_btn.pack(side=tk.LEFT, padx=5)
        
        # Track this window
        self.active_windows.append(popup)
        
        # Update status
        self.status_label.config(
            text=f"Status: {len(self.active_windows)} popups active"
        )
        
        # Auto-close after random time (5-15 seconds) - but not multiplying ones
        if popup_type != "multiplying":
            def auto_close():
                time.sleep(random.randint(5, 15))
                try:
                    if popup in self.active_windows:
                        self.active_windows.remove(popup)
                    popup.destroy()
                    self.status_label.config(
                        text=f"Status: {len(self.active_windows)} popups active"
                    )
                except:
                    pass
            
            auto_thread = threading.Thread(target=auto_close, daemon=True)
            auto_thread.start()
    
    def close_all_popups(self):
        """Close all active popup windows."""
        for popup in self.active_windows[:]:
            try:
                popup.destroy()
            except:
                pass
        self.active_windows.clear()
        self.status_label.config(text="Status: All popups closed")


def main():
    """Main function to run the popup spawner."""
    root = tk.Tk()
    # ===== SETTINGS YOU CAN ADJUST =====
    # spawner = PopupAdSpawner(root, spawn_interval=2, max_windows=5)
    # spawn_interval: How many seconds between each popup spawn (lower = more frequent)
    # max_windows: Maximum number of popups allowed at once
    spawner = PopupAdSpawner(root, spawn_interval=2, max_windows=5)
    root.mainloop()


if __name__ == "__main__":
    main()
