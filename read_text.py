import os
import shlex


def speak(text, timestamp):
    text = shlex.quote(text)
    os.system(f'say {text}')
    #
    # requests.post(
    #     url="https://j9igwbu9j7.execute-api.us-east-1.amazonaws.com/DEV/textToSpeech",
    #     json={
    #         "text": text,
    #         "textId": timestamp,
    #         "voiceId": "Joanna"
    #     })
    #
    # time.sleep(15)
    #
    # audio_source = os.getenv("AUDIO_SOURCE")
    # filepath = f"{audio_source}/{timestamp}"
    #
    # # for playing note.wav file
    # print(filepath)
    # playsound(filepath)
    # print('playing sound using playsound')
    # return

