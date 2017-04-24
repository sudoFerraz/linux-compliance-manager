import repo
import pkgs
from fabric.api import task, run

@task()
def update_all(reboot_host='false'):
    """
    Yum update a host
    :param reboot_host:
        (false|no|true|yes)
        reboot the host if its true
    """
    run("yum update -y")
    if reboot_host == 'true' or reboot_host == 'yes':
        run("reboot")


def hello():
    print("hello")
