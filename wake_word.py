def is_wake_word(text: str) -> bool:
    """
    Checks if the given text contains any variation of the wake word 'Hey Vyshu'.
    """
    if not text:
        return False
        
    wake_words = [
        "hey vyshu",
        "hey vishu",
        "hi vyshu",
        "hello vyshu",
        "hey wishu",
        "hi vishu",
        "vyshu",
        "vishu"
    ]
    
    clean_text = text.lower().strip()
    
    for word in wake_words:
        if word in clean_text:
            return True
            
    return False

if __name__ == "__main__":
    # Test wake word detection logic
    assert is_wake_word("hey vyshu") == True
    assert is_wake_word("hello vishu open website") == True
    assert is_wake_word("open youtube") == False
    print("Wake word tests passed successfully!")
