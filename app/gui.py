import tkinter as tk
import threading
from PIL import Image, ImageTk
import os
import webbrowser
from app.detector import run_detection

def start_gui(overlay_command_queue, root, mini_overlay_command_queue=None):
    root.deiconify()
    root.title("HeadsUp: Posture Monitor")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = int(screen_width * 0.8)
    height = int(screen_height * 0.8)
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.configure(bg="#121212")

    is_running = {"running": False}

    def start_monitoring():
        if not is_running["running"]:
            is_running["running"] = True
            threading.Thread(
                target=run_detection,
                args=(is_running, overlay_command_queue, mini_overlay_command_queue),
                daemon=True
            ).start()
            status_label.config(text="🟢 Monitoring Active", fg="#00FFB3")

    def stop_monitoring():
        is_running["running"] = False
        status_label.config(text="⏸️ Monitoring Paused", fg="#FFB347")

    def on_close():
        is_running["running"] = False
        root.destroy()

    logo_path = os.path.join("app", "assets", "HeadsUp_Logo.png")
    if os.path.exists(logo_path):
        try:
            img = Image.open(logo_path).resize((150, 150), Image.LANCZOS)
            logo = ImageTk.PhotoImage(img)
            logo_label = tk.Label(root, image=logo, bg="#121212")
            logo_label.image = logo  
            logo_label.pack(pady=(40, 10))
        except Exception as e:
            print(f"[HeadsUp] Failed to load logo: {e}")

    title = tk.Label(
        root,
        text="HeadsUp",
        font=("Segoe UI", 40, "bold"),
        bg="#121212",
        fg="#00FFC6"
    )
    title.pack(pady=(0, 20))

    button_style = {
        "font": ("Segoe UI", 16, "bold"),
        "width": 25,
        "height": 2,
        "relief": "flat",
        "bd": 0,
        "highlightthickness": 0
    }

    start_btn = tk.Button(
        root, text="▶️ Start Monitoring", command=start_monitoring,
        bg="#00AA88", fg="white", activebackground="#00FFCC", **button_style
    )
    start_btn.pack(pady=10)

    stop_btn = tk.Button(
        root, text="⏹️ Stop Monitoring", command=stop_monitoring,
        bg="#FF4444", fg="white", activebackground="#FF8888", **button_style
    )
    stop_btn.pack(pady=10)

    status_label = tk.Label(
        root,
        text="⏸️ Monitoring Paused",
        font=("Segoe UI", 14, "bold"),
        bg="#121212",
        fg="#FFB347"
    )
    status_label.pack(pady=30)

    note = tk.Label(
        root,
        text="Tip: Press 'q' in the webcam window to quit",
        font=("Segoe UI", 10),
        bg="#121212",
        fg="#666666"
    )
    note.pack(pady=10)

    links_frame = tk.Frame(root, bg="#121212")
    links_frame.pack(pady=(20, 40))

    def open_github():
        webbrowser.open_new("https://github.com/benjqminn")

    def open_linkedin():
        webbrowser.open_new("https://linkedin.com/in/btayl106")

    github_icon_path = os.path.join("app", "assets", "github.png")
    linkedin_icon_path = os.path.join("app", "assets", "linkedin.png")

    if os.path.exists(github_icon_path):
        try:
            gh_img = Image.open(github_icon_path).resize((30, 30), Image.LANCZOS)
            github_icon = ImageTk.PhotoImage(gh_img)
            github_btn = tk.Button(
                links_frame, image=github_icon, command=open_github,
                bg="#121212", bd=0, highlightthickness=0, activebackground="#121212"
            )
            github_btn.image = github_icon
            github_btn.pack(side="left", padx=10)
        except Exception as e:
            print(f"[HeadsUp] Failed to load GitHub icon: {e}")

    if os.path.exists(linkedin_icon_path):
        try:
            li_img = Image.open(linkedin_icon_path).resize((30, 30), Image.LANCZOS)
            linkedin_icon = ImageTk.PhotoImage(li_img)
            linkedin_btn = tk.Button(
                links_frame, image=linkedin_icon, command=open_linkedin,
                bg="#121212", bd=0, highlightthickness=0, activebackground="#121212"
            )
            linkedin_btn.image = linkedin_icon
            linkedin_btn.pack(side="left", padx=10)
        except Exception as e:
            print(f"[HeadsUp] Failed to load LinkedIn icon: {e}")

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
