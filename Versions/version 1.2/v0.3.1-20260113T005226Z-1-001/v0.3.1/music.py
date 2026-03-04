import os
import pygame

# Initialize the mixer
pygame.mixer.init()

# Track if music is currently playing
music_playing = False
current_track_index = 0

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the sounds folder (relative to script)
sound_folder = os.path.join(script_dir, "sounds")
sound_files = [
    "monday.mp3",
    "tuesday.mp3",
    "wednesday.mp3",
    "thursday.mp3",
    "friday.mp3"
]

# Define a custom event for music end
MUSIC_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END)

def play_music(start_index=0):
    global music_playing, current_track_index
    if not music_playing:
        current_track_index = start_index
        play_current_track()

def play_current_track():
    global music_playing, current_track_index
    if 0 <= current_track_index < len(sound_files):
        sound_file = sound_files[current_track_index]
        full_path = os.path.join(sound_folder, sound_file)
        if os.path.exists(full_path):
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.play()
            music_playing = True
        else:
            print(f"Error: {full_path} not found.")
            music_playing = False

def next_track():
    global current_track_index
    current_track_index = (current_track_index + 1) % len(sound_files)
    play_current_track()

def pause_music():
    global music_playing
    pygame.mixer.music.pause()
    music_playing = False

def resume_music():
    global music_playing
    pygame.mixer.music.unpause()
    music_playing = True

def stop_music():
    global music_playing
    pygame.mixer.music.stop()
    music_playing = False

def toggle_music():
    if pygame.mixer.music.get_busy():
        pause_music()
    else:
        resume_music()

def close():
    pygame.mixer.quit()

def check_and_advance():
    # Call this periodically from your Tkinter main file
    if music_playing and not pygame.mixer.music.get_busy():
        next_track()

def half_volume():
    pygame.mixer.music.set_volume(0.5)

def full_volume():
    pygame.mixer.music.set_volume(1)
