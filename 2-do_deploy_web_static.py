#!/usr/bin/python3
"""
Fabric script based on 1-pack_web_static.py that distributes
an archive to your web servers, using the function do_deploy.
"""

from fabric.api import put, run, env
import os

env.hosts = ['<IP web-01>', '<IP web-02>']


def do_deploy(archive_path):
    """Distributes an archive to your web servers."""
    if not os.path.exists(archive_path):
        return False

    try:
        file_name = os.path.basename(archive_path)
        name_no_ext = os.path.splitext(file_name)[0]
        release_path = "/data/web_static/releases/{}/".format(name_no_ext)

        put(archive_path, '/tmp/{}'.format(file_name))
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{} -C {}'.format(file_name, release_path))
        run('rm /tmp/{}'.format(file_name))
        run('mv {}web_static/* {}'.format(release_path, release_path))
        run('rm -rf {}web_static'.format(release_path))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(release_path))

        print("New version deployed!")
        return True
    except Exception:
        return False
