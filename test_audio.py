import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os

def test_recording():
    fs = 44100  # Sample rate
    seconds = 3  # Duration of recording
    
    print("Recording 3 seconds of audio in 1 second...")
    sd.sleep(1000)
    print("GO!")
    
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    print("Finished recording.")
    
    filename = "test_output.wav"
    wav.write(filename, fs, myrecording)
    
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        print(f"File created: {filename}, size: {size} bytes")
        if size > 1000:
            print("Audio recording TEST PASSED (file is non-empty).")
        else:
            print("Audio recording TEST FAILED (file is too small).")
    else:
        print("Audio recording TEST FAILED (file not created).")

if __name__ == "__main__":
    try:
        test_recording()
    except Exception as e:
        print(f"Audio recording TEST FAILED with exception: {e}")
