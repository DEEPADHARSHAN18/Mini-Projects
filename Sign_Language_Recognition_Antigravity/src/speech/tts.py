import pyttsx3
import threading

class TTSEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        # Optional: set properties like rate and volume
        self.engine.setProperty('rate', 150)
        
    def _speak_thread(self, text: str):
        """Runs the text-to-speech engine loop in a separate thread."""
        # Initialize a new engine inside the thread because pyttsx3 loops are thread-sensitive on some OS
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()

    def speak(self, text: str):
        """Speaks the given text without blocking the main OpenCV thread."""
        if text.strip():
            thread = threading.Thread(target=self._speak_thread, args=(text,), daemon=True)
            thread.start()
