import json
import firebase_admin
from firebase_admin import credentials, storage
import os.path
from datetime import date
import matplotlib.pyplot as plt

# Check if the file is an image
def is_image(file_name):
    return file_name[-5:] == ".jpeg" or file_name[-4:] == ".png" or file_name[-5:] == ".HEIC"

# Number of pictures in a blob
def get_num_pictures(blobs):
    count = 0
    for blob in blobs:
        blob_name = blob.name
        if is_image(blob_name):
            count += 1
    return count

# Number of albums in a blob.
def get_num_albums(blobs):
    count = 0
    albums = []
    thru_folders = ["ThruDates", "ThruPeople", "ThruPlaces", "ThruTime", "user1", "images"]
    for blob in blobs:
        blob_name = blob.name
        path = blob_name.split("/")
        for x in path:
            if (x not in albums) and (len(x.split(".")) == 1) and (x != "") and (x not in thru_folders):
                albums.append(x)
                count += 1
    return count

def store(fileName, var):
    if os.path.exists(fileName):
        # Append to the file
        f = open(fileName, "a")
        f.write(str(var) + "," + str(date.today()) + "\n")
        f.close()
    else:
        # Create the file and write to it
        f = open(fileName, "w")
        f.write(str(var) + "," + str(date.today()) + "\n")
        f.close()

def main():
    f = open('firebaseLink.json')
    data = json.load(f)
    f.close()

    storage_bucket_path = data["link"]

    cred = credentials.Certificate("firebaseKey.json")
    app = firebase_admin.initialize_app(cred, {'storageBucket': storage_bucket_path})

    bucket = storage.bucket(app=app)
    blobs = list(bucket.list_blobs()) # A blob has: name, prefixes

    num_pictures = get_num_pictures(blobs)
    num_albums = get_num_albums(blobs)

    album_file = "albumNum.txt"
    picture_file = "picturesNum.txt"

    store(album_file, num_albums)
    store(picture_file, num_pictures)

    

if __name__ == "__main__":
    main()