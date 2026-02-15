import os
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import threading

class AudioRecorder:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.recording = False
        self.audio_data = []
        self.thread = None

    def start_recording(self):
        if self.recording:
            return
        self.recording = True
        self.audio_data = []
        self.thread = threading.Thread(target=self._record)
        self.thread.start()
        print("Recording started...")

    def _record(self):
        def callback(indata, frames, time, status):
            if status:
                print(status)
            if self.recording:
                self.audio_data.append(indata.copy())
            else:
                raise sd.CallbackStop

        with sd.InputStream(samplerate=self.sample_rate, channels=1, callback=callback):
            while self.recording:
                sd.sleep(100)

    def stop_recording(self):
        if not self.recording:
            return None
        self.recording = False
        self.thread.join()
        print("Recording stopped.")
        return self._save_to_temp_file()

    def _save_to_temp_file(self):
        if not self.audio_data:
            return None
        
        # Concatenate all audio chunks
        recording = np.concatenate(self.audio_data, axis=0)
        
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        wav.write(temp_file.name, self.sample_rate, recording)
        return temp_file.name
