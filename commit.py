import os
from zipfile import ZipFile
import hashlib
import pandas as pd


def run():
    hashfile = os.path.join('.', '.octa', 'files.csv')
    # Check if files.csv exists
    if not os.path.isfile(hashfile):
        print("Error! Files are not staged for commit.\nUse octa add to stage files for commit.")
        return

    # Check for unstaged and modified files
    print("Checking for any unstaged changes.")
    files = _getAllFiles('.')
    filesdf = _createFileDataFrame(files)
    prexdf = pd.read_csv(hashfile)
    if not filesdf.equals(prexdf):
        print("Error! Untracked or modified files present.\nUse octa add to unstaged and modified files for commit.")
        return

    print("Check Complete!\nChanges can be committed successfully.")

    print("Starting commit.")
    stage_hash = _getHash(hashfile)
    _createZip(prexdf, stage_hash)


def _createZip(prexdf, stage_hash):
    # create a ZipFile object
    # zipObj = ZipFile(os.path.join('.', '.octa', f'{stage_hash}.zip', 'w')
    # add files to the zip
    '''sdfsdf'''
    # zipObj.write(filename='aac.pdf', arcname='xc')
    # close the Zip File
    # zipObj.close()


def _createFileDataFrame(files):
    file_hash_list = []

    # Generate MD5 Hashes of all files
    index = 1
    for filename in files:
        print(f"Calculating file ({index}/{len(files)})", end='\r')
        file_hash = _getHash(filename)
        file_hash_list.append([file_hash, filename])

    # Create Dataframe form 2D List
    file_hash_df = pd.DataFrame(file_hash_list, columns=['Hash', 'FilePath'])

    return file_hash_df


def _getHash(filename):
    md5_hash = hashlib.md5()
    with open(filename, "rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
        return md5_hash.hexdigest()


def _getAllFiles(path):
    files = _absoluteFilePaths(path)
    return list(files)


def _absoluteFilePaths(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        # if ".octa" in dirnames:
        #     dirnames.remove(".octa")

        for f in filenames:
            yield os.path.relpath(os.path.join(dirpath, f)).replace(os.sep, '/')
