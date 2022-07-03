import os

# абсолютные пути
ROOT_PATH_ABS = os.getenv('IDE_PROJECT_ROOTS')
PROJECT_PATH_ABS = os.path.dirname(__file__)
DATA_PATH_ABS = os.path.join(PROJECT_PATH_ABS, 'data')

# относительные пути
ROOT_PATH = '/' + os.path.relpath(ROOT_PATH_ABS, ROOT_PATH_ABS)
PROJECT_PATH = '/' + os.path.relpath(PROJECT_PATH_ABS, ROOT_PATH_ABS)
DATA_PATH = '/' + os.path.relpath(DATA_PATH_ABS, ROOT_PATH_ABS)
pass