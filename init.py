"""
Create a file ~/.surfsara with content:

user=<username>
pass=<password>

 * login to https://ui.hpccloud.surfsara.nl/
 * make sure you are in the user view
 * go to Apps
 * select an "app" (like Ubuntu-16.04.3-Server (2017-12-07)) and press
   "openNebula"
 * select local_images_ssh datastore and then press "download"
 * Go to VM Templates view and notice VM template ID. Use that ID
   on the CLI or change in this script.

"""
import oca
import os
import sys

DEFAULT_TEMPLATE_ID = 14190

# hostname, CPUs, MEM
layout = {
    'main':
        [('main', 4, 16 * 1024)],

    'sso':
        [('sso', 2, 2 * 1024)],

    'keep':
        [('keep', 2, 8 * 1024)],

    'store': [
        ('store0', 2, 4 * 1024),
        ('store1', 2, 4 * 1024),
    ]
}

# you probably don't want to change these
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


def init_client(user, pass_, endpoint):
    return oca.Client(f"{user}:{pass_}", endpoint)


def iplist(client):
    vp = oca.VirtualMachinePool(client)
    vp.info()
    for vm in vp:
        name = vm.name
        ip = list(v.ip for v in vm.template.nics)[0]
        yield name, ip


def create(client, name, memory, cpu, vcpu, number, template_id):
    extra_template = """
    MEMORY = {}
    CPU = {}
    VCPU = {}
    """.format(memory, cpu, vcpu)
    tp = oca.VmTemplatePool(client)
    tp.info()
    template = tp.get_by_id(template_id)
    for i in range(number):
        print("creating node '{}'".format(name))
        template.instantiate(name=name, extra_template=extra_template)


def destroy(client):
    vmp = oca.VirtualMachinePool(client=client)
    vmp.info()
    for i in vmp:
        print("destroying node '{}'".format(i.name))
        i.delete()


if __name__ == '__main__':
    config = read_config()
    client = init_client(config['user'], config['pass'], endpoint=endpoint)
    destroy(client)

    #for group, value in layout.items():
    #    for name, cpus, mem in value:
    #        create(client, name, mem, cpus, cpus, 1, template_id=DEFAULT_TEMPLATE_ID)

    print(list(iplist(client)))
