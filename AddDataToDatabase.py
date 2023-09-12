
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey1.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facerecognitionrealtime-21ed6-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

ref = db.reference('Student')

data = {
    # base on id/ktm
    "123457":
        {
            # key : value
            "name": "Azizu Ahmad",
            "major": "Teknik Informatika",
            "starting_year": 2021,
            "total_attendance": 6,
            "standing": "G",
            "year": 2,
            "last_parking": "2023-05-12 12:00:54"

        },
    "321654":
        {
            # key : value
            "name": "Hafizh",
            "major": "Teknik Informatika",
            "starting_year": 2021,
            "total_attendance": 2,
            "standing": "G",
            "year": 2,
            "last_parking": "2023-04-12 08:21:22"

        },
    "852741":
        {
            # key : value
            "name": "Farrel tod",
            "major": "Teknik Informatika",
            "starting_year": 2021,
            "total_attendance": 1,
            "standing": "G",
            "year": 2,
            "last_parking": "2023-05-22 13:00:54"

        },
    "963852":
        {
            # key : value
            "name": "Alam Vintod",
            "major": "Teknik Informatika",
            "starting_year": 2021,
            "total_attendance": 5,
            "standing": "G",
            "year": 2,
            "last_parking": "2023-05-11 14:01:54"

        },
}

for key, value in data.items():
    ref.child(key).set(value)