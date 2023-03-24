import os

def count_png_files(path):
    """Recursively counts the number of PNG files in a directory and its subdirectories."""

    # Initialize counters
    total_count = 0
    folder_counts = {}

    # Traverse the directory and its subdirectories
    for root, dirs, files in os.walk(path):
        folder_count = 0

        # Count the number of PNG files in the current directory
        for file in files:
            if file.endswith('.png'):
                total_count += 1
                folder_count += 1

        # Store the folder count in a dictionary
        folder_counts[root] = folder_count

    return total_count, folder_counts

# Example usage
total_count, folder_counts = count_png_files('/Users/exnihilo/Pictures/AI Generator Results/Refraxions')

# Print the results
print(f'Total PNG files: {total_count}')

for folder, count in folder_counts.items():
    # We just need the name of the last folder in the hierarchy
    folder_name = folder.split('/')[-1]
    print(f'{folder_name}: {count}')
