"""
Create a file ~/.surfsara with content:

user=<username>
pass=<password>

 * login to https://ui.hpccloud.surfsara.nl/
 * make sure you are in the user view
 * go to Storage -> Apps
 * select an "app" (like Ubuntu-16.04.3-Server (2017-12-07)) and press
   "openNebula"
 * select local_images_ssh datastore and then press "download"
 * Go to VM Templates view and notice VM template ID. Use that ID
   on the CLI or change in this script.

"""
from time import sleep

import oca
import paramiko
import os
import sys

DEFAULT_TEMPLATE_ID = 14190
NODENAME = "saltmaster"
CPU = 1
MEM = 2 * 1024

config_path = os.path.expanduser("~/.surfsara")
endpoint = 'https://api.hpccloud.surfsara.nl/RPC2'


def read_config():
    if not os.access(config_path, os.R_OK):
        print("can't read {}".format(config_path))
        print(__doc__)
        sys.exit(1)

    config = {}
    with open(config_path, 'r') as f:
        for l in f:
            s = l.strip().split('=')
            if len(s) == 2:
                config[s[0]] = s[1]

    if not ('user' in config and 'pass' in config):
        print("can't find user and/or pass in config")
        print(__doc__)
        sys.exit(1)
    return config


def destroy(client):
    vmp = oca.VirtualMachinePool(client=client)
    vmp.info()
    destroyed = []
    for i in vmp:
        if i.name == NODENAME:
            answer = input(f"{NODENAME} exists, going to destroy. is that OK? (Y/n)")
            if answer.lower().strip() == 'y':
                print("destroying node '{}'".format(i.name))
                i.delete()
                destroyed.append([v.ip for v in i.template.nics][0])
            else:
                exit(1)
    return destroyed


def create(client):
    tp = oca.VmTemplatePool(client)
    tp.info()
    template = tp.get_by_id(DEFAULT_TEMPLATE_ID)
    print(f"creating node '{NODENAME}'")

    extra_template = f"""
    MEMORY = {MEM}
    CPU = {CPU}
    VCPU = {CPU}
    """

    template.instantiate(name=NODENAME, extra_template=extra_template)


def wait_for_active(client, destroyed=None):
    if not destroyed:
        destroyed = []
    vp = oca.VirtualMachinePool(client)
    while True:
        print(f"waiting for new {NODENAME} to become active")
        sleep(1)
        vp.info()
        for vm in vp:
            if vm.name == NODENAME:
                ip = [v.ip for v in vm.template.nics][0]

                if vm.state == vm.ACTIVE:

                    # the destroyed machines stay active for a while
                    if ip in destroyed:
                        continue

                    print(f"name: {vm.name} state: {vm.str_state} ip: {ip}")
                    return ip


def run_command(ssh_client: paramiko.SSHClient, cmd: str):
    print(f"running command {cmd}")
    _, stdout, stderr = ssh_client.exec_command(cmd)
    print("stdout:")
    for line in stdout:
        print(line, end=None)
    print("stderr:")
    for line in stderr:
        print(line, end=None)


def install_salt(ip):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh_client.connect(ip, username='ubuntu')
    run_command(ssh_client, "curl -o bootstrap-salt.sh -L https://bootstrap.saltstack.com")
    run_command(ssh_client, "sudo sh bootstrap-salt.sh -M stable")


def main():
    config = read_config()
    client = oca.Client(f"{config['user']}:{config['pass']}", endpoint)

    #destroyed = destroy(client)
    destroyed = []
    #create(client)

    ip = wait_for_active(client, destroyed=destroyed)
    install_salt(ip)


if __name__ == '__main__':
    main()
