import os

import cv2

from cvzone.HandTrackingModule import HandDetector

#Variables
width, height = 1000, 500
folderPath = "Presentation"

#camera setup
cap = cv2.VideoCapture(0)

cap.set(3, width)
cap.set(4, height)

#Get list of presentation images
pathImages = sorted(os.listdir(folderPath), key=len)

#Variables 2.0
imgNumber = 0
hs, ws = int(120*1), int(213*1)
gestureThreshold = 300
buttonPress = False
buttonCounter = 0
buttonDelay = 30

#Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1) #0.8: confidence that it is a hand

while True:
    #import images
    success, img = cap.read()
    img = cv2.flip(img,1)
    pathFullImages = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrentSlide = cv2.imread(pathFullImages)

    hands, img = detector.findHands(img)
    cv2.line(img,(0, gestureThreshold), (width, gestureThreshold), (0,255,0), 10)

    #Get landmark of hands
    if hands and buttonPress is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand) #count how many fingers are up
        cx, cy = hand['center']
        print(fingers)

        if cy <= gestureThreshold: #if hand is at hte height of the face
            if fingers == [1,0,0,0,0]: #Gesture 1 : Left
                print("Left")
                if imgNumber>0:
                    buttonPress = True
                    imgNumber -= 1

            if fingers == [0,0,0,0,1]: #Gesture 2 : Right
                print("Right")
                if imgNumber < len(pathImages):
                    buttonPress = True
                    imgNumber += 1

#Button Pressed Iterations
    if buttonPress:
        buttonCounter +=1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPress = False

#Addding webcam image on slide
    imgSmall = cv2.resize(img, (ws, hs))
    h, w,_ = imgCurrentSlide.shape #width and height of slide
    imgCurrentSlide[0:hs,w-ws:w] = imgSmall #top right corner matrix
    cv2.imshow("Image", img)
    cv2.imshow("SlidePresentation", imgCurrentSlide)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
