from datax_website import app
import os
from os import path

extra_dirs = ['./datax_website/templates', './datax_website/static']
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in os.walk(extra_dir):
        for filename in files:
            filename = path.join(dirname, filename)
            if path.isfile(filename):
                extra_files.append(filename)

if __name__ == '__main__':
    app.run(debug=True, extra_files=extra_files)

