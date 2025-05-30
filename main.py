import threading
import signal
import sys
import tkinter as tk
import queue  

from app.gui import start_gui
from app.overlay import OverlayApp
from app.overlay_window import MiniOverlay

def signal_handler(sig, frame):
    print("\n[HeadsUp] Ctrl+C detected. Exiting gracefully...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    overlay_command_queue = queue.Queue()
    mini_overlay_command_queue = queue.Queue()

    root = tk.Tk()
    root.withdraw()

    threading.Thread(
        target=lambda: OverlayApp(tk.Toplevel(root), overlay_command_queue),
        daemon=True
    ).start()

    threading.Thread(
        target=MiniOverlay,
        args=(mini_overlay_command_queue,),
        daemon=True
    ).start()

    start_gui(overlay_command_queue, root, mini_overlay_command_queue)
