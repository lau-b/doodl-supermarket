from pathlib import Path


def get_project_root():
    ''' Returns the absolute path of the project including the project folder.
    '''
    return Path(__file__).parent.parent

# TODO: create initial data/ structure
