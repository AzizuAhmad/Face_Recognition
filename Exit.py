import os
import pickle

import cv2
import cvzone
import face_recognition as fr
import numpy as np
from datetime import datetime


import firebase_admin
from firebase_admin import credentials, storage

def findEncodings(imagesList):
    encodingList = []
    for img in imagesList :
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        encodingList.append(encode)
    return encodingList

def delete_images(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        os.remove(file_path)


# Initialize the Firebase Admin SDK
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)

now = datetime.now()
time = now.strftime("%H:%M:%S")
namaPath = "image/" + str(time) + ".png"
namaPath = namaPath.replace(":","_")

bucket_name = "facerecognition-717f7.appspot.com"

def delete_imageFB(image_path):
    bucket = storage.bucket(bucket_name)
    blob = bucket.blob(image_path)
    blob.delete()
    # print(f"Deleted: {image_path}")


# Get a reference to the storage bucket
bucket = storage.bucket(bucket_name)

# Specify the path to the image file in Firebase Storage
image_path = 'image/'

local_directory = 'image'
blobs = bucket.list_blobs(prefix=image_path)

for blob in blobs:
    # Extract the filename from the blob's name
    filename = os.path.basename(blob.name)

    # Download the image file to the local directory
    blob.download_to_filename(os.path.join(local_directory, filename))

# print('Images downloaded successfully.')
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgList = []
temp = []
folderPath = 'image'
pathList = os.listdir(folderPath)
for file in pathList:
    temp.append(file)


for path in pathList :
    imgList.append(cv2.imread(os.path.join(folderPath, path)))

encodingListKnown = findEncodings(imgList)

while True :
    index, img = cap.read()
    # cv2.imshow("Screen", img)

    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    # imgS = img[:, :, ::-1]
    faceCurFrame = fr.face_locations(imgS)
    encodeCurFrame = fr.face_encodings(imgS, faceCurFrame)
    # for (top, right, bottom, left) in faceCurFrame:
    #     # Draw the rectangle on the original image
    #     cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
    cv2.imshow("Screen", img)


    if(encodeCurFrame):

        for encodeFace ,faceLoc in zip(encodeCurFrame, faceCurFrame):
            faceDis = fr.face_distance(encodingListKnown, encodeFace)
            print(faceDis)
            nilaiTerkecil = min(faceDis)
            # print(nilaiTerkecil)
            if nilaiTerkecil < 0.45:
                print("silahkan keluar")
                least_value_index = np.argmin(faceDis)

                # print(temp[least_value_index])
                fbImage_path = "image/" + str(temp[least_value_index])
                delete_imageFB(fbImage_path)
                delete_images(folderPath)
                exit()
            else:
                print("gk bolh bang")
    else:
        print("wajah doko")


    cv2.waitKey(1)





