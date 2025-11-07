import numpy as np
import cv2
import time
import mediapipe as mp

#for video
cap = cv2.VideoCapture(0)
frame_width  = 1280
frame_height = 720

prev_frame_time = 0
new_frame_time = 0


mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(static_image_mode=False, max_num_faces=2, refine_landmarks=True, min_detection_confidence=0.5)
drawSpec = mpDraw.DrawingSpec(color=(255,0,0), thickness=2, circle_radius=2)
while True:
    
    success, img = cap.read()

    if not success:
        print("End of video or failed read")               
        break
    img = cv2.resize(img, (frame_width, frame_height))
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)

    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(image=img, landmark_list=faceLms, connections=mpFaceMesh.FACEMESH_CONTOURS,
                                  landmark_drawing_spec=drawSpec,connection_drawing_spec=drawSpec)
            for id,lm in enumerate(faceLms.landmark):
                #print(lm)
                ih, iw, ic = img.shape
                x,y = int(lm.x*iw), int(lm.y*ih)
                print(id,x,y)

    
    new_frame_time = time.time()
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time

    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)
    
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cv2.destroyAllWindows()
