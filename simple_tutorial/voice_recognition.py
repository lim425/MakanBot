import pyttsx3
import speech_recognition as sr
import time

class SpeechRecognizer:
    def __init__(self, timeout=5, letters=None):
        # Initialize speech recognizer and microphone
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        if letters is None:
            self.letters = {"A","B","C","D","E","F","G","H","I","NEXT","FINISH"}
        else:
            self.letters = letters

        self.confirmations = {"YES", "NO"}

        # Initialize TTS
        self.tts_engine = pyttsx3.init()
        voices = self.tts_engine.getProperty('voices')
        # Attempt to set a clearer voice if available
        if len(voices) > 1:
            self.tts_engine.setProperty('voice', voices[1].id)
        self.tts_engine.setProperty("rate", 145) # Slightly faster for better flow

        self.timeout = timeout

    def listen(self):
        """
        Uses listen() instead of record(). 
        It waits for speech, then automatically stops recording when silence is detected.
        """
        print("Listening...")
        
        with self.microphone as source:
            # Adjust for noise briefly before listening
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                # 'timeout' is how long it waits for sound to start
                # 'phrase_time_limit' prevents it from hanging if background noise is high
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                print("Processing audio...")
                
                text = self.recognizer.recognize_google(audio)
                print(f"🗣️ You said: {text}")
                return text.strip()
            
            except sr.WaitTimeoutError:
                print("No speech detected (Timeout)")
                return ""
            except sr.UnknownValueError:
                print("Could not understand audio")
                return ""
            except sr.RequestError as e:
                print(f"API error: {e}")
                return ""

    def speak(self, text):
        print(f"🤖 Robot: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def parse_command(self, text):
        words = text.upper().split()
        detected_letter = next((word for word in words if word in self.letters), None)

        if detected_letter == "NEXT":
            return "X"
        elif detected_letter == "FINISH":
            return "Z"
        elif detected_letter:
            return detected_letter
        else:
            return None
        
    def confirmation(self, text):
        words = text.upper().split()
        detected_letter = next((word for word in words if word in self.confirmations), None)
        return detected_letter if detected_letter else None

    def wait_for_activation(self):
        """
        Loops indefinitely until the user says 'HELLO'.
        """
        print("\n=== STANDBY MODE: Say 'Hello' to activate ===")
        while True:
            text = self.listen()
            if text and "hello" in text.lower():
                self.speak("Hello! System activated.")
                return True
            # If not hello, we just loop back and listen again silently
            time.sleep(0.5)

if __name__ == "__main__":
    recognizer = SpeechRecognizer(timeout=5)
    
    # MAIN PROGRAM LOOP
    while True:
        # 1. Wait for the Wake Word
        recognizer.wait_for_activation()

        # 2. Once activated, enter the Food Selection Loop
        recognizer.speak("Please choose a food letter: A to I. Say Next or End.")
        
        food_selected = False
        
        while not food_selected:
            # Step 2: Listen for selection
            text = recognizer.listen()
            cmd = recognizer.parse_command(text)

            if not cmd:
                recognizer.speak("I didn't catch that. Please say a letter, Next, or Finish.")
                continue 

            # Step 3: Ask for confirmation
            if cmd == "X":
                confirm_prompt = "Are you sure you want to select Next?"
            elif cmd == "Z":
                confirm_prompt = "Are you sure you want to Finish?"
            else:
                confirm_prompt = f"Are you sure you want to select {cmd}?"
            
            recognizer.speak(confirm_prompt)

            # Step 4: Listen for confirmation
            confirmation_arg = recognizer.listen()
            confirmation_answer = recognizer.confirmation(confirmation_arg)

            if confirmation_answer == "YES":
                recognizer.speak(f"Confirmed. You selected {cmd}.")
                food_selected = True # Break the inner loop to go back to standby
            elif confirmation_answer == "NO":
                recognizer.speak("Okay, please select again.")
            else:
                recognizer.speak("I didn't hear Yes or No. Let's try selecting again.")
        
        time.sleep(1)