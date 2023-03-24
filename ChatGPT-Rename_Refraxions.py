import os
import random

directory = "/Users/exnihilo/Pictures/AI Generator Results/Refraxions"  # Replace with the path to your directory
counter = 2  # Starting number for the new filenames

# Generate a list of random numbers from 2 to 499
random_numbers = random.sample(range(2, 500), 498)

for subdir, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".png") and file != "Refraxions 1.png" and file != "Refraxions 500.png":
            old_path = os.path.join(subdir, file)
            new_name = "Refraxions " + str(random_numbers[counter - 2]) + ".png"
            new_path = os.path.join(subdir, new_name)
            os.rename(old_path, new_path)
            counter += 1
