import cv2
import time
import mediapipe as mp

class FaceMeshDetector():

    def __init__(self, static_image_mode=False, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, color=(255,0,0), thickness=2, circle_radius=2):
        self.static_image_mode=static_image_mode
        # Facemesh parameter
        self.max_num_faces=max_num_faces
        self.refine_landmarks=refine_landmarks
        self.min_detection_confidence=min_detection_confidence
        # Drawing parameter
        self.color=color
        self.thickness=thickness
        self.circle_radius=circle_radius


        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.static_image_mode, self.max_num_faces, self.refine_landmarks, self.min_detection_confidence)
        self.drawSpec = self.mpDraw.DrawingSpec(self.color, self.thickness, self.circle_radius)

    def findFaceMesh(self, img, draw=True):
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(self.imgRGB)
        faces = []
        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image=img, landmark_list=faceLms, connections=self.mpFaceMesh.FACEMESH_CONTOURS,
                                            landmark_drawing_spec=self.drawSpec,connection_drawing_spec=self.drawSpec)
                face = []
                for id,lm in enumerate(faceLms.landmark):
                    ih, iw, ic = img.shape
                    x,y = int(lm.x*iw), int(lm.y*ih)
                    # cv2.putText(img, str(id), (x, y), cv2.FONT_HERSHEY_PLAIN,0.7, (0, 255, 0), 1)
                    # print(id,x,y)
                    face.append([x,y])
                faces.append(face)
        return img, faces


def main():
    cap = cv2.VideoCapture(0)
    frame_width  = 1280
    frame_height = 720

    prev_frame_time = 0
    new_frame_time = 0

    detector = FaceMeshDetector()

    while True:
        success, img = cap.read()
        if not success:
            print("End of video or failed read")               
            break

        img = cv2.resize(img, (frame_width, frame_height))
        img, faces = detector.findFaceMesh(img)

        # FPS
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time

        cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
                    3, (255, 0, 0), 3)
        
        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xff == ord("q"):
            break
    cv2.destroyAllWindows()





if __name__ == "__main__":
    main()