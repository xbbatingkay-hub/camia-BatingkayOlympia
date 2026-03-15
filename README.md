# MONOCLICKER

MONOCLICKER

MONOCLICKER (MC)


 # Problem Statement:
 - Most people are bored, but often turn to solutions that leave a negative impact on them (like doomscrolling).

 # Objectives:
 - Create a clean simulation experience for players to enjoy without too many unnecessary features.
 - Destroy boredom and be a timekiller that isn't too addictive.

 # Project Description:

 - A game aimed to destroy boredom, made to be a timekiller but not too addictive.
 - Also made to spite games in the same genre that experience common problems, such as feature bloat.



# Features:
- Clickable button to increase a number (the user's G)

- Generators that the user can purchase with G to increase G output and can be accessed via the "Shop" button.

- Slight chance for generators to break down, and requires a "minigame" using a consistent stream of user input in a limited amount of time to "fix" the generator

- Tips at the bottom of the main menu to push along progress and give the user hints as to what to do

- A timer that is put at the top of the screen that takes roughly 25% of the user's current G to slow down progress.

- A manual save system that uses JSON files to store data, such as generator amounts, inflated prices, and the user's G.

- A menu used to upgrade and fix generators, accessed via the "Generator Status" button.

- A music player you can put the music you want in!

- Rotating upgrades on the right, and your player stats on the left

  




 



# Gameplay/How to Run the Program:



- Click the button labeled "Increase G" to increase G



- Buy generators by clicking the "Shop" button and purchasing some to generate more G, but prices increase by 15% after every purchase.



- Click on the "Generator Status" Button to monitor the status of generators and upgrade the G output of different tiers of generators.



- Generate as much G as possible to minimize losses when the timer runs out.

# How to Play/Run

If using the raw Python file...

1. Install Python
2. In the selection screen, check all the boxes
3. Open the module_installer.py file in the game folder and let it install the packages needed (if you need to give it permissions, please do so)
4. Open the Python file (keep it inside its folder).

Gameplay


- Click the button for money and gain levels
- Buy generators
- Use levels to upgrade your generators
- Use the cool music player for music
- Get annoyed by randomly appearing but somewhat unobtrusive pop-ups
- Watch as your money gain gets increasingly ridiculous
- Suffer the pain of taxes
- Listen to cool music with the built-in music player in the settings! (press the folder button to add music in the custom music folder)
(Warning: If you don't hear anything, it's because you didn't activate the music player in the settings)




# Example Output

Main menu:
<img width="2559" height="1438" alt="Screenshot 2026-03-04 184347" src="https://github.com/user-attachments/assets/62aba664-b3aa-4022-88e2-a51e0cf906c4" />

Shop menu:
<img width="2559" height="1433" alt="Screenshot 2026-03-04 184350" src="https://github.com/user-attachments/assets/44b8af50-acd0-4e0f-a46b-449f7d4bac45" />

Upgrade and Status Menu
<img width="2559" height="1438" alt="Screenshot 2026-03-04 184353" src="https://github.com/user-attachments/assets/c6881db6-c083-4073-a706-3910c6d1c36e" />
<img width="2559" height="1439" alt="Screenshot 2026-03-04 184358" src="https://github.com/user-attachments/assets/0bda8008-9c62-47b1-8d95-49ea64b54d57" />

Settings: 
<img width="510" height="443" alt="Screenshot 2026-03-04 184403" src="https://github.com/user-attachments/assets/4706fb35-5e75-4ef3-a8a6-a21b04c07f5a" />

Music player:












# Methodology

Implementation of core features and Technologies used
- GUI (especially for main menu)
  - I used Tkinter for the GUI partially because I didn't know that other alternatives existed, and also because it was relatively simple for me, since I didn't work with GUI before.
  - I also used sv_ttk to make the GUI uniform and clean, although now I'm not sure if it did that, and for Dark Mode for accessibility.
- Saving and Loading
  - I used JSON files and the JSON module for saving and loading because it makes it easy to detect flaws in saves during testing, and also served as a way to look at your progress (until I added the player status widget)
- The Generators
  - They all generate G, and I used the random module for the Randomized Generator because I needed its output to be randomized.
- The Fix Minigames
  - Also used Tkinter for this stuff, and the progressbar that was already with Tkinter was useful for the timing minigame for the Randomized Generator
- Sounds
  - I used PyGame because it allows you to play multiple sounds at the same time
- Taxes
  - For the timer, I think I used time and datetime, although now I'm not sure
- Music Player
  - Honestly, I could've just made the project be this
  - I used Tkinter for GUI (labels, buttons, frames, sliders for volume control, and the list box for the list of music in the custom_mus folder)
  - os is used for allowing the program to access the custom_mus folder
  - Pygame is used for audio
- Module Installer
  - I used subprocess to call the "pip install" command to install the packages needed
  - Sys is used to get the Python executable path to make sure that pip installs in the correct Python version and exits the program if it fails
  - importlib allows the program to test if the module already exists
Backend Communication (if this counts as it)
- Functions use direct references to other functions
- The functions for each window usually use the same global variables
- Polling/update loops are used for some labels or buttons (like the money counter), such as in gen_update(), which frequently refreshes UI

Some of the other modules imported into the main game are just Python files I made to store other things, such as the extra generators, the pop-up windows, and the cool music player, or other things already included in the modules

## Contributors

- Student1: Bastijn Batingkay (User interface, general function of the program)
- Student2: Jibrael Olympia: (Graphics, game tester)



