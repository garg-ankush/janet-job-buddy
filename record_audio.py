import sounddevice as sd
from scipy.io.wavfile import write

# Choose your recording parameters
fs = 44100  # Sample rate
seconds = 10  # Duration of recording


def record_audio(number_of_secs_to_record_for=10):
    # Record audio
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    # Wait for the recording to finish
    sd.wait()

    # Save as WAV file
    write('output.wav', fs, recording)
