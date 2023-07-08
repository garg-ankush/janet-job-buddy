import os
import shlex


def speak(text):
    text = shlex.quote(text)
    os.system(f'say {text}')

