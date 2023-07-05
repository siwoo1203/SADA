import cv2 # open CV
import mediapipe as mp # 손가락 인식
from dynamikontrol import Module # 모터 움직임

mp_drawing = mp.solutions.drawing_utils # 손가락 뼈ㅏ미
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0) # 카메라 열기

module = Module()

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        results = hands.process(image) # 전처리된 이미지 대입
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks: # 손 인식되면 true
            for hand_landmarks in results.multi_hand_landmarks:
                thumb = hand_landmarks.landmark[4] # 엄지(4) 위치
                index = hand_landmarks.landmark[8] # 검지(8) 위치

                diff = abs(index.x - thumb.x)
                volume = int(diff * 500)

                module.motor.angle(volume)

                cv2.putText( # 볼륨이 몇인지 텍스트로 표현
                    image, text = 'Volume : %d' % volume, org = (10, 30),
                    fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1,
                    color = 255, thickness = 2)

                mp.drawing.draw_landmarks( # 손가락 뼈마디 그리기
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow('image', image)
        if cv2.waitkey(1) == ord('q'):
            break

    cap.release()
