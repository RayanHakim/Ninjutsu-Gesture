import cv2
import mediapipe as mp
import numpy as np
import time
from pygame import mixer

# --- 1. INISIALISASI AUDIO ---
mixer.init()

def load_sound(file_path):
    try:
        return mixer.Sound(file_path)
    except:
        print(f"⚠️ Warning: File {file_path} tidak ditemukan!")
        return None

sfx_api = load_sound("suara_api.mp3")
sfx_listrik = load_sound("suara_listrik.mp3")
sfx_air = load_sound("suara_air.mp3")
# SEKARANG MENGGUNAKAN FILE MP3 RASENGAN ASLI
sfx_rasengan = load_sound("suara_rasengan.mp3")

# --- 2. LOAD VIDEO ASSETS ---
cap_api = cv2.VideoCapture("video_api.mp4")
cap_listrik = cv2.VideoCapture("video_listrik.mp4")
cap_air = cv2.VideoCapture("video_air.mp4")
cap_rasengan = cv2.VideoCapture("video_rasengan.mp4")

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=0, # Ringan untuk CPU i5
    min_detection_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

pTime = 0

def get_overlay_frame(cap_video):
    ret, frame = cap_video.read()
    if not ret:
        cap_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap_video.read()
    if frame is not None:
        frame = cv2.resize(frame, (300, 300))
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array([35, 100, 100]), np.array([85, 255, 255]))
        mask_inv = cv2.bitwise_not(mask)
        jurus_only = cv2.bitwise_and(frame, frame, mask=mask_inv)
        return jurus_only, mask_inv
    return None, None

# --- 3. MAIN LOOP ---
cap = cv2.VideoCapture(0)
current_jutsu = None
last_action_time = time.time()
window_name = "Ninjutsu Gesture"

print("⚔️ SHINOBI SYSTEM ACTIVE! Rasengan SFX Loaded.")

while True:
    success, img = cap.read()
    if not success: break
    img = cv2.flip(img, 1)
    h_cam, w_cam, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    hand_detected = False

    if results.multi_hand_landmarks:
        hand_detected = True
        for handLms in results.multi_hand_landmarks:
            cx = int(handLms.landmark[9].x * w_cam)
            cy = int(handLms.landmark[9].y * h_cam)

            tips = [8, 12, 16, 20]
            open_f = []
            for tip in tips:
                open_f.append(handLms.landmark[tip].y < handLms.landmark[tip-2].y)
            
            count = open_f.count(True)

            # --- LOGIKA TRIGGER JUTSU ---
            
            # 1. KATON (Kepal)
            if count == 0 and current_jutsu != "API":
                mixer.stop()
                if sfx_api: sfx_api.play(-1)
                current_jutsu = "API"; last_action_time = time.time()
            
            # 2. CHIDORI (4 Jari terbuka tegak)
            elif count == 4 and current_jutsu != "LISTRIK":
                mixer.stop()
                if sfx_listrik: sfx_listrik.play(-1)
                current_jutsu = "LISTRIK"; last_action_time = time.time()
            
            # 3. SUITON (Pose Metal 🤘)
            elif open_f == [True, False, False, True] and current_jutsu != "AIR":
                mixer.stop()
                if sfx_air: sfx_air.play(-1)
                current_jutsu = "AIR"; last_action_time = time.time()

            # 4. RASENGAN (Telunjuk Tegak Saja)
            elif open_f == [True, False, False, False] and current_jutsu != "RASENGAN":
                mixer.stop()
                if sfx_rasengan: sfx_rasengan.play(-1)
                current_jutsu = "RASENGAN"; last_action_time = time.time()

            # --- RENDER JURUS ---
            if current_jutsu:
                sources = {"API": cap_api, "LISTRIK": cap_listrik, "AIR": cap_air, "RASENGAN": cap_rasengan}
                j_frame, m_inv = get_overlay_frame(sources[current_jutsu])
                
                if j_frame is not None:
                    hj, wj, _ = j_frame.shape
                    y1, y2 = max(0, cy-hj//2), min(h_cam, cy+hj//2)
                    x1, x2 = max(0, cx-wj//2), min(w_cam, cx+wj//2)
                    j_crop = j_frame[0:(y2-y1), 0:(x2-x1)]
                    m_crop = m_inv[0:(y2-y1), 0:(x2-x1)]
                    roi = img[y1:y2, x1:x2]
                    bg = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(m_crop))
                    img[y1:y2, x1:x2] = cv2.add(bg, j_crop)

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    if not hand_detected or (time.time() - last_action_time > 5):
        if current_jutsu:
            mixer.stop()
            current_jutsu = None

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
    
    if current_jutsu:
        cv2.putText(img, f'JUTSU: {current_jutsu}', (20, 90), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    cv2.imshow(window_name, img)
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()