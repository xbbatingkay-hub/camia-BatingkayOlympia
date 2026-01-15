import os
import pygame
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import subprocess
import sys

# i swear, this was a pain in the a## to make. If this so much as breaks,
# i will personally delete the ENTIRE, and i mean the ENTIRE repo. I dont care if i will get a 0, I CANT DO STUFF LIKE THIS IN 5 MINUTES
class AudioLooper:
    """Manages looping audio playback with ability to go to next file in folder."""
    
    def __init__(self):
        pygame.mixer.init()
        self.current_index = 0
        self.is_playing = False
        self.audio_files = []
        self.load_audio_files()
    
    def load_audio_files(self):
        """Load all audio files from the custom_mus_audio folder."""
        audio_folder = Path(__file__).parent / "custom_mus_audio"
        
        if not audio_folder.exists():
            audio_folder.mkdir(exist_ok=True)
            return
        
        # Supported audio formats
        audio_extensions = {'.mp3', '.wav', '.ogg', '.flac', '.mid', '.midi'}
        
        self.audio_files = sorted([
            f for f in audio_folder.iterdir() 
            if f.is_file() and f.suffix.lower() in audio_extensions
        ])
    
    def play(self, loop=True):
        """Play audio with looping."""
        if not self.audio_files:
            return False
        
        current_file = self.audio_files[self.current_index]
        
        try:
            pygame.mixer.music.load(str(current_file))
            pygame.mixer.music.play(-1 if loop else 0)  # -1 for infinite loop, 0 for play once
            self.is_playing = True
            return True
        except pygame.error:
            return False
    
    def next_file(self):
        """Move to the next audio file and play it."""
        if not self.audio_files:
            return False
        
        self.current_index = (self.current_index + 1) % len(self.audio_files)
        return self.play(loop=True)
    
    def previous_file(self):
        """Move to the previous audio file and play it."""
        if not self.audio_files:
            return False
        
        self.current_index = (self.current_index - 1) % len(self.audio_files)
        return self.play(loop=True)
    
    def stop(self):
        """Stop audio playback."""
        pygame.mixer.music.stop()
        self.is_playing = False
    
    def pause(self):
        """Pause audio playback."""
        pygame.mixer.music.pause()
    
    def unpause(self):
        """Resume audio playback."""
        pygame.mixer.music.unpause()
    
    def get_current_file(self):
        """Get the name of the currently playing file."""
        if self.audio_files:
            return self.audio_files[self.current_index].name
        return None
    
    def set_volume(self, volume):
        """Set volume (0.0 to 1.0)."""
        pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))
    
    def is_music_playing(self):
        """Check if music is currently playing."""
        return pygame.mixer.music.get_busy()


class AudioGUI:
    """GUI for the audio looper."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("900x650")
        
        self.looper = AudioLooper()
        self.update_thread = None
        self.running = True
        
        self.setup_ui()
        self.start_update_loop()
    
    def setup_ui(self):
        """Setup the GUI components."""
        # Title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(pady=10)
        title_label = ttk.Label(title_frame, text="🎵 Music player", font=("Arial", 16, "bold"))
        title_label.pack()
        
        # Warning label
        warning_frame = ttk.Frame(self.root)
        warning_frame.pack(pady=5)
        warning_label = ttk.Label(warning_frame, text="⚠️ Close ONLY with the Quit button or the program won't exit properly!", 
                                  font=("Arial", 9), foreground="red")
        warning_label.pack()
        
        # Current file display
        file_frame = ttk.LabelFrame(self.root, text="Now Playing", padding=10)
        file_frame.pack(padx=10, pady=10, fill=tk.X)
        
        self.file_label = ttk.Label(file_frame, text="No file loaded", font=("Arial", 12), wraplength=450)
        self.file_label.pack()
        
        # File list
        list_frame = ttk.LabelFrame(self.root, text="Audio Files", padding=10)
        list_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.file_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=8)
        self.file_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.file_listbox.yview)
        
        # Populate listbox
        self.update_file_list()
        
        # Control buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10, fill=tk.X, padx=10)
        
        self.play_btn = ttk.Button(button_frame, text="▶ Play", command=self.play_current)
        self.play_btn.grid(row=0, column=0, padx=5)
        
        self.pause_btn = ttk.Button(button_frame, text="⏸ Pause", command=self.pause_playback)
        self.pause_btn.grid(row=0, column=1, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="⏹ Stop", command=self.stop_playback)
        self.stop_btn.grid(row=0, column=2, padx=5)
        
        self.quit_btn = ttk.Button(button_frame, text="❌ Quit", command=self.on_closing)
        self.quit_btn.grid(row=0, column=3, padx=5)
        
        # Previous/Next buttons
        nav_frame = ttk.Frame(self.root)
        nav_frame.pack(pady=5, fill=tk.X, padx=10)
        
        self.prev_btn = ttk.Button(nav_frame, text="⏮ Previous", command=self.previous_file)
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.next_btn = ttk.Button(nav_frame, text="Next ⏭", command=self.next_file)
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        self.open_folder_btn = ttk.Button(nav_frame, text="📁 Open Folder", command=self.open_audio_folder)
        self.open_folder_btn.pack(side=tk.LEFT, padx=5)
        
        # Volume control
        volume_frame = ttk.Frame(self.root)
        volume_frame.pack(pady=10, fill=tk.X, padx=10)
        
        ttk.Label(volume_frame, text="Volume:").pack(side=tk.LEFT, padx=5)
        self.volume_slider = ttk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.change_volume)
        self.volume_slider.set(70)
        self.volume_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.volume_label = ttk.Label(volume_frame, text="70%", width=4)
        self.volume_label.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_file_list(self):
        """Update the listbox with audio files."""
        self.file_listbox.delete(0, tk.END)
        for i, file in enumerate(self.looper.audio_files):
            prefix = "▶ " if i == self.looper.current_index else "  "
            self.file_listbox.insert(tk.END, f"{prefix}{file.name}")
        
        if not self.looper.audio_files:
            self.file_listbox.insert(tk.END, "(No audio files in custom_mus_audio folder)")
    
    def play_current(self):
        """Play the current file."""
        if self.looper.audio_files:
            self.looper.play(loop=True)
            self.update_display()
    
    def pause_playback(self):
        """Pause playback."""
        if self.looper.is_music_playing():
            self.looper.pause()
        else:
            self.looper.unpause()
        self.update_display()
    
    def stop_playback(self):
        """Stop playback."""
        self.looper.stop()
        self.update_display()
    
    def next_file(self):
        """Go to next file."""
        self.looper.next_file()
        self.update_display()
        self.update_file_list()
    
    def previous_file(self):
        """Go to previous file."""
        self.looper.previous_file()
        self.update_display()
        self.update_file_list()
    
    def change_volume(self, value):
        """Change volume."""
        volume = int(float(value)) / 100
        self.looper.set_volume(volume)
        if hasattr(self, 'volume_label'):
            self.volume_label.config(text=f"{int(float(value))}%")
    
    def update_display(self):
        """Update the GUI display."""
        current_file = self.looper.get_current_file()
        if current_file:
            self.file_label.config(text=current_file)
        else:
            self.file_label.config(text="No file loaded")
        
        if self.looper.is_music_playing():
            self.status_label.config(text="▶ Playing")
        else:
            self.status_label.config(text="⏸ Paused")
    
    def start_update_loop(self):
        """Start the background update loop."""
        # Schedule update without blocking - runs every 1000ms
        if self.running:
            self.update_display()
            self.root.after(1000, self.start_update_loop)
    
    def on_closing(self):
        """Handle window closing."""
        self.running = False
        self.looper.stop()
        self.root.destroy()
    
    def open_audio_folder(self):
        """Open the custom_mus_audio folder in file explorer."""
        audio_folder = Path(__file__).parent / "custom_mus_audio"
        if audio_folder.exists():
            # Windows
            if os.name == 'nt':
                os.startfile(str(audio_folder))
            # macOS
            elif sys.platform == 'darwin':
                subprocess.Popen(['open', str(audio_folder)])
            # Linux
            else:
                subprocess.Popen(['xdg-open', str(audio_folder)])


if __name__ == "__main__":
    root = tk.Tk()
    gui = AudioGUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.on_closing)
    root.mainloop()

# Can i please stop putting comments on everything, my index fingers hurt :-(