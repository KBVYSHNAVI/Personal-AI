import sys
from voice import speak
from speech import listen
from wake_word import is_wake_word
from commands import execute_command

def main():
    print("========================================")
    print("               VYSHU AI                ")
    print("         Personal AI Assistant         ")
    print("========================================")
    
    speak("Hello! I am Vyshu, your personal AI assistant.")
    print("Tip: Say 'Hey Vyshu' to activate me, or type your command.\n")
    
    running = True
    
    while running:
        # Continuous wake word listening
        heard_text = listen(prompt="Listening for wake word ('Hey Vyshu')...")
        
        if is_wake_word(heard_text):
            speak("Yes, I'm listening.")
            
            # Listen for user command
            command = listen(prompt="State your command (e.g. 'Open YouTube')...")
            
            if command:
                running = execute_command(command)
            else:
                speak("I didn't hear a command.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nVYSHU AI session ended. Goodbye!")
        sys.exit(0)
