import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True

def listen(prompt: str = "Listening...") -> str:
    """
    Listens to microphone audio and transcribes it using SpeechRecognition.
    Falls back to console input if microphone hardware or audio driver is missing.
    """
    print(f"\n🎤 {prompt}")
    
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=8)
            
        text = recognizer.recognize_google(audio)
        print(f"You: {text}")
        return text.lower().strip()
        
    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        print("Vyshu: Sorry, I didn't catch that. Could you repeat?")
        return ""
    except sr.RequestError:
        print("Vyshu: Speech recognition service unavailable. Check connection.")
        return ""
    except Exception as e:
        # Fallback for environments without functional mic / PyAudio error
        print(f"[Mic Error: {e}]")
        text = input("You (Type command): ").strip()
        return text.lower()

if __name__ == "__main__":
    test_result = listen("Testing speech module...")
    print(f"Result: {test_result}")
