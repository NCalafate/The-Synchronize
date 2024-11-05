# [The-Synchronizer](https://github.com/NCalafate/The-Synchronize)
Program that synchronizes two folders: source and replica. [Link](https://github.com/NCalafate/The-Synchronize)

## Other Projects

Here are a few other projects I've developed that might be of interest:

- [Python API Restful](https://github.com/NCalafate/Python-API-Restful)
- [Python JSON-RPC Service](https://github.com/NCalafate/Python-JSON-RPC-Service)
- [Python Prime Number Checker](https://github.com/NCalafate/Python_PrimeNumber)

# Folder Synchronization Program

## Description

This program synchronizes two folders, `source` and `replica`, ensuring that the content of the `replica` folder is always an exact copy of the `source` folder. The synchronization process is one-way, meaning changes made to the `source` are propagated to the `replica`, but not vice-versa.

Synchronization is performed periodically, and the program logs all file operations (creation, update, deletion) to a specified log file as well as to the console output.

## Features

- **One-Way Synchronization**: Ensures `replica` matches `source` exactly, deleting files in `replica` that do not exist in `source`.
- **Logging**: Logs all file creation, copying, and deletion operations to a log file and the console.
- **Customizable Settings**: Accepts folder paths, synchronization interval, and log file path as command-line arguments.
- **Periodic Synchronization**: Synchronizes at a specified time interval.

## Usage

To run the program, use the following command:

```bash
python app.py <source_folder> <replica_folder> <log_file> <sync_interval>
``` 

## Code Structure

- **`setup_logging(log_file: str) -> None`**: Configures logging to record events to a file and the console.

- **`calculate_md5(file_path: str) -> str`**: Calculates the MD5 hash of a file for integrity check.

- **`remove_readonly(file_path: str) -> None`**: Removes the read-only attribute from a file to allow modifications.

- **`create_directory(replica_root: str) -> None`**: Creates a directory in the replica if it does not exist.

- **`needs_update(src_file: str, replica_file: str) -> bool`**: Checks if a replica file needs updating based on size or MD5 hash.

- **`process_file(src_file: str, replica_file: str) -> None`**: Copies or updates a file from the source to the replica.

- **`remove_files(replica_folder: str, source_folder: str) -> None`**: Removes files from the replica that do not exist in the source.

- **`remove_directories(replica_folder: str, source_folder: str) -> None`**: Removes directories from the replica that do not exist in the source.

- **`sync_folders(source_folder: str, replica_folder: str) -> None`**: Synchronizes content of the source folder with the replica folder.

- **`sync_loop(source_folder: str, replica_folder: str, sync_interval: int) -> None`**: Runs synchronization in a loop at specified intervals, with 'Q' to exit.










