# srt2html
Converts SRT (video subtitle) files to simple HTML files

## Main goal of this project

To take a tree containing SRT (video subtitle) files and convert it into
a tree of HTML files with the same structure.

## Single file conversion

Convert a single file.

From this directory, run `python3 process_srt_file.py <filename>` to print HTML.

For examples of typical SRT (input) and HTML (output) files, see the
[sample](sample) directory.

## Directory tree conversion

Convert all the files in a directory tree.

From this directory, run `python3 process_tree.py <source-root> <dest-root>`.

If *dest-root* already exists, the script exits with an error message.
