import pyttsx3

# Initialize TTS Engine
try:
    engine = pyttsx3.init()
    # Configure speech rate (words per minute)
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1.0)
    
    # Try selecting a natural female voice if available on Windows (e.g. Zira)
    voices = engine.getProperty('voices')
    for voice in voices:
        if "zira" in voice.name.lower() or "female" in voice.name.lower() or "hazel" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
except Exception as e:
    engine = None
    print(f"[Warning] TTS initialization error: {e}")

def speak(text: str):
    """
    Prints Vyshu's response to the terminal and speaks it aloud.
    """
    print(f"\nVyshu: {text}")
    if engine:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"[TTS Output Error]: {e}")

if __name__ == "__main__":
    speak("Hello! Voice module initialized successfully.")
