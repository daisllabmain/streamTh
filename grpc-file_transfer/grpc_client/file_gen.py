import os
import random
import shutil

def create_random_files_in_folder(base_folder_path, group_name, num_files, size_range):
    # Create the specific group folder path
    folder_path = os.path.join(base_folder_path, group_name)
    
    # Delete the folder if it exists
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"Deleted existing folder: {folder_path}")
    
    # Create the folder
    os.makedirs(folder_path, exist_ok=True)
    print(f"Created new folder: {folder_path}")
    
    print(f"Generating {num_files} files in '{group_name}' with random sizes between {size_range[0]} MB and {size_range[1]} MB.")
    
    for i in range(1, num_files + 1):
        # Generate random file size within the specified range
        file_size_mb = random.randint(size_range[0], size_range[1])
        file_size_bytes = file_size_mb * 1024 * 1024  # Convert MB to bytes
        
        file_path = os.path.join(folder_path, f"{group_name}_{i:02d}.dat")
        
        # Use `dd` to create a file with the specified size
        dd_cmd = f"dd if=/dev/zero of={file_path} bs=1M count={file_size_mb} status=none"
        os.system(dd_cmd)
        
        print(f"Created file: {file_path} with size {file_size_mb} MB")
    
    print(f"File generation complete for {group_name}.")

# Define the path for the base folder to be created
current_dir = os.getcwd()
base_folder_name = "random_files_folder"
base_folder_path = os.path.join(current_dir, base_folder_name)

# Define size ranges for each group
small_size_range = (5, 10)  # Small files between 5 MB and 10 MB
medium_size_range = (11, 50)  # Medium files between 11 MB and 50 MB
large_size_range = (51, 100)  # Large files between 51 MB and 100 MB

# Define the number of files to be generated for each group
num_small_files = 10
num_medium_files = 5
num_large_files = 2

# Create folders and generate random files for each group
create_random_files_in_folder(base_folder_path, 'small', num_small_files, small_size_range)
create_random_files_in_folder(base_folder_path, 'medium', num_medium_files, medium_size_range)
create_random_files_in_folder(base_folder_path, 'large', num_large_files, large_size_range)
