from fabric.api import task, run, local, put
import os

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

@task()
def hello():
    print("hello")
    put('/home/rh1n0/projects/linux-compliance-manager/checklist.py', '~/')
    output = run('uname -a')
    if output == "doido":
        print("doido")
    else:
        print("loco")
        print output


@task()
def delete_checklist():
    print("deletando...")
    output = run('sudo rm -r checklist.py')
    print output

@task()
def fab_scan():
    print("scanning...")
    output = run('python checklist.py')
    print output

