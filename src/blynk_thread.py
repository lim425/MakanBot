import BlynkLib
import time
from PySide6.QtCore import QThread

BLYNK_AUTH = 'amRyqJKCO32nzM6R_fQH3_REmwJBbpqC'

class BlynkThread(QThread):
    def __init__(self):
        super().__init__()
        self.blynk = BlynkLib.Blynk(BLYNK_AUTH, server='blynk.cloud', port=80)
        self._is_running = True
        self.update_live_cycle(0)
        self.update_live_time("0 minutes")
        self.blynk.virtual_write(1, 1)

    def run(self):
        print("Blynk: Service Started...")
        while self._is_running:
            # Keeps the connection alive
            self.blynk.run()
            time.sleep(0.05) 

    # --- UPLOAD FUNCTIONS ---

    def update_mode(self, mode_index):
        # V0: Control Mode
        # 0 = Manual, 1 = Head, 2 = Voice
        self.blynk.virtual_write(0, mode_index)

    def update_action(self, action_index):
        # V1: Current Action
        # 1 = Home, 2 = Pick Food, 4 = Feed, 8 = Finish
        self.blynk.virtual_write(1, action_index)

    def update_live_cycle(self, count):
        # V2: Live Cycle Count
        self.blynk.virtual_write(2, count)

    def update_live_time(self, time_str):
        # V3: Live Time Taken
        self.blynk.virtual_write(3, time_str)

    def log_feeding_summary(self, total_time, total_cycles):
        # Triggers the 'feeding_log' Event.
        msg = f"Total Time Taken: {total_time}\nTotal Cycle: {total_cycles}"
        self.blynk.log_event("feeding_log", msg)

    def stop(self):
        self._is_running = False
        self.wait()