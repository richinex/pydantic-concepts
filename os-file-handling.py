Certainly! I'll provide you with 20 advanced examples of using Python for file and directory operations, including recursive searches, renaming, and more. I'll use inline comments to explain each example in detail.

    Recursive search for files with a specific extension:

python

import os

def find_files_with_extension(root_dir, extension):
    for root, dirs, files in os.walk(root_dir):  # Walk through directory tree
        for file in files:
            if file.endswith(extension):  # Check if file has the desired extension
                yield os.path.join(root, file)  # Yield full path of matching file

# Example usage
for file_path in find_files_with_extension("/path/to/search", ".txt"):
    print(file_path)

    Rename files based on a pattern:

python

import os
import re

def rename_files_with_pattern(directory, pattern, replacement):
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            new_name = re.sub(pattern, replacement, filename)  # Replace pattern in filename
            if new_name != filename:
                os.rename(os.path.join(directory, filename),
                          os.path.join(directory, new_name))
                print(f"Renamed: {filename} -> {new_name}")

# Example usage
rename_files_with_pattern("/path/to/directory", r"(\d{4})_(\d{2})_(\d{2})", r"\3-\2-\1")

    Find duplicate files based on content:

python

import os
import hashlib

def find_duplicates(directory):
    hash_dict = {}
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_hash = hashlib.md5(open(filepath, 'rb').read()).hexdigest()  # Calculate file hash
            if file_hash in hash_dict:
                hash_dict[file_hash].append(filepath)
            else:
                hash_dict[file_hash] = [filepath]
    
    return {k: v for k, v in hash_dict.items() if len(v) > 1}  # Return only duplicates

# Example usage
duplicates = find_duplicates("/path/to/search")
for hash_value, file_list in duplicates.items():
    print(f"Duplicate files (hash: {hash_value}):")
    for file in file_list:
        print(f"  {file}")

    Move files older than a certain date:

python

import os
import shutil
from datetime import datetime, timedelta

def move_old_files(source_dir, destination_dir, days_old):
    cutoff_date = datetime.now() - timedelta(days=days_old)
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if datetime.fromtimestamp(os.path.getmtime(file_path)) < cutoff_date:
                relative_path = os.path.relpath(root, source_dir)
                dest_path = os.path.join(destination_dir, relative_path)
                os.makedirs(dest_path, exist_ok=True)
                shutil.move(file_path, os.path.join(dest_path, file))
                print(f"Moved: {file_path} -> {os.path.join(dest_path, file)}")

# Example usage
move_old_files("/path/to/source", "/path/to/destination", 30)

    Create a directory structure based on file extensions:

python

import os
import shutil

def organize_by_extension(source_dir):
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1][1:]  # Get extension without dot
            if file_extension:
                dest_dir = os.path.join(source_dir, file_extension)
                os.makedirs(dest_dir, exist_ok=True)
                shutil.move(file_path, os.path.join(dest_dir, file))
                print(f"Moved: {file_path} -> {os.path.join(dest_dir, file)}")

# Example usage
organize_by_extension("/path/to/organize")

    Find and delete empty directories:

python

import os

def delete_empty_dirs(directory):
    for root, dirs, files in os.walk(directory, topdown=False):  # Walk bottom-up
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):  # Check if directory is empty
                os.rmdir(dir_path)
                print(f"Deleted empty directory: {dir_path}")

# Example usage
delete_empty_dirs("/path/to/clean")

    Batch rename files with incrementing numbers:

python

import os

def batch_rename(directory, prefix, start_num=1, padding=3):
    files = sorted(os.listdir(directory))
    for i, filename in enumerate(files, start=start_num):
        file_extension = os.path.splitext(filename)[1]
        new_name = f"{prefix}{str(i).zfill(padding)}{file_extension}"
        os.rename(os.path.join(directory, filename),
                  os.path.join(directory, new_name))
        print(f"Renamed: {filename} -> {new_name}")

# Example usage
batch_rename("/path/to/rename", "file_", start_num=1, padding=3)

    Search for files containing specific text:

python

import os

def search_file_content(directory, search_text):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    if search_text in f.read():
                        yield file_path
            except (IOError, UnicodeDecodeError):
                pass  # Skip files that can't be read or aren't text

# Example usage
for file_path in search_file_content("/path/to/search", "specific text"):
    print(f"Found in: {file_path}")

    Create a zip archive of a directory:

python

import os
import zipfile

def zip_directory(directory, zip_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, directory)
                zipf.write(file_path, arcname)
                print(f"Added to zip: {file_path}")

# Example usage
zip_directory("/path/to/directory", "archive.zip")

    Find the largest files in a directory:

python

import os
import heapq

def find_largest_files(directory, n=10):
    file_sizes = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            heapq.heappush(file_sizes, (-file_size, file_path))  # Use negative size for max-heap

    return [heapq.heappop(file_sizes) for _ in range(min(n, len(file_sizes)))]

# Example usage
for size, path in find_largest_files("/path/to/search", n=5):
    print(f"{path}: {-size / 1024 / 1024:.2f} MB")

    Recursively change file permissions:

python

import os

def change_permissions(directory, mode):
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            os.chmod(os.path.join(root, dir_name), mode)
        for file_name in files:
            os.chmod(os.path.join(root, file_name), mode)
            print(f"Changed permissions for: {os.path.join(root, file_name)}")

# Example usage (set read and execute permissions for owner, group, and others)
change_permissions("/path/to/directory", 0o755)

    Find and replace text in multiple files:

python

import os
import fileinput

def find_replace_in_files(directory, find_text, replace_text, file_pattern="*"):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if fnmatch.fnmatch(file, file_pattern):
                file_path = os.path.join(root, file)
                with fileinput.input(files=(file_path,), inplace=True) as f:
                    for line in f:
                        print(line.replace(find_text, replace_text), end='')
                print(f"Processed: {file_path}")

# Example usage
find_replace_in_files("/path/to/search", "old_text", "new_text", "*.txt")

    Create a file tree structure:

python

import os

def print_directory_tree(directory):
    def print_tree(dir_path, prefix=""):
        contents = os.listdir(dir_path)
        pointers = ["├── " if i < len(contents) - 1 else "└── " for i in range(len(contents))]
        for pointer, name in zip(pointers, contents):
            print(f"{prefix}{pointer}{name}")
            full_path = os.path.join(dir_path, name)
            if os.path.isdir(full_path):
                extension = "│   " if pointer == "├── " else "    "
                print_tree(full_path, prefix + extension)

    print(f"Directory tree of {directory}:")
    print_tree(directory)

# Example usage
print_directory_tree("/path/to/directory")

    Batch convert file encodings:

python

import os
import codecs

def convert_file_encoding(file_path, source_encoding, target_encoding):
    with codecs.open(file_path, 'r', source_encoding) as source_file:
        content = source_file.read()
    
    with codecs.open(file_path, 'w', target_encoding) as target_file:
        target_file.write(content)

def batch_convert_encoding(directory, source_encoding, target_encoding, file_pattern="*.txt"):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if fnmatch.fnmatch(file, file_pattern):
                file_path = os.path.join(root, file)
                convert_file_encoding(file_path, source_encoding, target_encoding)
                print(f"Converted: {file_path}")

# Example usage
batch_convert_encoding("/path/to/convert", "utf-8", "ascii", "*.txt")

    Find files modified within a date range:

python

import os
from datetime import datetime

def find_files_by_date_range(directory, start_date, end_date):
    start_timestamp = start_date.timestamp()
    end_timestamp = end_date.timestamp()
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            mod_time = os.path.getmtime(file_path)
            if start_timestamp <= mod_time <= end_timestamp:
                yield file_path

# Example usage
start = datetime(2023, 1, 1)
end = datetime(2023, 12, 31)
for file_path in find_files_by_date_range("/path/to/search", start, end):
    print(f"Found: {file_path}")

    Create a backup of files with a timestamp:

python

import os
import shutil
from datetime import datetime

def backup_files(source_dir, backup_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_root = os.path.join(backup_dir, f"backup_{timestamp}")
    
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, source_dir)
            dst_path = os.path.join(backup_root, rel_path)
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)  # Copy with metadata
            print(f"Backed up: {src_path} -> {dst_path}")

# Example usage
backup_files("/path/to/source", "/path/to/backups")

    Remove duplicate lines from text files:

python

import os

def remove_duplicate_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    unique_lines = list(dict.fromkeys(lines))  # Remove duplicates while preserving order
    
    with open(file_path, 'w') as file:
        file.writelines(unique_lines)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                remove_duplicate_lines(file_path)
                print(f"Processed: {file_path}")

# Example usage
process_directory("/path/to/process")

    Generate a CSV report of file sizes:

python

import os
import csv

def generate_file_size_report(directory, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File Path', 'Size (bytes)'])
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                writer.writerow([file_path, file_size])
                print(f"Added to report: {file_path}")

# Example usage
generate_file_size_report("/path/to/analyze", "file_sizes.csv")

    Synchronize two directories:

python

import os
import shutil
import filecmp

def sync_directories(source_dir, target_dir):
    dcmp = filecmp.dircmp(source_dir, target_dir)
    
    # Copy files that don't exist in the target directory
    for file in dcmp.left_only:
        src_path = os.path.join(source_dir, file)
        dst_path = os.path.join(target_dir, file)
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)
            print(f"Copied: {src_path} -> {dst_path}")
        elif os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)
            print(f"Copied directory: {src_path} -> {dst_path}")
    
    # Update files that are different
    for file in dcmp.diff_files:
        src_path = os.path.join(source_dir, file)
        dst_path = os.path.join(target_dir, file)
        shutil.copy2(src_path, dst_path)
        print(f"Updated: {dst_path}")
    
    # Recursively sync subdirectories
    for subdir in dcmp.common_dirs:

Claude’s response was limited as it hit the maximum length allowed at this time. Claude does not have the ability to run the code it generates yet.
R

continue

Certainly! I'll continue with the remaining examples.

    Synchronize two directories (continued):

python

    # Recursively sync subdirectories
    for subdir in dcmp.common_dirs:
        sync_directories(os.path.join(source_dir, subdir),
                         os.path.join(target_dir, subdir))

# Example usage
sync_directories("/path/to/source", "/path/to/target")

    Find and delete files with specific patterns in their names:

python

import os
import re

def delete_files_by_pattern(directory, pattern):
    compiled_pattern = re.compile(pattern)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if compiled_pattern.search(file):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Deleted: {file_path}")

# Example usage (delete all temporary files ending with .tmp)
delete_files_by_pattern("/path/to/clean", r"\.tmp$")

These examples demonstrate advanced ways to use Python for file and directory operations. Here's a brief explanation of some key concepts used:

    os.walk(): This function is used to recursively traverse directory trees. It yields a tuple containing the current directory path, a list of subdirectories, and a list of files in the current directory.
    os.path module: This module provides functions for working with file paths, such as join(), splitext(), relpath(), etc.
    shutil module: This module offers high-level operations on files and collections of files, including functions like copy2(), move(), and copytree().
    re module: This module provides support for regular expressions, which are powerful tools for pattern matching and text manipulation.
    Generators: Some functions use yield to create generators, which are memory-efficient for processing large amounts of data.
    Context managers: The with statement is used to ensure proper handling of file operations, automatically closing files after use.
    List comprehensions and dictionary comprehensions: These provide concise ways to create lists and dictionaries based on existing data.
    Lambda functions: These are used for simple, one-line functions, often in sorting operations.

These examples cover a wide range of file and directory operations, including:

    Recursive searching
    File renaming and moving
    Finding duplicates
    Organizing files
    Creating archives
    Modifying file permissions
    Text processing
    File encoding conversion
    Date-based file operations
    Backup creation
    Directory synchronization
    File size reporting

When working with these scripts, always be cautious, especially when deleting or modifying files. It's a good practice to test your scripts on a small, non-critical set of files before running them on important data. Additionally, consider adding error handling and logging to make your scripts more robust and easier to debug.

Would you like me to explain any of these examples in more detail or provide additional information on any specific file handling concept?
Claude does not have the ability to run the code it generates yet.
R

good now lets do the same with Pathlib add more detailed comment explanations

Certainly! I'll provide you with 20 advanced examples using the pathlib module, which offers an object-oriented interface for working with file paths. I'll include detailed inline comments to explain each example.

    Recursive search for files with a specific extension:

python

from pathlib import Path

def find_files_with_extension(root_dir: str, extension: str):
    root_path = Path(root_dir)  # Convert string path to Path object
    # Use glob to recursively search for files with the given extension
    for file_path in root_path.rglob(f"*{extension}"):
        if file_path.is_file():  # Ensure it's a file, not a directory
            yield file_path  # Yield the Path object of the matching file

# Example usage
for file_path in find_files_with_extension("/path/to/search", ".txt"):
    print(file_path)

    Rename files based on a pattern:

python

from pathlib import Path
import re

def rename_files_with_pattern(directory: str, pattern: str, replacement: str):
    dir_path = Path(directory)
    for file_path in dir_path.iterdir():  # Iterate over directory contents
        if file_path.is_file():  # Check if it's a file
            new_name = re.sub(pattern, replacement, file_path.name)  # Apply regex substitution
            if new_name != file_path.name:
                new_path = file_path.with_name(new_name)  # Create new path with new name
                file_path.rename(new_path)  # Rename the file
                print(f"Renamed: {file_path.name} -> {new_name}")

# Example usage: Change date format from YYYY_MM_DD to DD-MM-YYYY
rename_files_with_pattern("/path/to/directory", r"(\d{4})_(\d{2})_(\d{2})", r"\3-\2-\1")

    Find duplicate files based on content:

python

from pathlib import Path
import hashlib

def find_duplicates(directory: str):
    dir_path = Path(directory)
    hash_dict = {}
    for file_path in dir_path.rglob("*"):  # Recursively iterate over all files
        if file_path.is_file():
            file_hash = hashlib.md5(file_path.read_bytes()).hexdigest()  # Calculate MD5 hash
            if file_hash in hash_dict:
                hash_dict[file_hash].append(str(file_path))
            else:
                hash_dict[file_hash] = [str(file_path)]
    
    return {k: v for k, v in hash_dict.items() if len(v) > 1}  # Return only duplicates

# Example usage
duplicates = find_duplicates("/path/to/search")
for hash_value, file_list in duplicates.items():
    print(f"Duplicate files (hash: {hash_value}):")
    for file in file_list:
        print(f"  {file}")

    Move files older than a certain date:

python

from pathlib import Path
import shutil
from datetime import datetime, timedelta

def move_old_files(source_dir: str, destination_dir: str, days_old: int):
    source_path = Path(source_dir)
    dest_path = Path(destination_dir)
    cutoff_date = datetime.now() - timedelta(days=days_old)
    
    for file_path in source_path.rglob("*"):  # Recursively iterate over all files
        if file_path.is_file() and file_path.stat().st_mtime < cutoff_date.timestamp():
            relative_path = file_path.relative_to(source_path)  # Get relative path
            new_path = dest_path / relative_path  # Construct new path
            new_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure destination directory exists
            shutil.move(str(file_path), str(new_path))  # Move the file
            print(f"Moved: {file_path} -> {new_path}")

# Example usage
move_old_files("/path/to/source", "/path/to/destination", 30)

    Create a directory structure based on file extensions:

python

from pathlib import Path
import shutil

def organize_by_extension(source_dir: str):
    source_path = Path(source_dir)
    for file_path in source_path.rglob("*"):  # Recursively iterate over all files
        if file_path.is_file():
            extension = file_path.suffix[1:]  # Get extension without dot
            if extension:
                dest_dir = source_path / extension  # Create Path for destination directory
                dest_dir.mkdir(exist_ok=True)  # Create destination directory if it doesn't exist
                new_path = dest_dir / file_path.name  # Construct new file path
                shutil.move(str(file_path), str(new_path))  # Move the file
                print(f"Moved: {file_path} -> {new_path}")

# Example usage
organize_by_extension("/path/to/organize")

    Find and delete empty directories:

python

from pathlib import Path

def delete_empty_dirs(directory: str):
    dir_path = Path(directory)
    for path in sorted(dir_path.rglob("*"), key=lambda x: len(str(x)), reverse=True):
        if path.is_dir() and not any(path.iterdir()):  # Check if directory is empty
            path.rmdir()  # Remove empty directory
            print(f"Deleted empty directory: {path}")

# Example usage
delete_empty_dirs("/path/to/clean")

    Batch rename files with incrementing numbers:

python

from pathlib import Path

def batch_rename(directory: str, prefix: str, start_num: int = 1, padding: int = 3):
    dir_path = Path(directory)
    files = sorted(dir_path.iterdir())  # Get sorted list of directory contents
    for i, file_path in enumerate(files, start=start_num):
        if file_path.is_file():
            new_name = f"{prefix}{str(i).zfill(padding)}{file_path.suffix}"
            new_path = file_path.with_name(new_name)
            file_path.rename(new_path)
            print(f"Renamed: {file_path.name} -> {new_name}")

# Example usage
batch_rename("/path/to/rename", "file_", start_num=1, padding=3)

    Search for files containing specific text:

python

from pathlib import Path

def search_file_content(directory: str, search_text: str):
    dir_path = Path(directory)
    for file_path in dir_path.rglob("*"):  # Recursively iterate over all files
        if file_path.is_file():
            try:
                content = file_path.read_text(encoding='utf-8')  # Read file content
                if search_text in content:
                    yield file_path
            except (IOError, UnicodeDecodeError):
                pass  # Skip files that can't be read or aren't text

# Example usage
for file_path in search_file_content("/path/to/search", "specific text"):
    print(f"Found in: {file_path}")

    Create a zip archive of a directory:

python

from pathlib import Path
import zipfile

def zip_directory(directory: str, zip_name: str):
    dir_path = Path(directory)
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in dir_path.rglob("*"):  # Recursively iterate over all files
            if file_path.is_file():
                arcname = file_path.relative_to(dir_path)  # Get relative path for archive
                zipf.write(file_path, arcname)
                print(f"Added to zip: {file_path}")

# Example usage
zip_directory("/path/to/directory", "archive.zip")

    Find the largest files in a directory:

python

from pathlib import Path
import heapq

def find_largest_files(directory: str, n: int = 10):
    dir_path = Path(directory)
    file_sizes = []
    for file_path in dir_path.rglob("*"):  # Recursively iterate over all files
        if file_path.is_file():
            file_size = file_path.stat().st_size
            heapq.heappush(file_sizes, (-file_size, str(file_path)))  # Use negative size for max-heap

    return [heapq.heappop(file_sizes) for _ in range(min(n, len(file_sizes)))]

# Example usage
for size, path in find_largest_files("/path/to/search", n=5):
    print(f"{path}: {-size / 1024 / 1024:.2f} MB")

I'll continue with the remaining examples in the next response.
Claude does not have the ability to run the code it generates yet.
R

continue

Certainly! I'll continue with the remaining examples using the pathlib module.

    Recursively change file permissions:

python

from pathlib import Path

def change_permissions(directory: str, mode: int):
    dir_path = Path(directory)
    for path in dir_path.rglob("*"):  # Recursively iterate over all files and directories
        path.chmod(mode)  # Change permissions
        print(f"Changed permissions for: {path}")

# Example usage (set read and execute permissions for owner, group, and others)
change_permissions("/path/to/directory", 0o755)

    Find and replace text in multiple files:

python

from pathlib import Path
import re

def find_replace_in_files(directory: str, find_text: str, replace_text: str, file_pattern: str = "*"):
    dir_path = Path(directory)
    for file_path in dir_path.rglob(file_pattern):  # Recursively find files matching the pattern
        if file_path.is_file():
            content = file_path.read_text()  # Read file content
            new_content = re.sub(find_text, replace_text, content)  # Replace text
            if new_content != content:
                file_path.write_text(new_content)  # Write updated content back to file
                print(f"Processed: {file_path}")

# Example usage
find_replace_in_files("/path/to/search", "old_text", "new_text", "*.txt")

    Create a file tree structure:

python

from pathlib import Path

def print_directory_tree(directory: str):
    dir_path = Path(directory)
    
    def print_tree(path: Path, prefix: str = ""):
        entries = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name))
        entries_count = len(entries)
        for i, entry in enumerate(entries):
            connector = "├── " if i < entries_count - 1 else "└── "
            print(f"{prefix}{connector}{entry.name}")
            if entry.is_dir():
                extension = "│   " if i < entries_count - 1 else "    "
                print_tree(entry, prefix + extension)

    print(f"Directory tree of {dir_path}:")
    print_tree(dir_path)

# Example usage
print_directory_tree("/path/to/directory")

    Batch convert file encodings:

python

from pathlib import Path
import codecs

def convert_file_encoding(file_path: Path, source_encoding: str, target_encoding: str):
    content = file_path.read_text(encoding=source_encoding)
    file_path.write_text(content, encoding=target_encoding)

def batch_convert_encoding(directory: str, source_encoding: str, target_encoding: str, file_pattern: str = "*.txt"):
    dir_path = Path(directory)
    for file_path in dir_path.rglob(file_pattern):  # Recursively find files matching the pattern
        if file_path.is_file():
            convert_file_encoding(file_path, source_encoding, target_encoding)
            print(f"Converted: {file_path}")

# Example usage
batch_convert_encoding("/path/to/convert", "utf-8", "ascii", "*.txt")

    Find files modified within a date range:

python

from pathlib import Path
from datetime import datetime

def find_files_by_date_range(directory: str, start_date: datetime, end_date: datetime):
    dir_path = Path(directory)
    start_timestamp = start_date.timestamp()
    end_timestamp = end_date.timestamp()
    
    for file_path in dir_path.rglob("*"):  # Recursively iterate over all files
        if file_path.is_file():
            mod_time = file_path.stat().st_mtime
            if start_timestamp <= mod_time <= end_timestamp:
                yield file_path

# Example usage
start = datetime(2023, 1, 1)
end = datetime(2023, 12, 31)
for file_path in find_files_by_date_range("/path/to/search", start, end):
    print(f"Found: {file_path}")

    Create a backup of files with a timestamp:

python

from pathlib import Path
import shutil
from datetime import datetime

def backup_files(source_dir: str, backup_dir: str):
    source_path = Path(source_dir)
    backup_path = Path(backup_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_root = backup_path / f"backup_{timestamp}"
    
    for file_path in source_path.rglob("*"):  # Recursively iterate over all files
        if file_path.is_file():
            rel_path = file_path.relative_to(source_path)
            dst_path = backup_root / rel_path
            dst_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure destination directory exists
            shutil.copy2(file_path, dst_path)  # Copy with metadata
            print(f"Backed up: {file_path} -> {dst_path}")

# Example usage
backup_files("/path/to/source", "/path/to/backups")

    Remove duplicate lines from text files:

python

from pathlib import Path

def remove_duplicate_lines(file_path: Path):
    lines = file_path.read_text().splitlines()
    unique_lines = list(dict.fromkeys(lines))  # Remove duplicates while preserving order
    file_path.write_text("\n".join(unique_lines) + "\n")

def process_directory(directory: str):
    dir_path = Path(directory)
    for file_path in dir_path.rglob("*.txt"):  # Recursively find all .txt files
        if file_path.is_file():
            remove_duplicate_lines(file_path)
            print(f"Processed: {file_path}")

# Example usage
process_directory("/path/to/process")

    Generate a CSV report of file sizes:

python

from pathlib import Path
import csv

def generate_file_size_report(directory: str, output_file: str):
    dir_path = Path(directory)
    output_path = Path(output_file)
    
    with output_path.open('w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File Path', 'Size (bytes)'])
        
        for file_path in dir_path.rglob("*"):  # Recursively iterate over all files
            if file_path.is_file():
                writer.writerow([str(file_path), file_path.stat().st_size])
                print(f"Added to report: {file_path}")

# Example usage
generate_file_size_report("/path/to/analyze", "file_sizes.csv")

    Synchronize two directories:

python

from pathlib import Path
import shutil
import filecmp

def sync_directories(source_dir: str, target_dir: str):
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    def sync(src: Path, dst: Path):
        if src.is_file():
            if not dst.exists() or not filecmp.cmp(str(src), str(dst)):
                shutil.copy2(str(src), str(dst))
                print(f"Copied: {src} -> {dst}")
        elif src.is_dir():
            if not dst.exists():
                dst.mkdir(parents=True)
                print(f"Created directory: {dst}")
            for item in src.iterdir():
                sync(item, dst / item.name)
    
    sync(source_path, target_path)

# Example usage
sync_directories("/path/to/source", "/path/to/target")

    Find and delete files with specific patterns in their names:

python

from pathlib import Path
import re

def delete_files_by_pattern(directory: str, pattern: str):
    dir_path = Path(directory)
    compiled_pattern = re.compile(pattern)
    for file_path in dir_path.rglob("*"):  # Recursively iterate over all files
        if file_path.is_file() and compiled_pattern.search(file_path.name):
            file_path.unlink()  # Delete the file
            print(f"Deleted: {file_path}")

# Example usage (delete all temporary files ending with .tmp)
delete_files_by_pattern("/path/to/clean", r"\.tmp$")

These examples demonstrate how to use the pathlib module for advanced file and directory operations. The pathlib module provides an object-oriented interface for working with file paths, which often results in more readable and maintainable code compared to the older os and os.path modules.

Key benefits of using pathlib include:

    Cross-platform compatibility: pathlib handles path separators correctly across different operating systems.
    Method chaining: You can perform multiple operations on paths using method chaining.
    Powerful path manipulation: pathlib provides methods for common path operations like joining, resolving, and getting parent directories.
    File operations: Many file operations can be performed directly on Path objects.
    Improved readability: pathlib often leads to more intuitive and readable code.

When using these scripts, always exercise caution, especially when deleting or modifying files. It's a good practice to test your scripts on a small, non-critical set of files before running them on important data. Additionally, consider adding error handling and logging to make your scripts more robust and easier to debug.
Claude does not have the ability to run the code it generates yet.
Claude can make mistakes. Please double-check responses.



