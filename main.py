import os
import time
import threading
from pynput import keyboard
from audio_recorder import AudioRecorder
from llm_client import LLMClient
from dotenv import load_dotenv
import pyautogui

# Load environment variables
load_dotenv()

class TextToFormulaApp:
    def __init__(self):
        self.recorder = AudioRecorder()
        try:
            self.llm_client = LLMClient()
        except ValueError as e:
            print(f"Error: {e}")
            print("Please set GOOGLE_API_KEY in .env file")
            self.llm_client = None

        self.is_recording = False
        self.check_api_key()

    def check_api_key(self):
        if not os.getenv("GOOGLE_API_KEY"):
            print("WARNING: GOOGLE_API_KEY is not set. The app will not function correctly.")

    def on_activate(self):
        if not self.llm_client:
             print("LLM Client not initialized. Check API Key.")
             return

        if not self.is_recording:
            print("Global hotkey activated! Starting recording...")
            self.is_recording = True
            self.recorder.start_recording()
            # Optional: Play a sound here to indicate start
        else:
            print("Stopping recording...")
            self.is_recording = False
            audio_path = self.recorder.stop_recording()
            
            if audio_path:
                print(f"Audio saved to {audio_path}. Processing...")
                self.process_audio(audio_path)
            
    def process_audio(self, audio_path):
        # Run in a separate thread to not block the listener
        threading.Thread(target=self._process_audio_thread, args=(audio_path,)).start()

    def _process_audio_thread(self, audio_path):
        latex_code = self.llm_client.transcribe_and_translate(audio_path)
        if latex_code:
            print(f"Generated LaTeX: {latex_code}")
            self.type_out(latex_code)
        else:
            print("Failed to generate LaTeX.")
        
        # Cleanup temp file
        try:
            os.remove(audio_path)
        except OSError:
            pass

    def type_out(self, text):
        # Type the text into the active window
        # We might need to give focus back to the previous window if we lost it, 
        # but since we are running as a background script/terminal, user focus should be on their editor.
        try:
            pyautogui.write(text)
        except Exception as e:
            print(f"Error typing text: {e}")

    def run(self):
        # predefined hotkey: Cmd+Option+L
        # Note: On Mac 'cmd' is often '<cmd>' or 'cmd_l'/'cmd_r'. 
        # pynput format: '<cmd>+<alt>+l'
        hotkey = '<cmd>+<alt>+l'
        
        print(f"Listening for hotkey: {hotkey}")
        print("Press the hotkey to START recording, and press it again to STOP recording.")
        
        with keyboard.GlobalHotKeys({
                hotkey: self.on_activate}) as h:
            h.join()

if __name__ == "__main__":
    app = TextToFormulaApp()
    app.run()
