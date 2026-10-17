#!/usr/bin/python3
"""Fabric script that distributes an archive to web servers."""

import os
from fabric.api import env, put, run

# Replace these placeholders with your actual ALX web-server IPs.
env.hosts = ['WEB01_IP', 'WEB02_IP']


def do_deploy(archive_path):
    """Distribute an archive to both web servers."""
    if not os.path.isfile(archive_path):
        return False

    try:
        file_name = os.path.basename(archive_path)
        release_name = os.path.splitext(file_name)[0]
        release_path = (
            "/data/web_static/releases/{}/".format(release_name)
        )
        remote_archive = "/tmp/{}".format(file_name)

        put(archive_path, remote_archive)
        run("mkdir -p {}".format(release_path))
        run("tar -xzf {} -C {}".format(
            remote_archive, release_path))
        run("rm {}".format(remote_archive))
        run("mv {}web_static/* {}".format(
            release_path, release_path))
        run("rm -rf {}web_static".format(release_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(
            release_path))

        print("New version deployed!")
        return True

    except Exception:
        return False
