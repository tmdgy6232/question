## test

import beepy
from question import kakao_utils
import key


# 컴퓨터에 내장된 소리를 출력
def beepsound():
    beepy.beep(sound=6)

# 카카오톡 메시지로 '졸음 방지 베타파' 영상 링크를 전송
def send_music_link():
    KAKAO_TOKEN_FILENAME = "kakao_token.json"  # "<kakao_token.json 파일이 있는 경로를 입력하세요.>"
    KAKAO_APP_KEY = key.REST_API_KEY
    tokens = kakao_utils.update_tokens(KAKAO_APP_KEY, KAKAO_TOKEN_FILENAME)

    # 텍스트 메시지 보내기
    template = {
        "object_type": "text",
        "text": "당신은 30초 이상 졸았습니다. 졸지 마세요!!!!",
        "link": {
            "web_url": "https://www.youtube.com/watch?v=7Q2N7919o5o",
            "mobile_web_url": "https://www.youtube.com/watch?v=7Q2N7919o5o"
        },
        "button_title": "잠깨는 노래 듣기"
    }

    # 카카오 메시지 전송
    res = kakao_utils.send_message(KAKAO_TOKEN_FILENAME, template)
    if res.json().get('result_code') == 0:
        print('텍스트 메시지를 성공적으로 보냈습니다.')
    else:
        print('텍스트 메시지를 보내지 못했습니다. 오류메시지 : ', res.json())
