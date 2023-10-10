import os
import sys

def rename_json_file(folder_path):
    # List the files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Filter for JSON files
    json_files = [f for f in files if f.endswith(".json")]

    if len(json_files) == 1:
        # Get the folder name
        folder_name = os.path.basename(folder_path)

        # Get the current file name
        current_file = json_files[0]

        # Define the new file name
        new_file_name = os.path.join(folder_path, folder_name + ".json")

        # Rename the file
        os.rename(os.path.join(folder_path, current_file), new_file_name)

        print(f"JSON file renamed to: {new_file_name}")
    elif len(json_files) == 0:
        print("No JSON files found in the folder.")
    else:
        print("Multiple JSON files found in the folder. Unable to proceed.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python rename_json_file.py folder_path")
        sys.exit(1)

    folder_path = sys.argv[1]
    rename_json_file(folder_path)
