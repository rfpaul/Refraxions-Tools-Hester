import os
from glob import glob
import numpy as np
import pandas as pd
from PIL import Image
from scipy.spatial import KDTree
from sklearn.cluster import KMeans
from webcolors import rgb_to_name, CSS3_HEX_TO_NAMES, hex_to_rgb

# Set the number of dominant colors to classify
NUM_COLORS = 5

def convert_rgb_to_closest_name(rgb_tuple):
    # a dictionary of all the hex and their respective names in css3
    css3_db = CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))

    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return names[index]

# Set the input pattern
input_pattern = '/Users/exnihilo/Pictures/AI Generator Results/Refraxions/*/*.png'
file_list = glob(input_pattern)

# Set the output report name & location
output_report = '/Users/exnihilo/Pictures/AI Generator Results/Refraxions/Refraxions_summary.csv'
# Collect the data into this list; it'll be cast into a pandas dataframe
data = []
# Column names for the dataframe
col_names = ["Filename",
             "ID",
             "Numeric ID",
             "Subject",
             "Dominant color",
             "Subdominant color",
             "Third color",
             "Fourth color",
             "Fifth color"]

# Loop through each file in the input directory
for filepath in file_list:
    if not filepath.endswith('.png'):
        continue

    # List to hold the current row of data
    row_data = []
    # Split the filepath by directory separator
    split_filepath = filepath.split('/')
    # Append the filename to the row data list
    row_data.append(split_filepath[-1])
    # Append the name ID to the row data list
    row_data.append(split_filepath[-1][:-4])
    # Append the numeric ID to the row data list
    row_data.append(row_data[1].split()[1])
    # Append the subject type to the row data list
    row_data.append(split_filepath[-2])

    # Load the image and convert to a numpy array
    image = Image.open(filepath)
    image_array = np.array(image)

    # Reshape the array to a 2D matrix of pixels
    num_pixels = image_array.shape[0] * image_array.shape[1]
    pixel_matrix = image_array.reshape(num_pixels, 3)

    # Use KMeans clustering to classify the dominant colors
    kmeans = KMeans(n_clusters=NUM_COLORS, random_state=0).fit(pixel_matrix)
    labels = kmeans.labels_
    dominant_colors, counts = np.unique(labels, return_counts=True)
    dominant_colors = kmeans.cluster_centers_[dominant_colors]

    # Sort the dominant colors by their count in descending order
    sort_idx = np.argsort(counts)[::-1]
    dominant_colors = dominant_colors[sort_idx]

    # Map the RGB values of the dominant colors to their names
    color_names = []
    for color in dominant_colors:
        color_name = convert_rgb_to_closest_name(color)
        color_names.append(color_name)

    # Extend the color names to the row data list
    row_data.extend(color_names)

    # Append the row data to the data list
    data.append(row_data)

    # Create a string of color names separated by commas
    color_string = ', '.join(color_names)

    print("{}: {}".format(split_filepath[-1], color_string))

# Construct a pandas dataframe from the data list
df = pd.DataFrame(data, columns = col_names)

# Save dataframe to output as CSV
df.to_csv(output_report, index = False)
