import shutil

# Create a copy of a file.
def copy_file(src_filename, dest_filename):
    try:
        shutil.copy2(src_filename, dest_filename)
        print(f"File '{src_filename}' copied to '{dest_filename}' successfully.")
    except IOError as e:
        print(f"Error copying file: {e}")
