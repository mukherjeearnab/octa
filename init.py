import os


def run():
    repoFlag = _createOctaRepository()
    if repoFlag:
        _createIndexingFile()


def _createIndexingFile():
    with open(os.path.join('.', '.octa', 'index.txt'), 'w') as out:
        out.write("stage_hash,timestamp\n")
    print("Initialized index file.")


def _createOctaRepository():
    # Create .octa folder in root directory
    if not os.path.exists('.octa'):
        print("Initialized empty octa repository.")
        os.makedirs('.octa')
        return True
    else:
        print("Octa repository already exists.")
        return False
