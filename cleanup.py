import os
import shutil
import hashlib
import time

def delete_folder_contents(folder_path):
    if os.path.exists(folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")
            for dir in dirs:
                try:
                    dir_path = os.path.join(root, dir)
                    shutil.rmtree(dir_path)
                    print(f"Deleted folder: {dir_path}")
                except Exception as e:
                    print(f"Failed to delete {dir_path}: {e}")

def clean_temp_files():
    print("Cleaning temporary files...")

    temp_folders = [
        os.getenv('TEMP'),
        os.getenv('TMP'),
        os.path.join(os.getenv('SystemRoot'), 'Temp')
    ]

    for folder in temp_folders:
        if folder:
            delete_folder_contents(folder)
    
    print("Temporary files cleaned successfully.")

def find_and_remove_duplicate_files(folder_path):
    print("Searching for duplicate files...")

    file_hashes = {}
    duplicates = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                if file_hash in file_hashes:
                    duplicates.append(file_path)
                    print(f"Duplicate found: {file_path}")
                else:
                    file_hashes[file_hash] = file_path
            except Exception as e:
                print(f"Failed to hash {file_path}: {e}")

    for file in duplicates:
        try:
            os.remove(file)
            print(f"Deleted duplicate file: {file}")
        except Exception as e:
            print(f"Failed to delete {file}: {e}")

    print("Duplicate files removed successfully.")

if __name__ == "__main__":
    start_time = time.time()
    
    # Clean temp files
    clean_temp_files()

    # Optional: Specify folders to clean up duplicate files
    folders_to_check = [
        os.path.expanduser('~'),  # User's home directory
        os.path.join(os.getenv('SystemDrive'), '\\')  # Root of the system drive (C:\)
    ]

    for folder in folders_to_check:
        find_and_remove_duplicate_files(folder)

    end_time = time.time()
    print(f"Cleaning completed in {end_time - start_time:.2f} seconds.")
