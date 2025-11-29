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
            "A": "A", "HEY": "A", "AY": "A",
            "B": "B", "BEE": "B", "BE": "B", "BI": "B",
            "C": "C", "SEE": "C", "SEA": "C", "SI": "C",
            "D": "D", "DEE": "D", "THE": "D",
            "E": "E",
            "F": "F",
            "G": "G", "GEE": "G", "JI": "G",
            "H": "H",
            "J": "J", "JAY": "J",
            "NEXT": "NEXT",
            "HOME": "HOME",
            "FINISH": "FINISH", "FINISHED": "FINISH"
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
            self.speak("Please select a food letter, or Next or Finish.")
            
            food_selected = False
            while not food_selected and self._is_running:
                self.update_status("Listening for Command...")
                
                # Step 1: Listen for selection
                text = self.listen_mic()
                if not text: 
                    continue

                cmd = self.parse_command(text)

                if not cmd:
                    if text: 
                        self.speak("I didn't catch that. Please say a letter.")
                    continue 

                # Step 2: Ask Confirmation
                prompt = f"Are you sure you want to select {cmd}?"
                self.speak(prompt)

                # Step 3: Listen for Confirmation
                self.update_status("Waiting for Confirmation...")
                confirmation_text = self.listen_mic()
                confirmation_answer = self.confirmation(confirmation_text)

                if confirmation_answer == "YES":
                    self.speak(f"Confirmed. You selected {cmd}.")
                    self.command_signal.emit(cmd)
                    food_selected = True # Return to standby
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