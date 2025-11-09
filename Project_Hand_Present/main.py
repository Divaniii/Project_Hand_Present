import os

import cv2

import numpy as np

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
annotations = [[]] # List within a list
annotationNumber = -1
annotationStart = False

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

        lmlist = hand['lmList']

        # Map from webcam coordinates to slide coordinates
        index_x = lmlist[8][0]  # Index finger tip X coordinate in webcam
        index_y = lmlist[8][1]  # Index finger tip Y coordinate in webcam

        # Map webcam coordinates (0 to width/height) to slide coordinates (0 to slide_w/slide_h)
        # Added padding to make movement easier at edges
        padding = 50  # pixels of padding for easier movement at edges

        # Map X: from webcam width to slide width with padding
        slide_x = int(np.interp(index_x, [padding, width - padding], [0, width]))
        slide_x = max(0, min(slide_x, width))  # Constrain to slide boundaries

        # Map Y: from webcam height to slide height with padding
        slide_y = int(np.interp(index_y, [padding, height - padding], [0, height]))
        slide_y = max(0, min(slide_y, height))  # Constrain to slide boundaries

        indexfinger = (slide_x, slide_y)
        print(fingers)

        if cy <= gestureThreshold: #if hand is at hte height of the face
            if fingers == [1,0,0,0,0]: #Gesture 1 : Left
                print("Left")
                if imgNumber>0:
                    buttonPress = True
                    annotations = [[]]  # List within a list
                    annotationNumber = 0
                    annotationStart = False
                    imgNumber -= 1

            if fingers == [0,0,0,0,1]: #Gesture 2 : Right
                print("Right")
                if imgNumber < len(pathImages):
                    buttonPress = True
                    annotations = [[]]  # List within a list
                    annotationNumber = 0
                    annotationStart = False
                    imgNumber += 1

            if fingers == [0,0,0,0,0]:
                break

        if fingers == [0,1,1,0,0]: #Gesture 3 : Pointer
            cv2.circle(imgCurrentSlide, indexfinger, 12, (0,0,255), cv2.FILLED)
            annotationStart = False

        if fingers == [0,1,0,0,0]: #Gesture 4 : Draw
            cv2.circle(imgCurrentSlide, indexfinger, 12, (0,0,255), cv2.FILLED)
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([]) # without this - no list to call
            annotations[annotationNumber].append(indexfinger)

        else:
            annotationStart = False

        if fingers == [0,1,1,1,0]:
            if annotations:
                if annotationNumber >= 0:
                    annotations.pop(-1)#remove the last drawing
                    annotationNumber -= 1
                    buttonPress = True


#Button Pressed Iterations
    if buttonPress:
        buttonCounter +=1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPress = False

    for i in range((len(annotations))):
        for j in range(len(annotations[i])): # loop thorugh all of the points
            if j!=0:
                cv2.line(imgCurrentSlide, annotations[i][j-1], annotations[i][j], (0,0,200), 12)

#Addding webcam image on slide
    imgSmall = cv2.resize(img, (ws, hs))
    h, w,_ = imgCurrentSlide.shape #width and height of slide
    imgCurrentSlide[0:hs,w-ws:w] = imgSmall #top right corner matrix
    cv2.imshow("Image", img)
    cv2.imshow("SlidePresentation", imgCurrentSlide)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
