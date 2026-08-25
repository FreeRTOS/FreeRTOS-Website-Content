import filecmp
import os
from datetime import date
from pprint import pprint

def get_files_and_folders(path):
    files_and_folders = []
    for root, dirs, files in os.walk(path):
        for file in files:
            files_and_folders.append(os.path.join(root, file))
        for folder in dirs:
            files_and_folders.append(os.path.join(root, folder))
    return files_and_folders

def compare_folders(folderA, folderB):
    comparison = filecmp.dircmp(folderA, folderB)
    
    # Files only in folderA
    only_in_A = comparison.left_only
    # for file in comparison.left_only:
    #   path = os.path.join(folderA, file)
    #   if os.path.isdir(path):
    #     only_in_A.extend(get_files_and_folders(path))
    
    # Files only in folderB
    only_in_B = comparison.right_only
    # only_in_B.extend(get_files_and_folders(only_in_B))
    
    # Files with differences
    diff_files = comparison.diff_files
    
    # Recursive comparison for subdirectories
    for subfolder in comparison.common_dirs:
        subfolderA = os.path.join(folderA, subfolder)
        subfolderB = os.path.join(folderB, subfolder)
        subfolder_diff = compare_folders(subfolderA, subfolderB)
        only_in_A.extend([os.path.join(subfolder, f) for f in subfolder_diff[0]])
        only_in_B.extend([os.path.join(subfolder, f) for f in subfolder_diff[1]])
        diff_files.extend([os.path.join(subfolder, f) for f in subfolder_diff[2]])
    
    return only_in_A, only_in_B, diff_files

# Replace 'folderA' and 'folderB' with your directory paths
folderA = './content'
folderB = './content-restructure'

only_in_A, only_in_B, diff_files = compare_folders(folderA, folderB)

# Generate diff report
with open(f'diff_report_{date.today()}.txt', 'w') as f:
    f.write('==========================================================\n')
    f.write(f'{len(only_in_A)} Files only in {folderA}:\n')
    for file in only_in_A:
      f.write(f"{file}\n")

    f.write('\n\n\n==========================================================\n')

    f.write(f'{len(only_in_B)} Files only in {folderB}:\n')
    for file in only_in_B:
      f.write(f"{file}\n")

    f.write('\n\n\n==========================================================\n')
    f.write(f'{len(diff_files)} Files with differences between {folderA} and {folderB}:\n')
    for file in diff_files:
      f.write(f"{file}\n")
