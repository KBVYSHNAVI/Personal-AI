from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import datetime
import threading
from voice import speak
from speech import listen
from wake_word import is_wake_word
from commands import execute_command, open_youtube, open_google, open_github, search_youtube, search_google, tell_time, open_vscode

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Track assistant state
assistant_state = {
    "status": "idle",  # idle, listening, speaking, processing
    "last_command": "",
    "last_response": "Hello! I am Vyshu. How can I help you today?",
    "history": [
        {"sender": "vyshu", "text": "Hello! I am Vyshu, your personal AI assistant.", "timestamp": datetime.datetime.now().strftime("%I:%M %p")}
    ]
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status", methods=["GET"])
def get_status():
    return jsonify({
        "state": assistant_state["status"],
        "last_response": assistant_state["last_response"],
        "history": assistant_state["history"],
        "time": datetime.datetime.now().strftime("%I:%M %p")
    })

@app.route("/api/command", methods=["POST"])
def process_command():
    data = request.json or {}
    user_text = data.get("command", "").strip()
    
    if not user_text:
        return jsonify({"status": "error", "message": "No command provided"}), 400
        
    timestamp = datetime.datetime.now().strftime("%I:%M %p")
    
    # Log user command
    assistant_state["history"].append({"sender": "user", "text": user_text, "timestamp": timestamp})
    assistant_state["last_command"] = user_text
    assistant_state["status"] = "processing"
    
    # Check if wake word or direct command
    cmd_to_run = user_text
    if is_wake_word(user_text):
        # Remove wake word from actual command text if present
        for kw in ["hey vyshu", "hi vyshu", "hello vyshu", "vyshu"]:
            cmd_to_run = cmd_to_run.replace(kw, "").strip()
            
    if not cmd_to_run:
        response_text = "Yes, I'm listening!"
    else:
        # Determine response & action
        cmd_lower = cmd_to_run.lower()
        if "open youtube" in cmd_lower:
            response_text = "Opening YouTube."
            open_youtube()
        elif "search youtube" in cmd_lower:
            q = cmd_lower.replace("search youtube for", "").replace("search youtube", "").strip()
            response_text = f"Searching YouTube for {q}."
            search_youtube(q)
        elif "open google" in cmd_lower:
            response_text = "Opening Google."
            open_google()
        elif "search google" in cmd_lower or "search for" in cmd_lower:
            q = cmd_lower.replace("search google for", "").replace("search google", "").replace("search for", "").strip()
            response_text = f"Searching Google for {q}."
            search_google(q)
        elif "open github" in cmd_lower:
            response_text = "Opening GitHub."
            open_github()
        elif "open vs code" in cmd_lower or "open vscode" in cmd_lower:
            response_text = "Opening VS Code."
            open_vscode()
        elif "time" in cmd_lower:
            now_str = datetime.datetime.now().strftime("%I:%M %p")
            response_text = f"The current time is {now_str}."
        else:
            response_text = f"Executed: {cmd_to_run}"
            
    # Speak response asynchronously to avoid blocking API
    threading.Thread(target=speak, args=(response_text,), daemon=True).start()
    
    assistant_state["last_response"] = response_text
    assistant_state["status"] = "idle"
    assistant_state["history"].append({"sender": "vyshu", "text": response_text, "timestamp": timestamp})
    
    return jsonify({
        "status": "success",
        "command": user_text,
        "response": response_text,
        "history": assistant_state["history"]
    })

@app.route("/api/listen", methods=["POST"])
def listen_backend():
    """Trigger microphone listening on backend python speech engine"""
    assistant_state["status"] = "listening"
    text = listen(prompt="Listening via Web Dashboard...")
    assistant_state["status"] = "idle"
    
    if text:
        return jsonify({"status": "success", "text": text})
    else:
        return jsonify({"status": "empty", "text": ""})

if __name__ == "__main__":
    print("\n==================================================")
    print("      VYSHU AI Web Dashboard Server Running     ")
    print("      Access at: http://127.0.0.1:5000           ")
    print("==================================================\n")
    app.run(host="127.0.0.1", port=5000, debug=False)

