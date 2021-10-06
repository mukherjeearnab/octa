import os
from zipfile import ZipFile
import hashlib
import pandas as pd
import time


def run():
    rootdir = './'
    files = _getAllFiles(rootdir)
    filesdf = _createFileDataFrame(files)
    if not _checkDuplicateStage(filesdf):
        _createCSVDump(filesdf)
        print(f'Added {len(files)} files.')
    else:
        print("All files already staged for commit.")


def _checkDuplicateStage(curent_stage):
    # Get Previous Stage (If exists)
    prev_hash = _getStageHash()
    hashfile = os.path.join('.', '.octa', f'octa_stage_{prev_hash}.csv')

    # Check Current and Previous Stage
    if os.path.isfile(hashfile):
        prev_stage = pd.read_csv(hashfile)
        if curent_stage.equals(prev_stage):
            return True
        else:
            return False
    else:
        return False


def _getStageHash(n_stage=0):
    # Fetch Hash (if Exists)
    indexdf = pd.read_csv(os.path.join('.', '.octa', 'index.csv'))
    indexdf = indexdf.sort_values(by=['timestamp'], ascending=False)

    # Return hash if exists, else '0000'
    if len(indexdf['stage_hash'].tolist()) > 0:
        return indexdf['stage_hash'].tolist()[n_stage]
    else:
        return '0000'


def _createCSVDump(filesdf):
    filepath = os.path.join('.', '.octa', 'files.csv')
    filesdf.to_csv(filepath, index=False)
    csvHash = _getHash(filepath)
    timestamp = _getTimestamp()

    # Rename file to Stage Hash
    os.rename(filepath, os.path.join(
        '.', '.octa', f'octa_stage_{csvHash}.csv'))

    # Add Stage to index file
    with open(os.path.join('.', '.octa', 'index.csv'), 'a') as out:
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

    # Clear Carriage Row
    print(f"                                                              ", end='\r')

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
        if ".octa" in dirnames:
            dirnames.remove(".octa")

        for f in filenames:
            yield os.path.relpath(os.path.join(dirpath, f)).replace(os.sep, '/')
