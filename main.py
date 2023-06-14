import os
import pickle

import cv2
import cvzone
import face_recognition
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# importing the mode images into list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

# print(len(imgModeList))

# Load/import the encoding file from encoding file
# rb = read binary,wb = write binary
print("Loading Encode File...")
file = open('Encode File.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
# ekstrak file and saperate the id and the binary
encodeListKnown, studentIds = encodeListKnownWithIds
# print(studentIds)
print("Encode File Loaded...")




while True:
    success, img = cap.read()

    # resize img and convert BGR TO RGB
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # feed in value to our face recognition
    faceCurFrame = face_recognition.face_locations(imgS)
    # our previous image we need to find encodings our new one and compare it
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162+480, 55:55+640] = img
    imgBackground[44:44+633, 808:808+414] = imgModeList[3]

    # compare our generate encoding one by one
    # extrac information encodeCureFrame to enceodeFace and information faceCurFram to faceLoc
    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        # compare image known and current image
        # more lower phase distance it means its look matches
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print("matches", matches)
        # print("faceDis", faceDis)

        #extract value phase distance on the list
        matchIndex = np.argmin(faceDis)
        # print('match Index', matchIndex)

        # make rectange on face
        if matches[matchIndex]:
            print("Known face detected")
            print(studentIds[matchIndex])
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            # add x and y value of our image start
            bbox = 55+x1, 162+y1, x2 - x1, y2 - y1
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)


    # cv2.imshow("Web Cam", imgBackground)
    cv2.imshow("Face Attandance", imgBackground)
    cv2.waitKey(1)
