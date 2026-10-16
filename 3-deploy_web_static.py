#!/usr/bin/python3
"""Deploy the web_static folder to a new version."""

from datetime import datetime
import os
from fabric.api import local


def do_pack():
    """Generate a .tgz archive from the web_static folder."""
    if not os.path.isdir("web_static"):
        return None

    if not os.path.isdir("versions"):
        os.makedirs("versions")

    filename = "web_static_{}.tgz".format(
        datetime.now().strftime("%Y%m%d%H%M%S"))
    archive_path = os.path.join("versions", filename)
    result = local(
        "tar -czf {} web_static".format(archive_path),
        capture=True)
    if result.failed:
        return None
    return archive_path


def do_deploy(archive_path):
    """Deploy an archive to a new release."""
    if not archive_path or not os.path.isfile(archive_path):
        return False

    try:
        filename = os.path.basename(archive_path)
        release_name = filename[:-4] if filename.endswith(".tgz") else filename
        release_path = "/data/web_static/releases/{}".format(release_name)

        local("mkdir -p {}".format(release_path))
        local("tar -xzf {} -C {}".format(archive_path, release_path))

        source_path = os.path.join(release_path, "web_static")
        if os.path.isdir(source_path):
            local("cp -a {}/. {}/".format(source_path, release_path))
            local("rm -rf {}".format(source_path))

        local("ln -sfn {} /data/web_static/current".format(release_path))
        return True
    except Exception:
        return False


def deploy():
    """Pack and deploy the web_static folder."""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)


if __name__ == "__main__":
    deploy()
