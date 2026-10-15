#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers,
using the function do_deploy.
"""
from fabric.api import put, run, env
import os

env.hosts = ['52.55.249.213', '54.157.32.137']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        filename = os.path.basename(archive_path)
        name_no_ext = os.path.splitext(filename)[0]
        tmp_path = "/tmp/{}".format(filename)
        dest_folder = "/data/web_static/releases/{}/".format(name_no_ext)

        # 1. Upload the archive to the /tmp/ directory of the web server
        put(archive_path, tmp_path)

        # 2. Uncompress the archive to the release folder
        run("mkdir -p {}".format(dest_folder))
        run("tar -xzf {} -C {}".format(tmp_path, dest_folder))

        # 3. Delete the archive from the web server
        run("rm {}".format(tmp_path))

        # 4. Move files out of the nested web_static folder if needed
        run("mv {}web_static/* {}".format(dest_folder, dest_folder))
        run("rm -rf {}web_static".format(dest_folder))

        # 5. Delete the current symbolic link
        run("rm -rf /data/web_static/current")

        # 6. Create a new symbolic link linked to the new version
        run("ln -s {} /data/web_static/current".format(dest_folder))

        print("New version deployed!")
        return True
    except Exception:
        return False
