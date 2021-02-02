"""Copy figures used by document."""
import os
import os.path
import shutil
import argparse
import errno
import tempfile
import shutil

dirpath = tempfile.mkdtemp() # use a tempdir if outputdir not specified
description = 'Build manifest for publication in LaTex.'
parser = argparse.ArgumentParser(description=description)
parser.add_argument('main', help="main file name", type=str)
parser.add_argument("--outputdir", help="output directory for manifest",
                    default="manifest")
parser.add_argument("--extensions", help="image file extensions",
                    default=['pdf', 'pdf_tex', 'png'])

args = parser.parse_args()

MAIN_FILE = args.main
TARGET_DIR = args.outputdir
EXTENSIONS = args.extensions
TMP_FLAG = False

cwd = os.getcwd()
if TARGET_DIR == 'manifest':
    TARGET_DIR = dirpath
    TMP_FLAG = True

# check if dep file has been built
try:
    DEP_FILE_BASE = os.path.splitext(MAIN_FILE)[0]
    DEP_FILE = DEP_FILE_BASE + ".dep"
    with open(DEP_FILE) as tmp:
        pass
except FileNotFoundError:
    message = f"missing dep file: {DEP_FILE}"
    print(message)
    quit()

BIB_FILE = DEP_FILE_BASE + ".bbl"
try:
    with open(BIB_FILE) as tmp:
        pass
except FileNotFoundError:
    mssage = "missing bbl file: {BIB_FILE}"
    print(message)
    quit()


def get_image_files():
    img_files = []
    with open(DEP_FILE, 'r') as f:
        for line in f:
            print(line)
            if '*{file}' not in line:
                continue
            value = line.split('{')[2].split('}')
            source = value[0]
            _, e = os.path.splitext(source)
            e = e.lower()[1:]
            if e not in EXTENSIONS:
                continue
            print(source)
            img_files.append(source)
    return img_files


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def main():
    """main"""
    image_files = get_image_files()
    file_list = []
    manifest = ["# File list"]
    MAIN_PDF = DEP_FILE_BASE + ".pdf"
    file_list.append(MAIN_PDF)
    manifest.append(f'- {MAIN_PDF}:\t compiled master pdf')
    file_list.append(MAIN_FILE)
    manifest.append(f'- {MAIN_FILE}:\t master tex file')
    file_list.append(BIB_FILE)
    manifest.append(f'- {BIB_FILE}:\t bib entries file')
    for i, file_name in enumerate(image_files):
        manifest.append(f'- {file_name}:\t Figure {i+1}')
        file_list.append(file_name)
    print("\n".join(manifest))
    print(file_list)

    # create manifest directory (if it doesnt exist)
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)

    # copy files over to manifest directory
    for file_name in file_list:
        dest = os.path.join(TARGET_DIR, file_name)
        path = os.path.dirname(dest)
        make_sure_path_exists(path)
        shutil.copyfile(file_name, dest)

    # write manifest list as README.md
    with open(os.path.join(TARGET_DIR, 'README.md'), 'w') as readme:
        readme.write("\n".join(manifest))

    # create archive
    shutil.make_archive(DEP_FILE_BASE, 'zip', TARGET_DIR)

    if TMP_FLAG:
        shutil.rmtree(dirpath)


if __name__ == '__main__':
    main()
