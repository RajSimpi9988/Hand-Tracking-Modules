from sre_constants import SUCCESS
import cv2
import mediapipe as mp
import time
import pyautogui

cap = cv2.VideoCapture(0)
cap.isOpened()

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(cx, cy)
                if id == 0:
                    # Move the cursor using the index finger
                    pyautogui.moveTo(cx, cy)

                if id == 4:  # Thumb
                    thumb_x, thumb_y = int(lm.x * w), int(lm.y * h)

            # Calculate the distance between index finger and thumb
            distance = ((cx - thumb_x) ** 2 + (cy - thumb_y) ** 2) ** 0.5

            # Execute click operation when distance is less than 100
            if distance < 100:
                pyautogui.click()

            # Execute double click operation when distance is less than 50
            if distance < 50:
                pyautogui.doubleClick()

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
