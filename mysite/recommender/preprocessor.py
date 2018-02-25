import os

def decompress():
    file = 'recommender/filteredVotes.gz'
    path = os.getcwd()
    fullpath = os.path.join(path, file)
    return fullpath