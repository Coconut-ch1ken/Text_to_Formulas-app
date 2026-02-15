import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def transcribe_and_translate(self, audio_path):
        """
        Transcribes audio and translates it to LaTeX using Gemini.
        """
        prompt = """
        You are a helpful assistant that converts spoken math into LaTeX.
        Listen to the audio and output ONLY the LaTeX code for the formula described.
        Do not include any markdown formatting (like ```latex or ```), just the raw LaTeX string.
        For example, if the audio says "e to the power of x squared", you should output: e^{x^2}
        """

        try:
            # Upload the file to Gemini
            audio_file = genai.upload_file(path=audio_path)
            
            # Generate content
            response = self.model.generate_content([prompt, audio_file])
            
            # Text cleaning (just in case)
            result = response.text.strip()
            if result.startswith("```latex"):
                result = result[8:]
            if result.startswith("```"):
                result = result[3:]
            if result.endswith("```"):
                result = result[:-3]
                
            return result.strip()
        except Exception as e:
            print(f"Error in LLM processing: {e}")
            return None
