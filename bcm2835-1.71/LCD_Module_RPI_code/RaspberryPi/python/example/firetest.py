# Written by Spencer Ekin
# April 19th, 2023
# This code shows the capability of the Rpi to Read and Write to and from the Firebase server
import pyrebase
import time

config = {
  "apiKey": "AIzaSyCBW17T8P2SM-WuyqxoR-BhJkOgOfHAk3c",
  "authDomain": "felboard-bec87.firebaseapp.com",
  "projectId": "felboard-bec87",
  "storageBucket": "felboard-bec87.appspot.com",
  "messagingSenderId": "945167240967",
  "appId": "1:945167240967:web:12ef8233e232d1211cffa2",
  "databaseURL": "https://felboard-bec87-default-rtdb.firebaseio.com/",
}

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()

# Read boolean value from our Firebase server
boolean = db.child("piData").get()
boolean = boolean.val()
print(boolean)

# Write new value to "piData" on the Firebase server
if (boolean):
  print("piData is True, changing it to False")
  db.child("piData").set(False)
  time.sleep(1)
  boolean = db.child("piData").get()
  boolean = boolean.val()
else:
  print("piData is False, changing it to True")
  db.child("piData").set(True)
  time.sleep(1)
  boolean = db.child("piData").get()
  boolean = boolean.val()

# Print new value
print(boolean)
exit()

