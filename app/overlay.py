import tkinter as tk

class OverlayApp:
    def __init__(self, root, command_queue):
        self.command_queue = command_queue
        self.root = root
        self.overlay = None
        self.root.after(100, self.check_queue)

    def show_overlay(self):
        if self.overlay is not None:
            return

        self.overlay = tk.Toplevel(self.root)
        self.overlay.attributes('-fullscreen', True)
        self.overlay.attributes('-topmost', True)
        self.overlay.configure(bg='black')
        self.overlay.overrideredirect(True)

        tk.Label(
            self.overlay,
            text="FIX YOUR POSTURE",
            font=("Segoe UI", 48, "bold"),
            fg="red",
            bg="black"
        ).pack(expand=True)

        self.overlay.focus_force()

    def hide_overlay(self):
        if self.overlay:
            self.overlay.destroy()
            self.overlay = None

    def check_queue(self):
        try:
            while True:
                command = self.command_queue.get_nowait()
                if command == "show":
                    print("[Overlay] Showing overlay")
                    self.show_overlay()
                elif command == "hide":
                    print("[Overlay] Hiding overlay")
                    self.hide_overlay()
        except:
            pass
        self.root.after(100, self.check_queue)
