#!/usr/bin/python3

# import
import threading
import configparser
import socket
import subprocess
import os

# set module functions
conf = configparser.ConfigParser()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clients = []
unames = []

# define variables from `conf_server`
def load_config():
    config_file = '/lib/lchat/server_conf.ini'
    config_file_dir = config_file.rsplit('/', 1)[0] + '/'
    print(f"Loading config file '{config_file}'...")
    try:
        conf.read(config_file)
        global HOST; HOST = conf['server_conf']['HOST']
        global PORT; PORT = int(conf['server_conf']['PORT'])
        print(f"Loaded config file '{config_file}'...")
    except (FileNotFoundError, KeyError) as errno:
        # create library if needed
        if not os.path.exists(config_file_dir):
            os.mkdir(config_file_dir)
            print(f"Created library '{config_file_dir}'...")
        with open(config_file, 'a') as file:
            # get network interface type
            intf = subprocess.getoutput('ifconfig | grep "BROADCAST,RUNNING"').split(':')[0]
            intf_ip = subprocess.getoutput("ip address show dev " + intf).split()
            intf_ip = intf_ip[intf_ip.index('inet') + 1].split('/')[0]
            # write the conf
            conf.add_section('server_conf')
            conf.set('server_conf', 'HOST', intf_ip)
            conf.set('server_conf', 'PORT', '8644')
            conf.write(file)
        # load config file
        print(f"Failed: {errno} not found - retrying...")
        load_config()
    except Exception as errno:
        # unexpected error reaction
        print("Failed: unexpeced error occured at {errno} - retrying...")
        load_config()

# define socket server connection
def start_server():
    server.bind((HOST, PORT))
    server.listen()
    print(f"Started server at [{HOST}:{PORT}]...")

# define broadcast message
def broadcast(message, uname):
    for client in clients:
        client.send(message)

# execute functions (main method)
if __name__ == '__main__':
    load_config()
    start_server()
