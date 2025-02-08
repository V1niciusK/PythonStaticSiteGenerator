from os import path, listdir, mkdir
from shutil import copy, rmtree

## Utils

def cleanDir(dirname: str) -> None:
    """Will erase the entirety of a very specific directory, not before logging all files and backing it up.

    Args:
        dirname (str): _description_

    Raises:
        NotImplementedError: _description_
    """
    raise NotImplementedError


# This is obviously less practical than copytree, but for the sake of the exercise this is here
def exerciseCopyFiles(fileList: list[str], destination: str) -> None:
    """Copy files from static/ to public/ recursively

    Args:
        fileList (list[str]): _description_

    Raises:
        NotImplementedError: _description_
    """
    
    # base case
    if len(fileList) == 1:
        copy(fileList[0], destination)
        return
    
    copy(fileList[0], destination)
    exerciseCopyFiles(fileList[1:])
    return

## Major functions

def publicDirectoryPrep() -> None:
    """Will call cleanDir() to unpopulate public/ before calling copyFiles() in preparation for server startup. In the interest of keeping this function clean I have severed out the functions that will deal with os calls. For now they reside inside this main functiion but will eventually be migrated to a utils.py file.

    Raises:
        NotImplementedError: _description_
    """
    raise NotImplementedError



def main():
    # Prepare for server startup
    publicDirectoryPrep()
    
    # Process md files
    
    # Start static content server
    

if __name__ == "__main__":
    main()