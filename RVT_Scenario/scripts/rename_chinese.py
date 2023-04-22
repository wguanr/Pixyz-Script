import os
import re
import random

# Folder to rename
folder = r'F:\PCG\pixyz\RVT_Scenario\_input'

# Regular expression to detect Chinese characters
regex = re.compile('[\u4e00-\u9fff]')

# Get all files in the folder
files = os.listdir(folder)

for f in files:
    # Check if the filename contains any Chinese characters
    if any(regex.search(c) for c in f):
        # The file name contains Chinese, rename it

        # Get the file extension
        ext = os.path.splitext(f)[1]

        # Find all Chinese words in the file name
        words = regex.findall(f)
        # print(f'{regex}======{words}')
        # Generate random ASCII words to replace the Chinese words
        replaced_words = [''.join(random.choice('abcdefghijklmnopqrstuvwxyz')
                                  ) for word in words]
        print(replaced_words)
        # Replace the Chinese words by indexing into the filename
        new_name = ''
        index = 0
        for word in words:
            new_name = new_name + f[index:f.index(word)] + replaced_words[words.index(word)]
            index = f.index(word) + len(word)
        new_name = new_name + f[index:] + ext
        print(new_name)

        # Construct the absolute file paths
        old_path = os.path.join(folder, f)
        new_path = os.path.join(folder, new_name)

        # Rename the file
        os.rename(old_path, new_path)