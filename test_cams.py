import cv2
import time

print("Scanning camera indices with DEFAULT backend...\n")

for i in range(5):
    print(f"Trying camera index {i}...", end=" ")
    cap = cv2.VideoCapture(i)  

    start = time.time()
    while not cap.isOpened() and time.time() - start < 3:  
        time.sleep(0.1)

    if cap.isOpened():
        print("[SUCCESS]")
        cap.release()
    else:
        print("[FAIL]")