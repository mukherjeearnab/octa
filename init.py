import os


def run():

    # Create .octa folder in root directory
    if not os.path.exists('.octa'):
        print("Initialized empty octa repository.")
        os.makedirs('.octa')
    else:
        print("Octa repository already exists.")
