import cv2
import mediapipe as mp
import autopy
import math
mp_drawing_util = mp.solutions.drawing_utils
mp_drawing_style = mp.solutions.drawing_styles

mp_hand = mp.solutions.hands
hands = mp_hand.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
def khoangCach(a, b):
    x1, y1 = a[0], a[1]
    x2, y2 = b[0], b[1]
    return math.hypot(x2 - x1, y2 - y1)
wScr, hScr = autopy.screen.size()   # lấy cdai, ccao của screen
#wCam, hCam = 640, 480 # khai báo màn hình của mình dùng

cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, img = cap.read()
    if not success:
        break
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    if result.multi_hand_landmarks:
        for idx, hand in enumerate(result.multi_hand_landmarks):
            # mp_drawing_util.draw_landmarks(
            #     img,
            #     hand,
            #     mp_hand.HAND_CONNECTIONS,
            #     mp_drawing_style.get_default_hand_landmarks_style(),
            #     mp_drawing_style.get_default_hand_connections_style()
            # )

            mp_drawing_util.draw_landmarks(img, hand, mp_hand.HAND_CONNECTIONS)

            #lbl = result.multi_handedness[idx].classification[0].label # nếu muốn dùng tay trái
            #if lbl == "Left":
            myHand = []  # tọa độ bàn tay
            h, w, _ = img.shape
            for id, lm in enumerate(hand.landmark):
                myHand.append([int(lm.x * w),int(lm.y * h)])
            xMouse = (wScr / w) * myHand[8][0] # tịnh tiến tọa độ chuột di chuyển dc ra ngoài màn hình
            yMouse = (hScr / h) * myHand[8][1]
            autopy.mouse.move(xMouse, yMouse) # di chuyển chuột

            kcChuan = khoangCach(myHand[6], myHand[5])
            lClick = khoangCach(myHand[3], myHand[5])
            rClick = khoangCach(myHand[4], myHand[3])
             # bấm chuột trái
            if lClick < kcChuan:
                autopy.mouse.click(autopy.mouse.Button.LEFT)
            if rClick < kcChuan/2 :
                autopy.mouse.click(autopy.mouse.Button.RIGHT)

    cv2.imshow("Nhan dang ban tay", img)
    #if key == 27:
        #break
    if cv2.waitKey(1) == 27:
        cap.release()
        break
#cap.release()