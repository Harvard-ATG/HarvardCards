"""
This script outputs the names of the files found in the folder "folder_path"
separated by file types. This allows easy copy pasting of file names to
flashcard templates when doing batch uploads involving images/audio.

Usage:
    Modify the variable folder_path as needed and run the script from the command line.
    The file "file_name" will be stored in the same folder as this script.
"""

import os, sys, subprocess
import numpy as np
import xlwt

folder_path = r'C:\Users\hassan\Desktop\flashcards\test'
# excel file where file names are stored
file_name = 'file_buckets.xls'
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

files = os.listdir(folder_path)

file_buckets = {}
for file in files:
    ext = file.split('.')[-1].lower()
    if ext in file_buckets.keys():
        file_buckets[ext].append(file)
    else:
        file_buckets[ext] = [file]

max_bucket_size = max(map(lambda b: len(b), file_buckets.values()))
for bucket in file_buckets.keys():
    size = len(file_buckets[bucket])
    diff = max_bucket_size - size
    file_buckets[bucket] += [None]*diff

zipped = zip(*file_buckets.values())

excel_bk = xlwt.Workbook(encoding="utf-8")
sheet = excel_bk.add_sheet("Sheet 1")

style = xlwt.easyxf('font: bold 1, height 250')

for i in range(len(file_buckets.keys())):
    sheet.write(0, i, file_buckets.keys()[i], style)
    for j in range(len(zipped)):
        sheet.write(j+1, i, zipped[j][i])
    lengths = map(lambda x: 0 if x is None else len(x), [row[i] for row in zipped])
    sheet.col(i).width = 256 * (max(lengths) + 1)

excel_bk.save(file_name)

# http://stackoverflow.com/questions/434597/open-document-with-default-application-in-python
if sys.platform.startswith('darwin'):
    subprocess.call(('open', file_path))
elif os.name == 'nt':
    os.startfile(file_path)
elif os.name == 'posix':
    subprocess.call(('xdg-open', file_path))