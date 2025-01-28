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

def copyFiles(fileList: list[str]) -> None:
    """Copy files from static/ to public/ recursively

    Args:
        fileList (list[str]): _description_

    Raises:
        NotImplementedError: _description_
    """
    
    if len(fileList) == 1:
        raise NotImplementedError
    pass

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