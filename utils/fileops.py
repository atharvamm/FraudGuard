import shutil
import os

# Create a copy of a file.
def copy_file(src_filename, dest_filename):
    try:
        shutil.copy2(src_filename, dest_filename)
        print(f"File '{src_filename}' copied to '{dest_filename}' successfully.")
    except IOError as e:
        print(f"Error copying file: {e}")

# Delete all files in directory
def delete_files_in_directory(directory_path):
   try:
    files = os.listdir(directory_path)
    for file in files:
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    print("All files deleted successfully.")
   except OSError:
     print("Error occurred while deleting files.")

