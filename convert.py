import csv
import pathlib
import os
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter, chomp
from concurrent.futures import ThreadPoolExecutor

"""
#TODO - Add title meta data to md file
#TODO - Table with multiple header. E.g mqtt/index.md
#TODO - Complex table page still have problems. E.g. FreeRTOS-Plus/FreeRTOS_Plus_TCP/index.md
"""

"""
Markdown converter: https://github.com/matthewwithanm/python-markdownify
"""
class CustomMarkDownConverter(MarkdownConverter):
    """
    Custom options
    """
    class Options:
        file_path = None
        website_folder = None
        
    """
    A custom img tag converter.
    """
    def convert_img(self, el, text, convert_as_inline):
        alt = el.attrs.get('alt', None) or ''
        src = el.attrs.get('src', None) or ''
        title = el.attrs.get('title', None) or ''
        title_part = ' "%s"' % title.replace('"', r'\"') if title else ''

        if src.startswith('/'):
            target_path = os.path.join(self.options['website_folder'], src[1:])
            src = os.path.relpath(target_path, self.options['file_path'])[3:]
            src = src.replace('\\', '/')

        return f'![{alt}]({src}{title_part})'

    """
    A custom a tag converter.
    """
    def convert_a(self, el, text, convert_as_inline):
        prefix, suffix, text = chomp(text)
        if not text:
            return ''
        href = el.get('href')
        title = el.get('title')
        # For the replacement see #29: text nodes underscores are escaped
        if (self.options['autolinks']
                and text.replace(r'\_', '_') == href
                and not title
                and not self.options['default_title']):
            # Shortcut syntax
            return f'<{href}>'
        if self.options['default_title'] and not title:
            title = href
        title_part = ' "%s"' % title.replace('"', r'\"') if title else ''
        
        if href and href.startswith('/'):
            href = href.replace('.html', '.md')
            target_path = os.path.join(self.options['website_folder'], href[1:])
            href = os.path.relpath(target_path, self.options['file_path'])[3:]
            href = href.replace('\\', '/')
        
        return f'{prefix}[{text}]({href}{title_part}){suffix}' if href else text

    """
    A custom td tag converter.
    """
    def convert_td(self, el, text, convert_as_inline):
        text = text.replace("\n", "<br>")
        return f' {text} |'


"""
Get all effective html files in a directory.
Return a list of Path objects.
"""
def get_file_list(root):
    exclude_folders = [
        "FreeRTOS_Support_Forum_Archive/**/*",
        "FreeRTOS_Support_Forum_Archive/*",
    ]
    exclude_paths = [os.path.join(root, x) for x in exclude_folders]
    all_paths = pathlib.Path(root).glob("**/*.html")
    return filter(lambda x: not any(x.match(e) for e in exclude_paths),
                  all_paths)


"""
Extract main_content from html file.
Return a soup object.
"""
def extract_body(file):
    with open(file, 'r') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'lxml')
        url = soup.find("meta", property="og:url")
        menu_title = None
        if url:
            url = url['content']
            if "zh-cn-cmn-s" in str(file):
                menu_title = soup.find("a", href=f"/zh-cn-cmn-s{url}", class_=["child-node", "parent-node"])
            else:
                menu_title = soup.find("a", href=url, class_=["child-node", "parent-node"])
            menu_title = menu_title.text if menu_title else None
        title = soup.find("title")
        description = soup.find("meta", property="og:description")
        meta_data = {
            "url": url,
            "title": title.text if title else None,
            "menu_title": menu_title,         
            "description": description['content'] if description else None,
        }
        
        main_content = soup.find(id='main_content')
        if main_content != None:
            exclude_list = [
                soup.find(id='breadcrumb-trail'),
                soup.find(class_='menu-footer-container'),
                soup.find(
                    'div', string='Copyright (C) Amazon Web Services, Inc. or its affiliates. All rights reserved.')
            ]
            for e in exclude_list:
                if e != None:
                    e.extract()
        
        return main_content, meta_data


"""
Write meta data to csv
"""
def write_to_csv(meta_data_list):
    with open("statistic.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, meta_data_list[0].keys())
        writer.writeheader()
        writer.writerows(meta_data_list)


"""
Convert a html file to markdown file.
"""
def convert_file_to_markdown(file, website_folder, markdown_folder):
    main_content, meta_data = extract_body(file)
    if main_content != None:
        # print(main_content)
        markdown = CustomMarkDownConverter(
            code_language='c',
            escape_asterisks=False,
            file_path=file,
            website_folder=website_folder,
        ).convert_soup(main_content)
        new_file = str(file).replace(
            website_folder, markdown_folder).replace('.html', '.md')
        p = pathlib.Path(new_file).parent
        p.mkdir(parents=True, exist_ok=True)
        with open(new_file, 'w') as output:
            output.write(markdown)
        return meta_data
    return None


if __name__ == '__main__':
    website_folder = "/Users/kanherea/Downloads/FreeRTOS_Support_Forum_Archive/"
    markdown_folder = "./content/en-us/Test/"

    with ThreadPoolExecutor() as executor:
        meta_data_list = []
        for file in get_file_list(website_folder):
            # print(file)
            future = executor.submit(convert_file_to_markdown, file,
                            website_folder, markdown_folder)
            try:
                if result := future.result():
                    meta_data_list.append(result)
            except Exception as e:
                print(e)
        write_to_csv(meta_data_list)

    # file = os.path.join(website_folder, "zh-cn-cmn-s/a00018.html")
    # file = pathlib.PurePosixPath(file)
    # convert_file_to_markdown(file, website_folder, markdown_folder)
