import speech_recognition as sr
import pyttsx3
import time
from PySide6.QtCore import QThread, Signal

class VoiceThread(QThread):
    # Signals to update the GUI
    log_signal = Signal(str)        # For "Robot: ..." messages
    user_text_signal = Signal(str)  # For "User: ..." input display
    status_signal = Signal(str)     # For "Listening...", "Processing..."
    command_signal = Signal(str)    # For sending final commands (A, B, Z) to Main Window

    def __init__(self):
        super().__init__()
        self._is_running = True
        self.activation_keyword = "hello"
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Format: "SPOKEN WORD" : "COMMAND CODE"
        self.command_map = {
            "PICK": "PICK", "PEAK": "PICK", "GET": "PICK", "TAKE": "PICK",
            "FEED": "FEED","SEND": "FEED", 
            "HOME": "HOME",
            "FINISH": "FINISH", "FINISHED": "FINISH",
            "HEAD": "HEAD", "CAMERA": "HEAD"
        }

        self.confirm_map = {
            "YES": "YES", "YEAH": "YES", "YEP": "YES", "YUP": "YES", "SURE": "YES",
            "NO": "NO", "NOPE": "NO", "NAH": "NO"
        }

        # Initialize TTS
        try:
            self.tts_engine = pyttsx3.init()
            voices = self.tts_engine.getProperty('voices')
            if len(voices) > 1:
                self.tts_engine.setProperty('voice', voices[1].id)
            self.tts_engine.setProperty("rate", 145)
        except Exception as e:
            print(f"TTS Init Error: {e}")
            self.tts_engine = None

    def run(self):
        while self._is_running:
            # STANDBY MODE
            self.update_status("Standby => Say 'Hello'")
            activated = self.wait_for_activation()
            
            if not self._is_running:
                break
            if not activated:
                continue

            # ACTIVE MODE
            self.speak("How can I help you?")
            
            selection = False
            while not selection and self._is_running:
                self.update_status("Listening for Command...")
                
                # Step 1: Listen for selection
                text = self.listen_mic()
                if not text: 
                    continue

                cmd = self.parse_command(text)

                if not cmd:
                    if text: 
                        self.speak("I didn't catch that. Please say again.")
                    continue 

                # Prompt
                if cmd == "PICK":
                    prompt1 = "Are you sure you want to pick up the food?"
                    prompt2 = "Okay, picking up the food..."
                elif cmd == "FEED":
                    prompt1 = "Are you sure you want to bring the food to your mouth?"
                    prompt2 = "Okay, sending the food to you..."
                elif cmd == "HOME":
                    prompt1 = "Are you sure you want the robotic arm to return to the home position?"
                    prompt2 = "Okay, robotic arm returning to home position..."
                elif cmd == "FINISH":
                    prompt1 = "Are you sure you want to finish eating?"
                    prompt2 = "Okay, Stopping voice control system..."
                elif cmd == "HEAD":
                    prompt1 = "Are you sure you want to switch to head control mode?"
                    prompt2 = "Okay, Switching to head control system..."

                # Step 2: Ask Confirmation
                self.speak(prompt1)

                # Step 3: Listen for Confirmation
                self.update_status("Waiting for Confirmation...")
                confirmation_text = self.listen_mic()
                confirmation_answer = self.confirmation(confirmation_text)

                if confirmation_answer == "YES":
                    self.speak(prompt2)
                    self.command_signal.emit(cmd)
                    selection = True # Return to standby
                elif confirmation_answer == "NO":
                    self.speak("Okay, please select again.")
                else:
                    self.speak("I didn't hear Yes or No. Try selecting again.")
                    
        
        # Cleanup
        self.update_status("Voice Control OFF")

    def stop(self):
        self._is_running = False
        self.wait()

    def speak(self, text):
        if not self._is_running: return
        self.log_signal.emit(f"Robot: {text}")
        if self.tts_engine:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()

    def update_status(self, text):
        self.status_signal.emit(text)

    def listen_mic(self):
    
        if not self._is_running: 
            return ""
        
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=7)
                self.status_signal.emit("Processing...")
                text = self.recognizer.recognize_google(audio)
                self.user_text_signal.emit(f"You: {text}")
                return text.strip()
            
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                print("Could not understand audio")
                return ""
            except sr.RequestError as e:
                print(f"API error: {e}")
                return ""

    def wait_for_activation(self):
        while self._is_running:
            text = self.listen_mic()
            if text and self.activation_keyword in text.lower():
                self.speak("Hello!")
                return True
            time.sleep(0.1)
        return False

    def parse_command(self, text):
        if not text: 
            return None
        words = text.upper().split()
        for word in words:
            if word in self.command_map:
                return self.command_map[word]
        return None

    def confirmation(self, text):
        if not text: 
            return None
        words = text.upper().split()
        for word in words:
            if word in self.confirm_map:
                return self.confirm_map[word]
                
        return None