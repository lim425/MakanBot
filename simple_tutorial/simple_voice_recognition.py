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

        # Initialize TTS (Text-to-Speech)
        self.tts_engine = pyttsx3.init()
        voices = self.tts_engine.getProperty('voices')
        if len(voices) > 1:
            self.tts_engine.setProperty('voice', voices[1].id)
        self.tts_engine.setProperty("rate", 115)

        self.timeout = timeout

    def listen(self):
            
        print("Listening for speech...")
        with self.microphone as source:
            print("Calibrating for ambient noise...")
            start_calib = time.time()
            self.recognizer.adjust_for_ambient_noise(source)
            end_calib = time.time()
            print(f"Calibration done in {end_calib - start_calib:.2f} seconds.")

            print(f"Start recording for {self.timeout} sec...")
            start_record = time.time()
            audio = self.recognizer.record(source, duration=self.timeout)
            end_record = time.time()
            print(f"Recording stopped after {end_record - start_record:.2f} seconds.")

        try:
            text = self.recognizer.recognize_google(audio)
            # print(f"🗣️ Recognized: {text}")
            return text.strip()
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return ""
        except sr.RequestError as e:
            print(f"API error: {e}")
            return ""

    def speak(self, text):
        print(f"Robot: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
        time.sleep(0.5)

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

        if detected_letter:
            return detected_letter
        else:
            return None

if __name__ == "__main__":
    recognizer = SpeechRecognizer(timeout=5, letters={"A","B","C","D","E","F","G","H","I","NEXT","FINISH"})
    
    # Step 1: Ask user to choose food
    recognizer.speak("Please choose a food letter: A to I. Say Next or End.")
    print("wating for 5 seconds .......")
    time.sleep(5)
    while True:

        # Step 2: Listen for selection
        text = recognizer.listen()
        print("recognized text:", text)
        cmd = recognizer.parse_command(text)

        if not cmd:
            recognizer.speak("I did not understand. Please say again.")
            time.sleep(2)
            continue 
        print("recognized cmd:", cmd)

        # Step 3: Ask for confirmation
        if cmd == "X":
            confirm_prompt = "Are you sure to select Next?"
        elif cmd == "Z":
            confirm_prompt = "Are you sure to select Finish?"
        else:
            confirm_prompt = f"Are you sure to select {cmd}?"
        recognizer.speak(confirm_prompt)
        time.sleep(1)

        # Step 4: Listen for confirmation
        confirmation_arg = recognizer.listen()
        print("Confirmation heard:", confirmation_arg)
        confirmation_answer = recognizer.confirmation(confirmation_arg)
        print("Confirmation asnwer:", confirmation_answer)

        if confirmation_answer == "YES":
            recognizer.speak(f"you select {cmd}")
            time.sleep(2)
            break
        else:
            recognizer.speak(f"please select again buddy")
            time.sleep(2)

