import os
from zipfile import ZipFile
import hashlib
import pandas as pd
import time


def run():
    rootdir = './'
    files = _getAllFiles(rootdir)
    filesdf = _createFileDataFrame(files)
    _createCSVDump(filesdf)
    print(f'Added {len(files)} files.')


def _createCSVDump(filesdf):
    filepath = os.path.join('.', '.octa', 'files.csv')
    filesdf.to_csv(filepath, index=False)
    csvHash = _getHash(filepath)
    timestamp = _getTimestamp()

    # Rename file to Stage Hash
    os.rename(filepath, os.path.join('.', '.octa', f'{csvHash}.csv'))

    # Add Stage to index file
    with open(os.path.join('.', '.octa', 'index.txt'), 'w') as out:
        out.write(f'{csvHash},{timestamp}\n')


def _getTimestamp():
    return time.time()


def _createFileDataFrame(files):
    file_hash_list = []

    # Generate MD5 Hashes of all files
    index = 1
    for filename in files:
        print(f"Adding ({index}/{len(files)})", end='\r')
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
