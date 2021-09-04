import cv2
import tensorflow.keras
import numpy as np
from kakao import beepsound, send_music_link, send_question_text


## 이미지 전처리
def preprocessing(frame):
    # 사이즈 조정
    size = (224, 224)
    frame_resized = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)

    # 이미지 정규화
    frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1

    # 이미지 차원 재조정 - 예측을 위해 reshape 해줍니다.
    frame_reshaped = frame_normalized.reshape((1, 224, 224, 3))

    return frame_reshaped


## 학습된 모델 불러오기
model_filename = 'keras_model.h5'
model = tensorflow.keras.models.load_model(model_filename)

# 카메라 캡쳐 객체, 0=내장 카메라
capture = cv2.VideoCapture(0)

# 캡쳐 프레임 사이즈 조절
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


sleep_cnt = 1  # 30초간 "졸림" 상태를 확인하기 위한 변수

while True:
    ret, frame = capture.read()
    if ret == True:
        print("read success!")

    # 이미지 뒤집기
    frame_fliped = cv2.flip(frame, 1)

    # 이미지 출력
    cv2.imshow("VideoFrame", frame_fliped)

    # 1초마다 검사하며, videoframe 창으로 아무 키나 누르게 되면 종료
    if cv2.waitKey(200) > 0:
        break

    # 데이터 전처리
    preprocessed = preprocessing(frame_fliped)

    # 예측
    prediction = model.predict(preprocessed)
    print(np.round(prediction, 3))

    if prediction[0, 1] >= np.mean(prediction[0]):
        print('졸림 상태')
        sleep_cnt += 1

        # 졸린 상태가 30초간 지속되면 소리 & 카카오톡 보내기
        if sleep_cnt % 30 == 0:
            sleep_cnt = 1
            print('30초간 졸고 있네요!!!')
            beepsound()
            send_music_link()
            break

    elif prediction[0, 0] >= np.mean(prediction[0]):
        print('깨어있는 상태')
        sleep_cnt = 1

    elif prediction[0, 2] >= np.mean(prediction[0]):
        print('질문이 있어요!')
        beepsound()
        send_question_text()
        break

# 카메라 객체 반환
capture.release()
# 화면에 나타난 윈도우들을 종료
cv2.destroyAllWindows()