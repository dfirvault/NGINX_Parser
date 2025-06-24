import os
import concurrent.futures
from threading import Lock
from pathlib import Path
import lzma

# Lock for thread-safe file operations
file_lock = Lock()

def process_file(filepath, log_type):
    """Read and return the content of a single file, supporting .xz files"""
    try:
        if filepath.endswith('.xz'):
            with lzma.open(filepath, 'rt', encoding='utf-8', errors='ignore') as f:
                return log_type, f.read()
        else:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return log_type, f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def combine_logs_in_folder(foldername, filenames, root_dir, output_dir):
    """Process all files in a single folder"""
    log_types = {
        'access': [],
        'error': [],
        'ssl': []
    }

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for filename in filenames:
            if filename.startswith('combined-'):
                continue

            lower_filename = filename.lower()

            # Determine log type by name (even for .xz files)
            if 'access' in lower_filename:
                log_type = 'access'
            elif 'error' in lower_filename:
                log_type = 'error'
            elif 'ssl' in lower_filename:
                log_type = 'ssl'
            else:
                continue

            filepath = os.path.join(foldername, filename)

            # Process both plain and .xz log files
            if filepath.endswith('.log') or filepath.endswith('.xz'):
                futures.append(executor.submit(process_file, filepath, log_type))

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                log_type, content = result
                log_types[log_type].append(content)

    rel_path = os.path.relpath(foldername, root_dir)
    output_folder = os.path.join(output_dir, rel_path)
    os.makedirs(output_folder, exist_ok=True)

    for log_type, contents in log_types.items():
        if contents:
            combined_filename = f"combined-{log_type}.log"
            combined_path = os.path.join(output_folder, combined_filename)
            try:
                with file_lock:
                    with open(combined_path, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(contents))
                print(f"Created {combined_filename} in {output_folder}")
            except Exception as e:
                print(f"Error writing {combined_path}: {e}")

def combine_log_files(root_dir, output_dir):
    """Recursively combine log files in all subdirectories"""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        folder_futures = []
        for foldername, subfolders, filenames in os.walk(root_dir):
            if not any(f for f in filenames if not f.startswith('combined-') and 
                      any(t in f.lower() for t in ['access', 'error', 'ssl']) and
                      (f.endswith('.log') or f.endswith('.xz'))):
                continue
            folder_futures.append(executor.submit(combine_logs_in_folder, foldername, filenames, root_dir, output_dir))

        for future in concurrent.futures.as_completed(folder_futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing folder: {e}")

if __name__ == '__main__':
    root_directory = input("Enter the root directory to process (or press Enter for current directory): ").strip()
    if not root_directory:
        root_directory = os.getcwd()

    if not os.path.isdir(root_directory):
        print(f"Error: Directory '{root_directory}' does not exist")
        exit(1)

    output_directory = input("Enter the output directory to save combined logs: ").strip()
    if not output_directory:
        print("No output directory provided.")
        exit(1)

    os.makedirs(output_directory, exist_ok=True)

    print(f"\nProcessing from: {root_directory}")
    print(f"Outputting combined logs to: {output_directory}\n")
    combine_log_files(root_directory, output_directory)
    print("\nProcessing complete!")
