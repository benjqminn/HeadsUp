import tkinter as tk
from queue import Empty

class MiniOverlay:
    def __init__(self, command_queue):
        self.command_queue = command_queue
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.configure(bg="#000000", padx=10, pady=5)
        self.root.attributes('-alpha', 0.85)

        self.label = tk.Label(
            self.root,
            text="Good Posture",
            font=("Segoe UI", 14, "bold"),
            fg="white",
            bg="#000000"
        )
        self.label.pack()

        self.set_position()

        self.root.after(100, self.poll_queue)
        self.root.mainloop()

    def set_position(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width = 160
        height = 40
        x = screen_width - width - 20
        y = screen_height - height - 60
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def poll_queue(self):
        try:
            while True:
                command = self.command_queue.get_nowait()
                if command == "show":
                    self.show_slouch()
                elif command == "hide":
                    self.show_good()
        except Empty:
            pass
        self.root.after(100, self.poll_queue)

    def show_slouch(self):
        self.label.config(text="BAD POSTURE", fg="red")

    def show_good(self):
        self.label.config(text="Good Posture", fg="white")
