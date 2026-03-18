import subprocess
import sys
import importlib
import threading
import tkinter as tk
from tkinter import ttk

PACKAGES = ['sv_ttk', 'pygame-ce']

def install_and_import(package, log_callback, progress_callback, done_event):
    try:
        importlib.import_module(package)
        log_callback(f"✔ {package} is already installed.\n")
    except ImportError:
        log_callback(f"⬇ Installing {package}...\n")
        try:
            process = subprocess.Popen(
                [sys.executable, "-m", "pip", "install", package],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            for line in process.stdout:
                log_callback(line)
            process.wait()
            if process.returncode == 0:
                log_callback(f"✔ Successfully installed {package}.\n")
            else:
                log_callback(f"✖ Failed to install {package}.\n")
        except Exception as e:
            log_callback(f"✖ Error: {e}\n")

def run_installs(log_callback, progress_var, status_var, finish_callback):
    total = len(PACKAGES)
    for i, pkg in enumerate(PACKAGES):
        status_var.set(f"Installing {pkg}... ({i+1}/{total})")
        install_and_import(pkg, log_callback, None, None)
        progress_var.set(int((i + 1) / total * 100))
    status_var.set("All done!")
    finish_callback()

class InstallerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Module Installer")
        self.geometry("520x400")
        self.resizable(False, False)
        self.configure(bg="#1e1e2e")

        # Title bar area
        header = tk.Frame(self, bg="#313244", pady=12)
        header.pack(fill="x")
        tk.Label(header, text="🔧  Module Installer", font=("Segoe UI", 14, "bold"),
                 fg="#cdd6f4", bg="#313244").pack()
        tk.Label(header, text="Installing required packages for your environment",
                 font=("Segoe UI", 9), fg="#a6adc8", bg="#313244").pack()

        # Log box
        log_frame = tk.Frame(self, bg="#1e1e2e", padx=16, pady=10)
        log_frame.pack(fill="both", expand=True)
        self.log_text = tk.Text(log_frame, bg="#181825", fg="#cdd6f4",
                                font=("Consolas", 9), relief="flat",
                                insertbackground="#cdd6f4", state="disabled",
                                wrap="word", bd=0, highlightthickness=1,
                                highlightbackground="#45475a")
        self.log_text.pack(fill="both", expand=True)

        # Progress bar
        bottom = tk.Frame(self, bg="#1e1e2e", padx=16, pady=8)
        bottom.pack(fill="x")

        self.status_var = tk.StringVar(value="Preparing...")
        tk.Label(bottom, textvariable=self.status_var, font=("Segoe UI", 9),
                 fg="#a6adc8", bg="#1e1e2e", anchor="w").pack(fill="x")

        self.progress_var = tk.IntVar(value=0)
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("green.Horizontal.TProgressbar",
                        troughcolor="#313244", background="#a6e3a1",
                        darkcolor="#a6e3a1", lightcolor="#a6e3a1", bordercolor="#1e1e2e")
        self.progressbar = ttk.Progressbar(bottom, variable=self.progress_var,
                                           maximum=100, length=488,
                                           style="green.Horizontal.TProgressbar")
        self.progressbar.pack(pady=(4, 0))

        # Close button (hidden until done)
        self.close_btn = tk.Button(self, text="Close", command=self.destroy,
                                   bg="#a6e3a1", fg="#1e1e2e",
                                   font=("Segoe UI", 10, "bold"),
                                   relief="flat", cursor="hand2",
                                   padx=20, pady=6, state="disabled")
        self.close_btn.pack(pady=(0, 14))

        self.after(300, self.start_installation)

    def log(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message)
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def start_installation(self):
        thread = threading.Thread(
            target=run_installs,
            args=(self.log, self.progress_var, self.status_var, self.on_done),
            daemon=True
        )
        thread.start()

    def on_done(self):
        self.close_btn.configure(state="normal")
        # Auto-close after 1 second to let user see the completion message
        self.after(1000, self.destroy)

if __name__ == "__main__":
    app = InstallerApp()
    app.mainloop()
