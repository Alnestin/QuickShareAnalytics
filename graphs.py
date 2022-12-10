import os.path
from datetime import date
import matplotlib.pyplot as plt

def main():

    figure, axis = plt.subplots(1, 2)

    if os.path.exists("albumNum.txt"):
        dates = []
        album_per_date = []
        with open('albumNum.txt') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip("\n")
                line = line.split(",")
                album_per_date.append(line[0])
                dates.append(line[1])
        axis[0].plot(dates, album_per_date)
        axis[0].set_title("Number of albums per date")
        # plt.show()

    if os.path.exists("picturesNum.txt"):
        dates = []
        pictures_per_date = []
        with open('picturesNum.txt') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip("\n")
                line = line.split(",")
                pictures_per_date.append(line[0])
                dates.append(line[1])
        axis[1].plot(dates, pictures_per_date)
        axis[1].set_title("Number of pictures per date")
    plt.show()

if __name__ == "__main__":
    main()