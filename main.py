import json
import firebase_admin
from firebase_admin import credentials, storage
import os.path

def is_image(file_name):
    return file_name[-5:] == ".jpeg" or file_name[-4:] == ".png" or file_name[-5:] == ".HEIC"

def get_num_pictures(blobs):
    count = 0
    for blob in blobs:
        blob_name = blob.name
        if is_image(blob_name):
            count += 1
    return count

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

def main():
    f = open('firebaseLink.json')
    data = json.load(f)
    f.close()

    storage_bucket_path = data["link"]

    cred = credentials.Certificate("firebaseKey.json")
    app = firebase_admin.initialize_app(cred, {'storageBucket': storage_bucket_path})

    bucket = storage.bucket(app=app)
    blobs = list(bucket.list_blobs())

    # A blob has: name, prefixes

    num_pictures = get_num_pictures(blobs)
    num_albums = get_num_albums(blobs)

    if os.path.exists("albumNum.txt"):
        # Append to the file
        f = open("albumNum.txt", "a")
        f.write(str(num_albums) + "\n")
        f.close()
    else:
        # Create the file and write to it
        f = open("albumNum.txt", "w")
        f.write(str(num_albums) + "\n")
        f.close()
    
    if os.path.exists("picturesNum.txt"):
        # Append to the file
        f = open("picturesNum.txt", "a")
        f.write(str(num_pictures) + "\n")
        f.close()
    else:
        # Create the file and write to it
        f = open("picturesNum.txt", "w")
        f.write(str(num_pictures) + "\n")
        f.close()

if __name__ == "__main__":
    main()