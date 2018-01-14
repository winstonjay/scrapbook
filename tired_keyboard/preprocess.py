'''
preprocess.py:

GOAL:
    Quantify keyboard key usage from images.
PLAN:
    Walk through folder "data/imgs", for each file:
    load image as an array and sum the pixels.
    Write results to csv file as we go.
'''
import os
import numpy as np
from PIL import Image

image_folder = "data/imgs/"
output_file  = "data/keyscores.csv"

def main():
    with open(output_file, "w") as csvfile:
        # write csv head. cba to use the module.
        csvfile.write("key,score\n")
        for key_name in os.listdir(image_folder):
            if not key_name.endswith(".png"):
                continue
            # load image convert to greyscale
            img = Image.open(image_folder + key_name).convert('L')
            # convert to an array and get the sum.
            score = np.asarray(img, dtype='uint8').sum()
            # use name without exstention.
            name  = key_name.rsplit('.', 1)[0]
            csvfile.write("{0},{1}\n".format(name, score))
    print("Saved data to file '%s'." % output_file)

if __name__ == "__main__":
    main()