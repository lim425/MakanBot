import cv2
import time

class GUI():

    def __init__(self, frame_width=1280, frame_height=720):
        # Scale
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scale_x = self.frame_width / 1280
        self.scale_y = self.frame_height / 720
        self.scale = (self.scale_x + self.scale_y) / 2

    def guiPosition(self, offset1=20, offset2=50, offset3=150, offset4=30, offset5=30, offset6=50, offset7=150, offset8=280, offset9=30, offset10=40, offset11=20):

        offset1 = offset1 * self.scale_y    # distance between gui box and the promt display
        offset2 = offset2 * self.scale_y    # distance between promt display and finish button
        offset3 = offset3 * self.scale_y   # height of the function button
        offset4 = offset4 * self.scale_x    # width of the function button
        offset5 = offset5 * self.scale_x     # distance horizontal between each function button
        offset6 = offset6 * self.scale_y    # distance between function button and action button
        offset7 = offset7 * self.scale_y    # height of the action button
        offset8 = offset8 * self.scale_x  # width of the action button
        offset9 = offset9 * self.scale_x    # distance horizontal between each action button
        offset10 = offset10 * self.scale_y    # height of the progress bar
        offset11 = offset11 * self.scale_y    # distance between bottom frame and the bottom of progress bar
        
        # Position boundaries
        self.gui_box = (self.frame_width//2, 0, self.frame_width, self.frame_height)
        self.prompt_display = (self.gui_box[0]+offset1, offset1, self.gui_box[2]-offset1, self.gui_box[3]//4)
        self.home_button = (self.prompt_display[0], (self.prompt_display[3])+offset2, (((self.prompt_display[2]-self.prompt_display[0])//4)+offset4)+self.prompt_display[0], (self.prompt_display[3])+offset3)
        self.finish_button = (self.home_button[2]+offset5, (self.prompt_display[3])+offset2, (((self.prompt_display[2]-self.prompt_display[0])//4)+offset4)+self.home_button[2]+offset5, (self.prompt_display[3])+offset3)
        self.voice_button = (self.finish_button[2]+offset5, (self.prompt_display[3])+offset2, (((self.prompt_display[2]-self.prompt_display[0])//4)+offset4)+self.finish_button[2]+offset5, (self.prompt_display[3])+offset3)
        self.button_pick = (self.home_button[0], self.home_button[3]+offset6, self.home_button[0]+offset8, self.home_button[3]+offset6+offset7)
        self.button_feed = (self.button_pick[2]+offset9, self.button_pick[1], self.button_pick[2]+offset9+offset8, self.button_pick[3])
        self.progress_bar = (self.prompt_display[0], self.frame_height-offset11, self.prompt_display[2], self.frame_height-offset11-offset10)
        gui_position_boundaries = [self.gui_box, self.prompt_display, self.home_button , self.finish_button, self.voice_button, self.button_pick, self.button_feed, self.progress_bar]
        return gui_position_boundaries


    def guiDisplay(self, img):
        # GUI
        cv2.rectangle(img, (self.gui_box[0], self.gui_box[1]), (self.gui_box[2], self.gui_box[3]), (212, 61, 104), -1)
        # Prompt Display
        cv2.rectangle(img, (int(self.prompt_display[0]), int(self.prompt_display[1])), (int(self.prompt_display[2]), int(self.prompt_display[3])), (61, 212, 207), -1)
        # Function button
        cv2.rectangle(img, (int(self.home_button[0]), int(self.home_button[1])), (int(self.home_button[2]), int(self.home_button[3])), (104, 212, 61), -1)
        cv2.rectangle(img, (int(self.finish_button[0]), int(self.finish_button[1])), (int(self.finish_button[2]), int(self.finish_button[3])), (61, 61, 212), -1)
        cv2.rectangle(img, (int(self.voice_button[0]), int(self.voice_button[1])), (int(self.voice_button[2]), int(self.voice_button[3])), (80, 164, 247), -1)
        # Progress Bar
        cv2.rectangle(img, (int(self.progress_bar[0]), int(self.progress_bar[1])), (int(self.progress_bar[2]), int(self.progress_bar[3])), (70, 62, 57), -1)
        # Action Buttons
        cv2.rectangle(img, (int(self.button_pick[0]), int(self.button_pick[1])), (int(self.button_pick[2]), int(self.button_pick[3])), (196, 186, 173), -1)
        cv2.rectangle(img, (int(self.button_feed[0]), int(self.button_feed[1])), (int(self.button_feed[2]), int(self.button_feed[3])), (196, 186, 173), -1)


        self.drawTextCenter(img, "HOME", self.home_button)
        self.drawTextCenter(img, "FINISH", self.finish_button)
        self.drawTextCenter(img, "VOICE", self.voice_button)
        self.drawTextCenter(img, "PICK FOOD", self.button_pick)
        self.drawTextCenter(img, "FEED TO MOUTH", self.button_feed)
        
    def drawTextCenter(self, img, text, box, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, color=(72, 52, 33), thickness=3):
        font_scale_ = max(1, int(font_scale* self.scale))
        thickness_ = max(3, int(thickness * self.scale))
        (x1, y1, x2, y2) = box
        text_size = cv2.getTextSize(text, font, font_scale_, thickness_)[0]
        text_x = x1 + (x2 - x1 - text_size[0]) / 2
        text_y = y1 + (y2 - y1 + text_size[1]) / 2
        cv2.putText(img, text, (int(text_x), int(text_y)), font, font_scale_, color, thickness_)

    def fpsDisplay(self, img, fps, box=(20,70), font=cv2.FONT_HERSHEY_PLAIN, font_scale=3, color=(72, 52, 33), thickness=3):
        x, y = box
        cv2.putText(img, f'FPS: {int(fps)}', (x, int(y*self.scale_y)), font, int(font_scale*self.scale), color, int(thickness*self.scale))


def main():
    cap = cv2.VideoCapture(0)
    frame_width  = 1280
    frame_height = 720
    prev_fps_time = 0
    new_fps_time = 0

    gui = GUI(frame_width, frame_height)

    while True:
        success, img = cap.read()
        if not success:
            print("End of video or failed read")               
            break

        img = cv2.resize(img, (frame_width, frame_height))
        
        # ----------------------- GUI display ----------------------------
        gui_button_boundaries = gui.guiPosition()
        gui.guiDisplay(img)

        # fps
        new_fps_time = time.time()
        fps = 1 / (new_fps_time - prev_fps_time)
        prev_fps_time = new_fps_time
        gui.fpsDisplay(img, fps)
        
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xff == ord("q"):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()