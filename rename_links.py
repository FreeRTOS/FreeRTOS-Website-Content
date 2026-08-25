import os
import fileinput
import re
import json


def find_replace_in_files(directory, name_mapping):
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)

                # Use fileinput for in-place replacement
                with fileinput.FileInput(file_path, inplace=True) as file:
                    slashes = r"((\.\./)*|/)"
                    endings = "(.html|.md)?"
                    for line in file:
                        for old_name, new_name in name_mapping.items():
                            line = re.sub(
                                f"\({slashes}{old_name}{endings}\)",
                                f"({new_name})",
                                line,
                            )
                        print(line, end="")
    except Exception as e:
        print(f"Error: {e}")


with open("rename_links.json") as f:
    name_mapping = json.load(f)
    find_replace_in_files("content/en-us/", name_mapping)
