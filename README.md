<p>
  <img src="assets/HeadsUp_Logo.png"/>
</p>

---

# HeadsUp - Real-Time Posture Monitoring App

**HeadsUp** is a real-time posture monitoring and correction tool built using **OpenCV**, **MediaPipe**, and **Tkinter**. Designed to improve your ergonomic habits, it detects head tilts via webcam and alerts you when your posture strays from optimal alignment.

Created as a solo open-source project by Benjamin Taylor, this desktop app combines computer vision, system overlays, and a minimalist interface to run seamlessly in the background during whatever you may be doing.

---

## 🔧 Features

- 🧠 **AI-Powered Posture Detection** via MediaPipe FaceMesh  
- 🎯 Detects subtle head tilts using eye alignment
- ⏱️ Dual Alert System:
  - Mini overlay after **0.1s tilt**
  - Full overlay after **3s sustained tilt**
- 🔲 Clean GUI dashboard to start/stop detection
- 📌 Floating status overlay always visible
- 🪞 Mirrored camera feed to match user orientation
- 💻 Lightweight desktop app with minimal CPU usage
- 🌐 GitHub and LinkedIn profile buttons for dev contact

---

## 🚀 Screenshots

### Coming soon
---

## 🖥️ How It Works

1. Launch the app and click "Start Monitoring"
2. The webcam starts detecting your head alignment
3. If your head tilts beyond '2°':
   - After **0.1s**, the mini overlay appears saying 'Fix Your Posture'
   - After **3s**, the full-screen overlay activates
4. Sit upright to auto-clear both overlays

---

## 🧪 Dev Setup Instructions

```bash
# Clone the repo
git clone https://github.com/benjqminn/HeadsUp.git
cd HeadsUp

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Launch the app
python main.py
