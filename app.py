import os
import shutil   # high-level file operations, including copying and removing files and directories
import hashlib  # Allowing the program to generate file hashes to verify integrity. (MD5)
import time
import sys
import stat     # Contains constants and functions for interpreting and manipulating file permissions and modes (read-only files)
import logging  # Provides a flexible framework for emitting log messages from Python programs

"""
This script synchronizes source and replica folders, copying, updating, and removing
files and directories as needed. Synchronization runs in a continuous loop with a user-specified interval.
"""

def setup_logging(log_file: str) -> None:
    """Configures logging to record events to a file and the console."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )


def calculate_md5(file_path: str) -> str:
    """Calculates the MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
    except IOError as e:
        logging.error("Error reading file %s for MD5 calculation: %s", file_path, e)
        return ""
    return hash_md5.hexdigest()


def remove_readonly(file_path: str) -> None:
    """Removes the read-only attribute from a file to allow modifications."""
    os.chmod(file_path, stat.S_IWRITE)


def create_directory(replica_root: str) -> None:
    """Creates a directory at the specified path if it does not exist."""
    os.makedirs(replica_root, exist_ok=True)
    logging.info("Created directory: %s", replica_root)


def needs_update(src_file: str, replica_file: str) -> bool:
    """Checks if a file in the replica needs to be updated based on size or MD5 hash."""
    if os.path.getsize(src_file) != os.path.getsize(replica_file):
        return True
    return calculate_md5(src_file) != calculate_md5(replica_file)


def process_file(src_file: str, replica_file: str) -> None:
    """Copies or updates a file from the source to the replica."""
    try:
        if os.path.exists(replica_file):
            if needs_update(src_file, replica_file):
                if not os.access(replica_file, os.W_OK):
                    remove_readonly(replica_file)
                shutil.copyfile(src_file, replica_file)
                logging.info("Updated file: %s", replica_file)
        else:
            shutil.copyfile(src_file, replica_file)
            logging.info("Copied file: %s", replica_file)
    except Exception as e:
        logging.error("Failed to process file %s -> %s: %s", src_file, replica_file, e)


def remove_files(replica_folder: str, source_folder: str) -> None:
    """Removes files from the replica that no longer exist in the source."""
    for root, _, files in os.walk(replica_folder):
        relative_path = os.path.relpath(root, replica_folder)
        source_root = os.path.join(source_folder, relative_path)
        for file_name in files:
            replica_file = os.path.join(root, file_name)
            src_file = os.path.join(source_root, file_name)
            if not os.path.exists(src_file):
                try:
                    if not os.access(replica_file, os.W_OK):
                        remove_readonly(replica_file)
                    os.remove(replica_file)
                    logging.info("Deleted file: %s", replica_file)
                except Exception as e:
                    logging.error("Failed to delete file %s: %s", replica_file, e)


def remove_directories(replica_folder: str, source_folder: str) -> None:
    """Removes directories from the replica that no longer exist in the source."""
    for root, dirs, _ in os.walk(replica_folder):
        relative_path = os.path.relpath(root, replica_folder)
        source_root = os.path.join(source_folder, relative_path)
        for dir_name in dirs:
            replica_dir = os.path.join(root, dir_name)
            src_dir = os.path.join(source_root, dir_name)
            if not os.path.exists(src_dir):
                try:
                    shutil.rmtree(replica_dir)
                    logging.info("Deleted directory: %s", replica_dir)
                except Exception as e:
                    logging.error("Failed to delete directory %s: %s", replica_dir, e)


def sync_folders(source_folder: str, replica_folder: str) -> None:
    """Synchronizes files and directories from the source folder to the replica folder."""
    for root, _, files in os.walk(source_folder):
        relative_path = os.path.relpath(root, source_folder)
        replica_root = os.path.join(replica_folder, relative_path)
        if not os.path.exists(replica_root):
            create_directory(replica_root)
        for file_name in files:
            src_file = os.path.join(root, file_name)
            replica_file = os.path.join(replica_root, file_name)
            process_file(src_file, replica_file)
    remove_files(replica_folder, source_folder)
    remove_directories(replica_folder, source_folder)


def sync_loop(source_folder: str, replica_folder: str, sync_interval: int) -> None:
    """Continuously synchronizes the source and replica folders at a specified time interval."""
    while True:
        sync_folders(source_folder, replica_folder)
        time.sleep(sync_interval)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python app.py <source_folder> <replica_folder> <log_file> <sync_interval>")
        sys.exit(1)

    source_folder = sys.argv[1]
    replica_folder = sys.argv[2]
    log_file = sys.argv[3]
    sync_interval = int(sys.argv[4])

    setup_logging(log_file)
    sync_loop(source_folder, replica_folder, sync_interval)
