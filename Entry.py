import cv2
import numpy as np
import face_recognition as fr
from PIL import Image
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import os


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://facerecognition-717f7-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageURL': "facerecognition-717f7.appspot.com"
})

now = datetime.now()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

time = now.strftime("%H:%M:%S")
namaPath = "image/" + str(time) + ".png"
namaPath = namaPath.replace(":","_")
namafile = namaPath.split("/")
namafile = namafile[1]
fototemp = []

bucket_name = "facerecognition-717f7.appspot.com"

while True :
    index, img = cap.read()
    cv2.imshow("Screen", img)
    gambar = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    encode = fr.face_encodings(gambar)
    if(encode) :
        print("Wajah terdeteksi")
        img = cv2.resize(img, (300, 300))
        cv2.imwrite(str(namaPath), img)

        # upload to firebase storage
        bucket = storage.bucket(bucket_name)
        blob = bucket.blob(namaPath)
        blob.upload_from_filename(namaPath)
        break
    else :
        print("Wajah Doko?")
    cv2.waitKey(2)

os.remove(namaPath)
cv2.destroyAllWindows()