#!/usr/bin/python3
"""
Main module for the HBNB project
"""

import os
from models import storage
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage

if os.environ.get('HBNB_TYPE_STORAGE') == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()
