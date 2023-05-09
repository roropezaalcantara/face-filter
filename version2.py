"""
[Version 2]
Adds Rotational Function

[Assignment/Purpose]
Create program that adds a facial filter utilizing OpenCV

[Name(s)]
Ronny Oropeza

[Resources]
Intro Material/References-
https://analyticsindiamag.com/how-to-build-your-own-face-filter-with-opencv/
https://pysource.com/2019/03/25/pigs-nose-instagram-face-filter-opencv-with-python/

[Notes]
Install Guide-
1. Install Visual Studio with Desktop Development with C++ (ensure cmake tools for windows is checked)
    https://visualstudio.microsoft.com/
2. Install required packages with pip (commands below)
    *may require administrative privileges
    pip install cmake
    pip install dlib
    pip install opencv-python
    pip install imutils

[TODO]
- Face Filter Options - Full Face, mouth, eyes, forehead, background
- Face Filter Types - Static, Dynamic
- Add function to insert video/photo to apply filter to
- Improve stability

[Known Issues]
- Crashes when multiple faces are introduced to frame
"""

import cv2
import imutils
import numpy as np
import dlib
import math
from math import hypot

# Preset Values
rotationValue = 0
rotationChange = 0

print("Program Start")
# Prepares Camera Feed
capture = cv2.VideoCapture(0)
_, frame = capture.read()
print("Camera Loaded")

# Prepares select image
imageFile = cv2.imread("Green-Up-Arrow.png")
print("Images Loaded")

# Generate Mask for subject
rows, cols, _ = frame.shape
subjectMask = np.zeros((rows, cols), np.uint8)
print("Mask Generated")

# Loading shape predictor and detector with dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor.dat")
print("Face Detection Loaded")

print("Initializing Filter")
while True:
    # Loads camera feed
    _, frame = capture.read()
    subjectMask.fill(0)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(frame)

    for face in faces:
        # Utilizing the previously established detector and predictor
        # points are placed on subject(face) and given coordinates labeled as landmarks assigned with a numerical value
        # From each landmark, an X and Y coordinate value can be extracted and used for positioning uploaded image
        landmarks = predictor(gray_frame, face)

        # Gathers X and Y values for two points on subject to determine the angle for the image to match the subject
        xVal = landmarks.part(29).x - landmarks.part(30).x
        yVal = landmarks.part(29).y - landmarks.part(30).y
        rotAngle = math.atan(xVal / yVal)*100
        print(rotAngle)

        # Utilizes calculated angle and applies it to the uploaded images to be used for the filter
        if rotationValue != rotAngle:
            rotationChange = rotAngle - rotationValue
            imageFile = imutils.rotate(imageFile, angle=rotationChange)
            rotationValue = rotAngle

        # Subject coordinates
        # Defines coordinates and size to a variable
        centerSubject = (landmarks.part(30).x, landmarks.part(30).y)
        leftSubject = (landmarks.part(31).x, landmarks.part(31).y)
        rightSubject = (landmarks.part(35).x, landmarks.part(35).y)
        subjectWidth = int(hypot(leftSubject[0] - rightSubject[0], leftSubject[1] - rightSubject[1]) * 1.7)
        subjectHeight = int(subjectWidth * 0.77)

        # Subject Position
        # Calculates approximate corner of subject to apply image to
        top_left = (int(centerSubject[0] - subjectWidth / 2), int(centerSubject[1] - subjectHeight / 2))

        # Applying the image to the subject
        # Resizes uploaded image to match the dimensions of the subject
        imageSubject = cv2.resize(imageFile, (subjectWidth, subjectHeight))
        imageSubject_gray = cv2.cvtColor(imageSubject, cv2.COLOR_BGR2GRAY)
        # Combines subject and image and output to new feed
        _, subjectMask = cv2.threshold(imageSubject_gray, 25, 255, cv2.THRESH_BINARY_INV)
        subjectZone = frame[top_left[1]: top_left[1] + subjectHeight, top_left[0]: top_left[0] + subjectWidth]
        nonSubjectZone = cv2.bitwise_and(subjectZone, subjectZone, mask=subjectMask)
        final_frame = cv2.add(nonSubjectZone, imageSubject)
        frame[top_left[1]: top_left[1] + subjectHeight, top_left[0]: top_left[0] + subjectWidth] = final_frame
    cv2.imshow("Final Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
