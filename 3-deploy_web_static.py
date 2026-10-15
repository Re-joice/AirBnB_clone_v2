#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers,
using the function deploy.
"""
from fabric.api import env, local
from datetime import datetime
import os

env.hosts = ['52.55.249.213', '54.157.32.137']


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
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


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        from fabric.api import put, run
        filename = os.path.basename(archive_path)
        name_no_ext = os.path.splitext(filename)[0]
        tmp_path = "/tmp/{}".format(filename)
        dest_folder = "/data/web_static/releases/{}/".format(name_no_ext)

        put(archive_path, tmp_path)
        run("mkdir -p {}".format(dest_folder))
        run("tar -xzf {} -C {}".format(tmp_path, dest_folder))
        run("rm {}".format(tmp_path))
        run("mv {}web_static/* {}".format(dest_folder, dest_folder))
        run("rm -rf {}web_static".format(dest_folder))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(dest_folder))

        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """
    Creates and distributes an archive to the web servers.
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
