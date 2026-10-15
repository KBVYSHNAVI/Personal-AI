import webbrowser
import datetime
import subprocess
import os
from voice import speak

def open_youtube():
    speak("Opening YouTube.")
    webbrowser.open("https://www.youtube.com")

def open_google():
    speak("Opening Google.")
    webbrowser.open("https://www.google.com")

def open_github():
    speak("Opening GitHub.")
    webbrowser.open("https://github.com")

def search_youtube(query: str):
    speak(f"Searching YouTube for {query}.")
    search_url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(search_url)

def search_google(query: str):
    speak(f"Searching Google for {query}.")
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)

def tell_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    speak(f"The current time is {current_time}.")

def open_vscode():
    speak("Opening Visual Studio Code.")
    try:
        subprocess.Popen(["code"])
    except Exception:
        speak("Could not launch VS Code executable directly. Opening project folder instead.")
        os.startfile("D:\\code files\\VYSHU_AI")

def execute_command(command: str) -> bool:
    """
    Executes the command based on detected intent.
    Returns True if assistant should continue running, False if user asked to stop/exit.
    """
    cmd = command.lower().strip()
    
    if not cmd:
        return True
        
    if "exit" in cmd or "stop" in cmd or "quit" in cmd or "bye" in cmd:
        speak("Goodbye! Have a great day.")
        return False
        
    if "open youtube" in cmd:
        open_youtube()
    elif "search youtube for" in cmd or "search youtube" in cmd:
        query = cmd.replace("search youtube for", "").replace("search youtube", "").strip()
        if query:
            search_youtube(query)
        else:
            open_youtube()
    elif "open google" in cmd:
        open_google()
    elif "search google for" in cmd or "search google" in cmd or "search for" in cmd:
        query = cmd.replace("search google for", "").replace("search google", "").replace("search for", "").strip()
        if query:
            search_google(query)
        else:
            open_google()
    elif "open github" in cmd:
        open_github()
    elif "open vs code" in cmd or "open vscode" in cmd or "open code" in cmd:
        open_vscode()
    elif "time" in cmd or "what time" in cmd:
        tell_time()
    else:
        speak(f"I heard: '{command}'. I am still learning new commands!")
        
    return True

if __name__ == "__main__":
    print("Testing command execution...")
    tell_time()
