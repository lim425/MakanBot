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

    def guiPosition(self, offset=30, offset1=20, offset2=50, offset3=120, offset4=40, offset5=80, offset6=20, offset7=40, offset8=30):
        offset = offset * self.scale_x     # offset (horizontal & vertical) between each button
        offset1 = offset1 * self.scale_y    # offset between gui box and the promt display
        offset2 = offset2 * self.scale_y    # offset between promt display and finish button
        offset3 = offset3 * self.scale_y   # height of the self.next_selection_button self.home_button
        offset4 = offset4 * self.scale_y    # offset between finsih_eat_button and self.buttonA,B,C
        offset5 = offset5 * self.scale_y    # height of the button A-I
        offset6 = offset6 * self.scale_y    # offset between self.buttonG,H,I and progress bar
        offset7 = offset7 * self.scale_y    # height of the progress bar
        offset8 = offset8 * self.scale_x    # width of the button
        # Position boundaries
        self.gui_box = (self.frame_width//2, 0, self.frame_width, self.frame_height)
        self.prompt_display = (self.gui_box[0]+offset1, offset1, self.gui_box[2]-offset1, self.gui_box[3]//4)
        self.next_selection_button = (self.prompt_display[0], (self.prompt_display[3])+offset2, (((self.prompt_display[2]-self.prompt_display[0])//4)+offset8)+self.prompt_display[0], (self.prompt_display[3])+offset3)
        self.home_button = (self.next_selection_button[2]+offset, (self.prompt_display[3])+offset2, (((self.prompt_display[2]-self.prompt_display[0])//4)+offset8)+self.next_selection_button[2]+offset, (self.prompt_display[3])+offset3)
        self.buttonA = (self.next_selection_button[0], self.next_selection_button[3]+offset4, self.next_selection_button[2], self.next_selection_button[3]+offset4+offset5)
        self.buttonB = (self.buttonA[2]+offset, self.buttonA[1], (((self.prompt_display[2]-self.prompt_display[0])//4)+offset8)+self.buttonA[2]+offset, self.buttonA[3])
        self.buttonC = (self.buttonB[2]+offset, self.buttonB[1], (((self.prompt_display[2]-self.prompt_display[0])//4)+offset8)+self.buttonB[2]+offset, self.buttonB[3])
        self.buttonD=(self.buttonA[0], self.buttonA[3]+offset, self.buttonA[2], self.buttonA[3]+offset+offset5)
        self.buttonE=(self.buttonB[0], self.buttonB[3]+offset, self.buttonB[2], self.buttonB[3]+offset+offset5)
        self.buttonF=(self.buttonC[0], self.buttonC[3]+offset, self.buttonC[2], self.buttonC[3]+offset+offset5)
        self.buttonG=(self.buttonD[0], self.buttonD[3]+offset, self.buttonD[2], self.buttonD[3]+offset+offset5)
        self.buttonH=(self.buttonE[0], self.buttonE[3]+offset, self.buttonE[2], self.buttonE[3]+offset+offset5)
        self.buttonI=(self.buttonF[0], self.buttonF[3]+offset, self.buttonF[2], self.buttonF[3]+offset+offset5)
        self.progress_bar = (self.prompt_display[0], self.buttonG[3]+offset6, self.prompt_display[2], self.buttonG[3]+offset6+offset7)

        gui_position_boundaries = [self.gui_box, self.prompt_display, self.next_selection_button , self.home_button, self.buttonA, self.buttonB, self.buttonC, self.buttonD, self.buttonE, self.buttonF, self.buttonG, self.buttonH, self.buttonI, self.progress_bar]
        return gui_position_boundaries


    def guiDisplay(self, img):
        # GUI
        cv2.rectangle(img, (self.gui_box[0], self.gui_box[1]), (self.gui_box[2], self.gui_box[3]), (212, 61, 104), -1)
        # Prompt Display
        cv2.rectangle(img, (int(self.prompt_display[0]), int(self.prompt_display[1])), (int(self.prompt_display[2]), int(self.prompt_display[3])), (61, 212, 207), -1)
        # Function button
        cv2.rectangle(img, (int(self.next_selection_button[0]), int(self.next_selection_button[1])), (int(self.next_selection_button[2]), int(self.next_selection_button[3])), (104, 212, 61), -1)
        cv2.rectangle(img, (int(self.home_button[0]), int(self.home_button[1])), (int(self.home_button[2]), int(self.home_button[3])), (61, 61, 212), -1)
        # Progress Bar
        cv2.rectangle(img, (int(self.progress_bar[0]), int(self.progress_bar[1])), (int(self.progress_bar[2]), int(self.progress_bar[3])), (70, 62, 57), -1)
        # Buttons
        cv2.rectangle(img, (int(self.buttonA[0]), int(self.buttonA[1])), (int(self.buttonA[2]), int(self.buttonA[3])), (196, 186, 173), -1)
        cv2.rectangle(img, (int(self.buttonB[0]), int(self.buttonB[1])), (int(self.buttonB[2]), int(self.buttonB[3])), (196, 186, 173), -1)
        cv2.rectangle(img, (int(self.buttonC[0]), int(self.buttonC[1])), (int(self.buttonC[2]), int(self.buttonC[3])), (196, 186, 173), -1)
        cv2.rectangle(img, (int(self.buttonD[0]), int(self.buttonD[1])), (int(self.buttonD[2]), int(self.buttonD[3])), (196, 186, 173), -1)
        cv2.rectangle(img, (int(self.buttonE[0]), int(self.buttonE[1])), (int(self.buttonE[2]), int(self.buttonE[3])), (196, 186, 173), -1)
        cv2.rectangle(img, (int(self.buttonF[0]), int(self.buttonF[1])), (int(self.buttonF[2]), int(self.buttonF[3])), (196, 186, 173), -1)
        cv2.rectangle(img, (int(self.buttonG[0]), int(self.buttonG[1])), (int(self.buttonG[2]), int(self.buttonG[3])), (196, 186, 173), -1)
        cv2.rectangle(img, (int(self.buttonH[0]), int(self.buttonH[1])), (int(self.buttonH[2]), int(self.buttonH[3])), (196, 186, 173), -1)
        cv2.rectangle(img, (int(self.buttonI[0]), int(self.buttonI[1])), (int(self.buttonI[2]), int(self.buttonI[3])), (196, 186, 173), -1)

        self.drawTextCenter(img, "NEXT", self.next_selection_button)
        self.drawTextCenter(img, "HOME", self.home_button)
        self.drawTextCenter(img, "A", self.buttonA)
        self.drawTextCenter(img, "B", self.buttonB)
        self.drawTextCenter(img, "C", self.buttonC)
        self.drawTextCenter(img, "D", self.buttonD)
        self.drawTextCenter(img, "E", self.buttonE)
        self.drawTextCenter(img, "F", self.buttonF)
        self.drawTextCenter(img, "G", self.buttonG)
        self.drawTextCenter(img, "H", self.buttonH)
        self.drawTextCenter(img, "J", self.buttonI)


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