---
date:    2013-09-26
subject: serializer.py
tags:
    - portfolio
    - python
abstract: |
    Written by me this afternoon, this script traverses a directory
    structure and strings all of the supported files together into a
    single plaintext file -- essentially, a compressionless archive.
    Under normal circumstances, no one should ever need this...
---

## Source

```python
import datetime
import os
import re
import sys

# ----------------------------------- CONSTANTS -----------------------------------
SUPPORTED_EXTENSIONS=(
    "css", "js", "htm", "html", "xhtm", "xhtml",
    "php", "py",
    "txt", "xml",
    "htaccess", "config", "ini"
    )
# ---------------------------------------------------------------------------------


"""
Recurses through a directory tree and serializes all supported files contained
within

@param string path
"""
def read_directory(path):

    # Keep some metrics
    files_processed = 0
    bytes_read      = 0

    # Header
    path = os.path.abspath(path)
    print("$ serializer {0:s} {1:%Y-%m-%d %X} $".format(path, datetime.datetime.now()))

    # Iterate over all directories below this
    for current_directory, subdirectories, files in os.walk(path):

        # Skip hidden directories
        if re.match("^\..+$", os.path.basename(current_directory)):
            continue

        # Iterate over all files at the current directory
        for filename in files:
            # Gather information about the current file
            absolute_path_to_file = os.path.abspath("{0}/{1}".format(current_directory, filename))
            path_to_file          = os.path.relpath(absolute_path_to_file)
            file_extension        = filename.split(".")[-1]

            # Clean up the relative path
            path_to_file = path_to_file.replace("\\", "/")
            path_to_file = re.sub("^\.+/", "", path_to_file)

            # Only process files with the proper extensions
            if file_extension in SUPPORTED_EXTENSIONS:
                fp = open(absolute_path_to_file, "r")
                file_contents = fp.read().strip()
                fp.close()

                bytes_read += len(file_contents)
                files_processed += 1
                print("#### START {0}\n{1}\n#### END {0}".format(path_to_file, file_contents))

    # Print metrics
    print()
    print("{:8d} files processed".format(files_processed))
    print("{:8d} bytes read".format(bytes_read))



"""
Main Routine
"""
def main():
    target = "."

    # Attempt to resolve any directory given as an argument
    if len(sys.argv) > 1:
        target = os.path.relpath( sys.argv[1] )

    if os.path.isdir(target):
        read_directory(target)
    else:
        print("{} is not a valid directory".format(target))
        exit(1)


# Execute Main Routine
if "__main__" == __name__:
    main()
```
