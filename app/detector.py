import cv2
import mediapipe as mp
import math
import time

TILT_THRESHOLD = 2              
TILT_NOTICE_DELAY = 0.1         
TILT_DURATION = 3               

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True
)

def calculate_angle(p1, p2):
    delta_x = p2[0] - p1[0]
    delta_y = p2[1] - p1[1]
    return math.degrees(math.atan2(delta_y, delta_x))

def try_open_camera(index, timeout=3):
    print(f"[HeadsUp] Trying index {index} with CAP_DSHOW...")
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    start_time = time.time()
    while not cap.isOpened() and time.time() - start_time < timeout:
        time.sleep(0.1)
    if cap.isOpened():
        print(f"[HeadsUp] Success on index {index}.")
        return cap
    else:
        print(f"[HeadsUp] Failed to open camera index {index}.")
        cap.release()
        return None

def run_detection(is_running_flag, overlay_command_queue, mini_overlay_command_queue=None):
    print("[HeadsUp] Scanning for available webcam...")

    cap = None
    for i in range(3):
        cap = try_open_camera(i)
        if cap:
            break

    if not cap:
        print("[HeadsUp ERROR] No working webcam found.")
        is_running_flag["running"] = False
        return

    print("[HeadsUp] Webcam stream active.")
    tilt_start_time = None
    mini_visible = False
    overlay_visible = False

    try:
        while is_running_flag["running"]:
            ret, frame = cap.read()
            if not ret:
                print("[HeadsUp ERROR] Failed to grab frame.")
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)

            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0]
                h, w, _ = frame.shape

                left_eye = landmarks.landmark[33]
                right_eye = landmarks.landmark[263]

                left = (int(left_eye.x * w), int(left_eye.y * h))
                right = (int(right_eye.x * w), int(right_eye.y * h))
                angle = calculate_angle(left, right)

                if abs(angle) > TILT_THRESHOLD:
                    if tilt_start_time is None:
                        tilt_start_time = time.time()
                    elapsed = time.time() - tilt_start_time

                    cv2.putText(
                        frame,
                        f"TILT DETECTED ({angle:+.1f}°) [{elapsed:.1f}s]",
                        (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 0, 255),
                        2
                    )

                    if elapsed >= TILT_NOTICE_DELAY and not mini_visible:
                        print("[HeadsUp] Mini alert triggered (early).")
                        if mini_overlay_command_queue:
                            mini_overlay_command_queue.put("show")
                        mini_visible = True

                    if elapsed >= TILT_DURATION and not overlay_visible:
                        print("[HeadsUp] Fullscreen alert triggered (sustained).")
                        overlay_command_queue.put("show")
                        overlay_visible = True
                else:
                    if mini_visible:
                        print("[HeadsUp] Mini overlay cleared.")
                        if mini_overlay_command_queue:
                            mini_overlay_command_queue.put("hide")
                        mini_visible = False

                    if overlay_visible:
                        print("[HeadsUp] Fullscreen overlay cleared.")
                        overlay_command_queue.put("hide")
                        overlay_visible = False

                    tilt_start_time = None
            else:
                if mini_visible:
                    print("[HeadsUp] Face lost - hiding mini overlay.")
                    if mini_overlay_command_queue:
                        mini_overlay_command_queue.put("hide")
                    mini_visible = False

                if overlay_visible:
                    print("[HeadsUp] Face lost - hiding fullscreen overlay.")
                    overlay_command_queue.put("hide")
                    overlay_visible = False

                tilt_start_time = None

            cv2.imshow("HeadsUp Posture Monitor", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("[HeadsUp] Manual quit triggered.")
                is_running_flag["running"] = False
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        overlay_command_queue.put("hide")
        if mini_overlay_command_queue:
            mini_overlay_command_queue.put("hide")
        print("[HeadsUp] Webcam released. Monitoring stopped.")
