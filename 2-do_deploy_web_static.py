#!/usr/bin/python3
"""
Fabric script based on 1-pack_web_static.py that distributes
an archive to your web servers, using the function do_deploy.
"""

from fabric.api import put, run, env
import os

env.hosts = ['<IP web-01>', '<IP web-02>']
# Optional: specify default user or ssh key if not passed via command line
# env.user = 'ubuntu'
# env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Distributes an archive to your web servers."""
    if not os.path.exists(archive_path):
        return False

    try:
        # Extract filename and name without extension
        file_name = os.path.basename(archive_path)
        name_no_ext = os.path.splitext(file_name)[0]
        release_path = "/data/web_static/releases/{}/".format(name_no_ext)

        # 1. Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/{}'.format(file_name))

        # 2. Uncompress the archive to the release folder
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{} -C {}'.format(file_name, release_path))

        # 3. Delete the archive from the web server
        run('rm /tmp/{}'.format(file_name))

        # 4. Move files out of the nested web_static folder and delete the folder
        run('mv {}web_static/* {}'.format(release_path, release_path))
        run('rm -rf {}web_static'.format(release_path))

        # 5. Delete the current symbolic link
        run('rm -rf /data/web_static/current')

        # 6. Create a new symbolic link pointing to the new release
        run('ln -s {} /data/web_static/current'.format(release_path))

        print("New version deployed!")
        return True
    except Exception:
        return False
