#!/usr/bin/env python3
import re
import os
import logging
import argparse
import json
import requests
import csv

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

parser = argparse.ArgumentParser(
    prog="check_links.py",
    description="Check and fix links in markdown files"
)

parser.add_argument('-f', '--fix', action='store_true', help="Specify this option to attempt to fix broken links using built in heuristics.")
parser.add_argument('--external', action='store_true', help="Specify this flag to test external URLs")
parser.add_argument('--csv', help="Path to store a CSV containing broken links detected.")
parser.add_argument('--directory', help="Directory to search for links in.")
parser.add_argument("files", nargs="*", help="File to check")

args = parser.parse_args()

WEB_BROWSER_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

external_link_cache: dict[str,int] = dict()
def check_external_link(url: str) -> int:
    # recall from cache if already checked
    if url in external_link_cache:
        status_code = external_link_cache[url]
    else:
        headers = {
            "User-Agent": WEB_BROWSER_USER_AGENT
        }
        try:
            response = requests.get(url, headers=headers, timeout=(10,10))
        except:
            response = None

        status_code = 404
        if response:
            status_code = response.status_code

        # Save in cache
        external_link_cache[url] = status_code
    return status_code

def generate_file_path_set(directory):
    paths = set()
    file_name_count_dict = dict()
    file_name_path_dict = dict()
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith(".md"):
                paths.add(file_path)
                if file not in file_name_count_dict:
                    file_name_count_dict[file] = 1
                    file_name_path_dict[file] = file_path
                else:
                    file_name_count_dict[file] = file_name_count_dict[file] + 1

    unique_file_name_path_dict = dict()

    for name,count in file_name_count_dict.items():
        if count == 1:
            unique_file_name_path_dict[name] = file_name_path_dict[name]

    return paths, unique_file_name_path_dict

with open('rename_links.json', 'r') as f:
    renames_dict = json.load(f)

directory = args.directory

if not os.path.isdir(args.directory):
    print("Specified directory: {} does not exist".format(args.directory))
    exit(1)

paths, unique_names_dict = generate_file_path_set(directory)
md_link_regex = re.compile(r"\[(?P<text>[^\]]+)\]\((?P<target>[^)#]+)/?(?P<anchor>#[^#]+)?\)(?P<post>[^)])")

broken_links: list[dict[str,str]] = list()

def check_file(file_path: str):
    lines = []
    modified = False
    new_lines = []
    relative_path = os.path.relpath(file_path, directory)
    with open(file_path, 'r') as file:
        logger.info("Checking file: {}".format(relative_path))
        lines = file.readlines()
        new_lines = []
        for line in lines:
            new_line = line
            for m in md_link_regex.finditer(line):
                matched_data = m.group(0)
                groups = m.groupdict()
                text = m.group('text')
                target = m.group('target')
                anchor = m.group('anchor')
                post = m.group('post')
                if not anchor:
                    anchor = ""

                new_target = None

                if target.endswith("/"):
                    target = target[:-1]

                target_file_name = os.path.split(target)[1]
                if target == "":
                    pass
                elif target.startswith("mailto:"):
                    logger.info("Ignoring mailto link: {}".format(target))
                elif target.startswith("http://") or target.startswith("https://"):
                    if args.external:
                        logger.info("Checking external link: {}".format(target))
                        status_code = check_external_link(target)
                        if status_code != 200:
                            print("Bad external link in file: {}, target: {}, status_code: {}".format(relative_path, target, status_code))
                            broken_links.append({
                                "target_file_name": target_file_name,
                                "target": target,
                                "resolved_target": target,
                                "type": "external",
                                "file": relative_path
                            })

                elif target.startswith("/"):
                    if target.endswith(".md"):
                        target = target.replace(".md","")
                        new_target = target
                    elif target.endswith(".html"):
                        target = target.replace(".html","")
                        new_target = target
                    # Handle site-root relative links
                    logger.info("Checking site-root relative link: {}".format(target))
                    if target.endswith(".png") or target.endswith(".jpg") or "/media/" in target:
                        resolved_target = os.path.join("content", target[1:])
                        if os.access(resolved_target, os.R_OK) == False:
                            print("Bad site-relative link in file: {}, target: {}, resolved target: {}".format(relative_path, target, resolved_target))
                            broken_links.append({
                                "target_file_name": target_file_name,
                                "target": target,
                                "resolved_target": resolved_target,
                                "type": "site-relative",
                                "file": relative_path
                            })
                    else:
                        resolved_target = os.path.join(directory, target[1:]) + ".md"
                        if os.access(resolved_target, os.R_OK) == False:
                            print("Bad site-relative link in file: {}, target: {}, resolved target: {}".format(relative_path, target, resolved_target))
                            broken_links.append({
                                "target_file_name": target_file_name,
                                "target": target,
                                "resolved_target": resolved_target,
                                "type": "site-relative",
                                "file": relative_path
                            })
                            if target_file_name + ".md" in unique_names_dict:
                                print("Potential Fix: {} -> {}".format(target, unique_names_dict[target_file_name + ".md"]))
                                new_target = unique_names_dict[target_file_name + ".md"].replace(directory, "").replace(".md", "")
                            elif target_file_name in renames_dict:
                                print("Potential Fix: {} -> {}".format(target, renames_dict[target_file_name]))
                                new_target = renames_dict[target_file_name]
                            else:
                                for key in unique_names_dict.keys():
                                    if key.lower().endswith(target_file_name.lower() + ".md"):
                                        print("Potential Fix: {} -> {}".format(target, unique_names_dict[key]))
                                        new_target = unique_names_dict[key].replace(directory, "").replace(".md", "")
                                        break
                else:
                    if target.endswith(".md"):
                        target = target.replace(".md","")
                        new_target = target
                    elif target.endswith(".html"):
                        target = target.replace(".html","")
                        new_target = target
                    # Handle relative links
                    logger.info("Checking file-relative link: {}".format(target))
                    resolved_target = os.path.join(os.path.dirname(file_path), target) + ".md"
                    if os.access(resolved_target, os.R_OK) == False:
                        print("Bad file-relative link in file: {}, target: {}, resolved target: {}".format(relative_path, target, resolved_target))
                        broken_links.append({
                                "target_file_name": target_file_name,
                                "target": target,
                                "resolved_target": resolved_target,
                                "type": "file-relative",
                                "file": relative_path
                            })
                        if target_file_name + ".md" in unique_names_dict:
                            print("Potential Fix: {} -> {}".format(target, unique_names_dict[target_file_name + ".md"]))
                            new_target = unique_names_dict[target_file_name + ".md"].replace(directory, "").replace(".md", "")
                        elif target_file_name in renames_dict:
                                print("Potential Fix: {} -> {}".format(target, renames_dict[target_file_name]))
                                new_target = renames_dict[target_file_name]
                        else:
                            for key in unique_names_dict.keys():
                                if key.lower().endswith(target_file_name.lower() + ".md"):
                                    print("Potential Fix: {} -> {}".format(target, unique_names_dict[key]))
                                    new_target = unique_names_dict[key].replace(directory, "").replace(".md", "")
                                    break
                if new_target:
                    new_line = new_line.replace(matched_data, f"[{text}]({new_target}{anchor}){post}")
                    modified = True

            new_lines.append(new_line)
        file.close()

    if args.fix and modified:
        with open(file_path, 'w') as file:
            file.writelines(new_lines)
            file.close()

if not args.files:
    for file_path in paths:
        check_file(file_path)
else:
    for file_path in args.files:
        check_file(file_path)

target_file_names_count: dict[str,int] = dict()
for link in broken_links:
    if link["target_file_name"] not in target_file_names_count:
        target_file_names_count[link["target_file_name"]] = 1
    else:
        target_file_names_count[link["target_file_name"]] = target_file_names_count[link["target_file_name"]] + 1

broken_links_with_stats: list[dict] = list()
for link in broken_links:
    link["target_file_name_count"] = target_file_names_count[link["target_file_name"]]
    broken_links_with_stats.append(link)

if args.csv:
    with open(args.csv, "w") as csvfile:
        field_names = ["target_file_name", "target_file_name_count", "target", "resolved_target", "type", "file"]
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        for link in broken_links_with_stats:
            writer.writerow(link)

print("Summary:")
print("Number of Broken links: {}".format(len(broken_links)))
print("Number of unique broken link targets: {}".format(len(target_file_names_count)))
