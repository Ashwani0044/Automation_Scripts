# The script to instantly bundel the file into Documents/, Images/, and Code/ subfolders, leaving behind a cleanup_log.txt showing the exact date and time it executed.

import os
import shutil
from datetime import datetime

# define the directory that needs to be cleared
TARGET_DIR = '.' # '.' means the current directory

# mapping files extensions to their destination folders
FILE_TYPES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.svg'],
    'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx'],
    'Code': ['.py', '.js', '.html', '.css', '.json'],
    'Compressed': ['.zip', '.tar', '.gz', '.rar']
}

def organize_folder():
    print(f"Starting cleanup in: {os.path.abspath(TARGET_DIR)}")
    moved_file_count = 0

    # Iterating through all the files in the targeted dir
    for item in os.listdir(TARGET_DIR):
        item_path = os.path.join(TARGET_DIR, item)

        # skipping dir as we only want to move files
        if os.path.isdir(item_path):
            continue

        # skip the script itself so it doesn't move
        if item == "cleaner.py" or item == "cleanup_log.txt":
            continue

        # get the file extension
        _, extension = os.path.splitext(item)
        extension = extension.lower()

        # find the correct folder for this extension
        destination_folder = None
        for folder_name, extensions in FILE_TYPES.items():
            if extension in extensions:
                destination_folder = folder_name
                break

        if destination_folder:
            # create the folder if it doesn't exist yet
            folder_path =  os.path.join(TARGET_DIR, destination_folder)
            os.makedirs(folder_path, exist_ok=True)

            # move the file
            shutil.move(item_path, os.path.join(folder_path, item))
            moved_file_count += 1
            print(f"Moved: {item} -> {destination_folder}/")

    # generate an automated log file report
    write_log(moved_file_count)


def write_log(count):
    log_file = os.path.join(TARGET_DIR, 'cleanup_log.txt')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] Automation Run: Successfully organized {count} files.\n")
    print(f"Log updated at {log_file}. Run complete!")

if __name__ == "__main__":
    organize_folder()