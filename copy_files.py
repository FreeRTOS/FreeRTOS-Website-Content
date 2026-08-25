import shutil
import os
import fileinput
import re


def find_replace_in_files(directory, find_str, replace_str):
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)

                # Use fileinput for in-place replacement
                with fileinput.FileInput(file_path, inplace=True) as file:
                    for line in file:
                        modified_line = re.sub(
                            r"(\.\./)*" + find_str, replace_str, line
                        )
                        print(modified_line, end="")

        print(f"String '{find_str}' replaced with '{replace_str}' in all files.")
    except Exception as e:
        print(f"Error: {e}")


with open("output7") as f:
    for line in f.readlines():
        line = line.rstrip("\n")
        split = line.split("/")
        try:
            find_replace_in_files(
                "content/en-us/", line, f"/media/{split[2]}/{split[4]}"
            )
        except Exception:
            print(line)

with open("output7") as f:
    for line in f.readlines():
        line = line.rstrip("\n")
        split = line.split("/")
        try:
            target = f"content/media/{split[2]}/{split[4]}"
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.copy(f"content-restructure/{line}", target)
        except Exception:
            print(line)
