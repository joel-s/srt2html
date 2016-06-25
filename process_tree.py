#!/usr/bin/env python3
#-*- coding:utf-8 -*-

"""
Example of using this module:
$ python3 process_tree.py /the/source/root /the/dest/root
"""

import os
import process_srt_file

def process_tree(src_root, dest_root):
    """
    Convert a directory tree of SRT files to HTML files.
    """
    if not os.path.isdir(src_root):
        print("Missing source directory '{}'".format(src_root))
    if os.path.exists(dest_root):
        print("Destination directory '{}' already exists".format(dest_root))

    for dirname, dirs, files in os.walk(src_root):
        dest = get_dest_dir(dirname, src_root, dest_root)
        os.mkdir(dest)
        for fname in files:
            if fname.endswith(".srt"):
                new_fname = fname[:-4] + ".html"
                process_file(os.path.join(dirname, fname),
                             os.path.join(dest, new_fname))

def get_dest_dir(dirname, src_root, dest_root):
    relative_dir = dirname[len(src_root):]
    if relative_dir[:1] in ("/", "\\"):
        relative_dir = relative_dir[1:]
    result = os.path.join(dest_root, relative_dir)
    return result

def process_file(src_name, dest_name):
    print("From {}\n to {}".format(src_name, dest_name))
    title = process_srt_file.make_title(src_name)
    with open(src_name, "r") as src, open(dest_name, "w") as dest:
        process_srt_file.convert_to_html(src, dest, title)

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: {} src-root dest-root".format(sys.argv[0]))
        sys.exit()

    process_tree(sys.argv[1], sys.argv[2])
