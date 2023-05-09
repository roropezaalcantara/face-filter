"""
[Main Build]
Contains latest instance of the code

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
- Improve developer readability
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


def calculate_part_boundingbox(centerPart,leftPart,rightPart,widthscale,heightscale):
    # Subject coordinates
    # Defines coordinates and size to a variable
    ### This code may be changed/removed with a new method of data collection and analysis
    centerSubject = (landmarks.part(centerPart).x, landmarks.part(centerPart).y)
    leftSubject = (landmarks.part(leftPart).x, landmarks.part(leftPart).y)
    rightSubject = (landmarks.part(rightPart).x, landmarks.part(rightPart).y)
    subjectWidth = int(hypot(leftSubject[0] - rightSubject[0], leftSubject[1] - rightSubject[1]) * widthscale)
    subjectHeight = int(subjectWidth * heightscale)

    # Subject Position
    # Calculates approximate corner of subject to apply image to
    top_left = (int(centerSubject[0] - subjectWidth / 2), int(centerSubject[1] - subjectHeight / 2))
    return subjectWidth, subjectHeight, top_left


def filter_query():
    # Asks Filter type and image name
    if typeVal == 1:
        print("Full Face Filter Loading")
    elif typeVal == 2:
        print("Center Face Filter Loading")
    elif typeVal == 3:
        print("Lower Face Filter Loading")
    elif typeVal == 4:
        print("Outer Face Filter Loading")
    else:
        print("Please Select One of the Options")
        exit(10)

    imageName = input("\nEnter Filter Image Name\n")
    return imageName


def read_image(imageName):
    # Prepares select image
    imageFile = cv2.imread(imageName)
    print("Images Loaded")
    return imageFile


def full_face():
    return calculate_part_boundingbox(30,0,16,1.2,1.3)


def center_face():
    return calculate_part_boundingbox(30,31,35,1.7,.77)


def lower_face():
    return calculate_part_boundingbox(51,3,13,1.1,1)


def outer_face():
    return calculate_part_boundingbox(31, 2, 16, 1.7, .77)


# Preset Values
rotationValue = 0

# Asks Filter type and image name
print("\nSelect the Filter Type\n"
      "1: Full Face\n"
      "2: Center Face\n"
      "3: Lower Face\n"
      "4: Outer Face\n")
typeVal = input("Select Corresponding Number:\n")
typeVal = int(typeVal)
imageName = filter_query()

print("\nProgram Start")
# Prepares Camera Feed
capture = cv2.VideoCapture(0)
_, frame = capture.read()
print("Camera Loaded")

# Prepares select image
imageFile = read_image(imageName)

# Generate Mask for subject
rows, cols, _ = frame.shape
subjectMask = np.zeros((rows, cols), np.uint8)
print("Mask Generated")

# Loading shape predictor and detector with dlib
### This code may be changed/removed with a new method of data collection and analysis
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
        ### This code may be changed/removed with a new method of data collection and analysis
        xVal = landmarks.part(29).x - landmarks.part(30).x
        yVal = landmarks.part(29).y - landmarks.part(30).y
        rotAngle = math.atan(xVal / yVal) * 100
        print(rotAngle)

        # Utilizes calculated angle and applies it to the uploaded images to be used for the filter
        ### This code may be changed/removed with a new method of data collection and analysis
        if rotationValue != rotAngle:
            rotationChange = rotAngle - rotationValue
            imageFile = imutils.rotate(imageFile, angle=rotationChange)
            rotationValue = rotAngle

        # Executes Specific Function
        if typeVal == 1:
            # Full Face Filter
            subjectWidth, subjectHeight, top_left = full_face()
        elif typeVal == 2:
            # Center Face Filter
            subjectWidth, subjectHeight, top_left = center_face()
        elif typeVal == 3:
            # Lower Face Filter
            subjectWidth, subjectHeight, top_left = lower_face()
        elif typeVal == 4:
            # Outer Face Filter
            exit(99)

        # Applying the image to the subject
        # Resizes uploaded image to match the dimensions of the subject
        imageSubject = cv2.resize(imageFile, (subjectWidth, subjectHeight))
        imageSubject_gray = cv2.cvtColor(imageSubject, cv2.COLOR_BGR2GRAY)
        # Combines subject and image and output to new feed
        _, subjectMask = cv2.threshold(imageSubject_gray, 25, 255, cv2.THRESH_BINARY_INV)
        # Outlines Area Where Filter will be applied
        subjectZone = frame[top_left[1]: top_left[1] + subjectHeight, top_left[0]: top_left[0] + subjectWidth]
        nonSubjectZone = cv2.bitwise_and(subjectZone, subjectZone, mask=subjectMask)
        final_frame = cv2.add(nonSubjectZone, imageSubject)
        # Finalizes frame contents
        frame[top_left[1]: top_left[1] + subjectHeight, top_left[0]: top_left[0] + subjectWidth] = final_frame
    cv2.imshow("Final Frame", frame)
    # Program Pause Period
    key = cv2.waitKey(1)

    # Filter Switch
    if key == 27:
        exit(101)
    elif key == 49:
        typeVal = 1
        imageName = filter_query()
        imageFile = read_image(imageName)
    elif key == 50:
        typeVal = 2
        imageName = filter_query()
        imageFile = read_image(imageName)
    elif key == 51:
        typeVal = 3
        imageName = filter_query()
        imageFile = read_image(imageName)
    elif key == 52:
        typeVal = 4
        imageName = filter_query()
        imageFile = read_image(imageName)
