#!/usr/bin/python3
"""
do_pack(): Generates a .tgz archive from the
contents of the web_static folder
do_deploy(): Distributes an archive to a web server
deploy (): Creates and distributes an archive to a web server
do_clean(): Deletes out-of-date archives
"""

from fabric.operations import local, run, put, sudo
from datetime import datetime
import os
from fabric.api import env
import re


env.hosts = ['3.236.9.233', '44.200.93.43']
env.user = "ubuntu"
env.key_filename = '~/.ssh/alx'

def do_pack():
    """Function to compress files in an archive"""
    local("mkdir -p versions")
    filename = "versions/web_static_{}.tgz".format(datetime.strftime(
                                                   datetime.now(),
                                                   "%Y%m%d%H%M%S"))
    result = local("tar -cvzf {} web_static"
                   .format(filename))
    if result.failed:
        return None
    return filename


def do_deploy(archive_path):
    """Function to distribute an archive to a server"""
    if not os.path.exists(archive_path):
        return False
    rex = r'^versions/(\S+).tgz'
    match = re.search(rex, archive_path)
    filename = match.group(1)
    res = put(archive_path, "/tmp/{}.tgz".format(filename))
    if res.failed:
        return False
    res = run("mkdir -p /data/web_static/releases/{}/".format(filename))
    if res.failed:
        return False
    res = run("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/"
              .format(filename, filename))
    if res.failed:
        return False
    res = run("rm /tmp/{}.tgz".format(filename))
    if res.failed:
        return False
    res = run("mv /data/web_static/releases/{}"
              "/web_static/* /data/web_static/releases/{}/"
              .format(filename, filename))
    if res.failed:
        return False
    res = run("rm -rf /data/web_static/releases/{}/web_static"
              .format(filename))
    if res.failed:
        return False
    res = run("rm -rf /data/web_static/current")
    if res.failed:
        return False
    res = run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
              .format(filename))
    if res.failed:
        return False
    print('New version deployed!')
    return True


def deploy():
    """Creates and distributes an archive to a web server"""
    filepath = do_pack()
    if filepath is None:
        return False
    d = do_deploy(filepath)
    return d


def do_clean(number=0):
    """Deletes out-of-date archives"""
    try:
        n = int(number)
        if n < 1:
            n = 1
    except ValueError:
        print("Error: number must be an integer")
        return False
    
    files = local("ls -1t versions", capture=True)
    file_names = files.split("\n")
    if len(file_names) <= n:
        print("Nothing to delete")
        return False
    print("The following files will be deleted:")
    print("\n".join(file_names[n:]))
    confirm = input("Are you sure you want to delete these files? (y/n) ")
    if confirm.lower() != "y":
        print("Aborted")
        return False
    for i in file_names[n:]:
        local("rm versions/{}".format(i))
    dir_server = run("ls -1t /data/web_static/releases")
    dir_server_names = dir_server.split("\n")
    if len(dir_server_names) <= n:
        print("Nothing to delete")
        return False
    print("The following directories will be deleted:")
    print("\n".join(dir_server_names[n:]))
    confirm = input("Are you sure you want to delete these directories? (y/n) ")
    if confirm.lower() != "y":
        print("Aborted")
        return False
    for i in dir_server_names[n:]:
        if i == 'test':
            continue
        run("rm -rf /data/web_static/releases/{}".format(i))
    print("Done")
    return True

