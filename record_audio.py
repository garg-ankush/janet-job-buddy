import sounddevice as sd
from scipy.io.wavfile import write


def record_audio(output_filename, sample_rate=44100, number_of_secs_to_record_for=10):
    print("====Listening====")
    print()
    # Record audio
    recording = sd.rec(
        int(number_of_secs_to_record_for * sample_rate), samplerate=sample_rate, channels=1)
    # Wait for the recording to finish
    sd.wait()

    # Save as WAV file
    write(f'{output_filename}.wav', sample_rate, recording)
