#!/usr/bin/python3
"""
Initialize the models package, instantiating the storage engine
based on the HBNB_TYPE_STORAGE environment variable.
"""
from os import getenv

storage_t = getenv('HBNB_TYPE_STORAGE')

if storage_t == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
