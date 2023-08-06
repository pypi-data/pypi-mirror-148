#
# Vagrantfile generator
# Adrian Ramos
# https://github.com/aramcap/vagrantgen
#
#
# License GNU AFFERO GENERAL PUBLIC LICENSE 3.0
#
#

from os.path import exists
import argparse
import yaml
import jinja2 as j2
import subprocess
import re


def loadyamlconfig(file):
    try:
        with open(file, "r") as stream:
            return yaml.load(stream, Loader=yaml.BaseLoader)
    except yaml.YAMLError as e:
        print(e)
        exit(1)
    except IOError as e:
        print("Error: No such file '"+file+"'")
        exit(1)


def template_vagrantfile(dicc):
    template = j2.Environment(loader=j2.PackageLoader("vagrantgen", "."), trim_blocks=True).get_template("Vagrantfile.j2")
    return template.render(clusters=dicc)


def template_ansibleinventory(dicc):
    template = j2.Environment(loader=j2.PackageLoader("vagrantgen", "."), trim_blocks=True).get_template("ansible-inventory.j2")
    return template.render(hosts=dicc)


def vagrantsshconfig():
    stdout = subprocess.run(['vagrant','ssh-config'], stdout=subprocess.PIPE).stdout
    sshconfig = stdout.decode("utf-8").split("\n")
    inventory = []
    host_tmp = {}
    for elem in sshconfig:
        obj = elem.lstrip().split(" ")
        if 'Host ' in elem:
            host_tmp[obj[0]] = re.sub(r'[^\w]', '', obj[1])
        elif 'HostName ' in elem:
            host_tmp[obj[0]] = obj[1]
        elif 'User ' in elem:
            host_tmp[obj[0]] = obj[1]
        elif 'Port ' in elem:
            host_tmp[obj[0]] = obj[1]
        elif 'UserKnownHostsFile ' in elem:
            host_tmp[obj[0]] = obj[1]
        elif 'StrictHostKeyChecking ' in elem:
            host_tmp[obj[0]] = obj[1]
        elif 'PasswordAuthentication ' in elem:
            host_tmp[obj[0]] = obj[1]
        elif 'IdentitiesOnly ' in elem:
            host_tmp[obj[0]] = obj[1]
        elif 'LogLevel ' in elem:
            host_tmp[obj[0]] = obj[1]
        elif '' == elem:
            if len(host_tmp) > 0:
                inventory.append(host_tmp)
                host_tmp = {}
    return inventory


def writefile(content, file):
    try:
        with open(file, 'w') as file:
            file.write(content)
    except IOError as e:
        print("Error writing file '"+file+"'")
        exit(1)


def argparse_menu(parser):
    subparsers_main = parser.add_subparsers(help='Subcommands', dest="command")
    # generate template
    parser_template = subparsers_main.add_parser('template', help='Generate template')
    # generate vagranfile
    parser_vf = subparsers_main.add_parser('vf', help='Generate Vagrantfile')
    parser_vf.add_argument('--input', '-i', action='store', default='vagrant-template.yaml', help='Vagrant template input file name')
    parser_vf.add_argument('--stdout', '-o', nargs='?', const=True, help='To stdout')
    parser_vf.add_argument('--force', '-f', nargs='?', const=True, help='To force overwrite file')
    # generate ansible-inventory
    parser_ai = subparsers_main.add_parser('ai', help='Generate ansible-inventory file from "vagrant ssh-config" command')
    parser_ai.add_argument('--stdout', '-o', nargs='?', const=True, help='To stdout')
    parser_ai.add_argument('--force', '-f', nargs='?', const=True, help='To force overwrite file')
    return parser.parse_args()


def main():
    parser = argparse.ArgumentParser(description="Vagrantfile Generator - github.com/aramcap/vagrantgen")
    args = argparse_menu(parser)

    if args.command == "template":
        if exists("vagrant-template.yaml"):
            print("Template file already exists")
            exit(1)
        else:
            from importlib_resources import files
            template = files("vagrantgen").joinpath("vagrant-template.yaml").read_text()
            writefile(template, "vagrant-template.yaml")
    elif args.command == "vf":
        FILE_NAME = args.input
        yaml = loadyamlconfig(FILE_NAME)
        vf = template_vagrantfile(yaml)
        if args.stdout:
            print(vf)
        else:
            if args.force:
                writefile(vf, "Vagrantfile")
            elif exists("Vagrantfile"):
                print("Vagrantfile file already exists. If you want overwrite use the option -f to force.")
                exit(1)
            else:
                writefile(vf, "Vagrantfile")
    elif args.command == "ai":
        inventory = vagrantsshconfig()
        ai = template_ansibleinventory(inventory)
        if args.stdout:
            print(ai)
        else:
            if args.force:
                writefile(ai, "inventory")
            elif exists("inventory"):
                print("inventory file already exists. If you want overwrite use the option -f to force.")
                exit(1)
            else:
                writefile(ai, "inventory")
    else:
        parser.print_help()
    exit(0)

# if __name__ == "__main__":
#     main()