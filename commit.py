import os
from zipfile import ZipFile
import hashlib
import pandas as pd
from datetime import date


def run():
    current_hash = _getStageHash()
    hashfile = os.path.join('.', '.octa', f'octa_stage_{current_hash}.csv')
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
    modified_files = _getModifiedFiles(filesdf)
    _createZip(modified_files, stage_hash)


def _getStageHash(n_stage=0):
    # Fetch Hash (if Exists)
    indexdf = pd.read_csv(os.path.join('.', '.octa', 'index.csv'))
    indexdf = indexdf.sort_values(by=['timestamp'], ascending=False)

    # Return hash if exists, else '0000'
    if len(indexdf['stage_hash'].tolist()) > n_stage:
        return indexdf['stage_hash'].tolist()[n_stage]
    else:
        return '0000'


def _getModifiedFiles(current_stage):
    prev_hash = _getLastCommitStageHash()
    hashfile = os.path.join('.', '.octa', f'octa_stage_{prev_hash}.csv')
    if os.path.isfile(hashfile):
        prev_stage = pd.read_csv(hashfile)
        current_stage = current_stage[~current_stage['Hash'].isin(
            prev_stage['Hash'])]

        return current_stage
    else:
        return current_stage


def _getLastCommitStageHash():
    last_commit_file = os.path.join('.', '.octa', 'last_commit.txt')

    # Check if Last commit exists, else return '0000'
    if os.path.isfile(last_commit_file):
        with open(last_commit_file, 'r') as reader:
            last_commit = str(reader.read())
        return last_commit
    else:
        return '0000'


def _setLastCommitStageHash(commit_hash):
    last_commit_file = os.path.join('.', '.octa', 'last_commit.txt')

    with open(last_commit_file, 'w') as writer:
        writer.write(commit_hash)


def _createZip(file_df, stage_hash):
    # create a ZipFile object
    today = _getCurrentDate()
    commit_zip_name = os.path.join(
        '.', '.octa', f'octa_commit_{stage_hash}_{today}.zip')
    zipObj = ZipFile(commit_zip_name, 'w')

    # add index and stage files to zip file
    zipObj.write(filename=os.path.join(
        '.', '.octa', f'octa_stage_{stage_hash}.csv'), arcname=f'.octa_stage_{stage_hash}.csv')
    zipObj.write(filename=os.path.join(
        '.', '.octa', 'index.csv'), arcname=f'.index.csv')

    # Drop duplicate Hash files from File DataFrame
    file_df = file_df.drop_duplicates(subset=['Hash'])
    # Added All Modified Files to Zip
    index = 1
    for _, row in file_df.iterrows():
        print(f"Committing file ({index}/{file_df.shape[0]})", end='\r')
        zipObj.write(filename=row['FilePath'], arcname=row['Hash'])

    # close the Zip File
    zipObj.close()

    # Update Last Commit Log
    _setLastCommitStageHash(stage_hash)

    # Print Commit details
    print('Commit Successful!')
    print(f'Commit Hash: {stage_hash}')
    print(f'Commit Zip Dump: {commit_zip_name}')


def _getCurrentDate():
    today = date.today()
    return str(today)


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
        if ".octa" in dirnames:
            dirnames.remove(".octa")

        for f in filenames:
            yield os.path.relpath(os.path.join(dirpath, f)).replace(os.sep, '/')
