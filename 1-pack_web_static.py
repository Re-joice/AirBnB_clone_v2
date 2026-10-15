#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of
the web_static folder of the AirBnB Clone repo.
"""
from datetime import datetime
from fabric.api import local
import os


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    Returns the archive path if correctly generated, otherwise None.
    """
    try:
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        if not os.path.exists("versions"):
            os.makedirs("versions")
        file_path = "versions/web_static_{}.tgz".format(timestamp)
        print("Packing web_static to {}".format(file_path))
        result = local("tar -cvzf {} web_static".format(file_path))
        if result.succeeded:
            return file_path
        else:
            return None
    except Exception:
        return None
