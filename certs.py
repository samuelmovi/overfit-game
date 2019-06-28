#!/usr/bin/env python

'''
Before executing, create the following folder on the repository's root:

certificates/
	client/
	server/
'''

import os
import shutil
import zmq.auth


base_dir = os.path.join(os.path.dirname(__file__), 'certificates')
server_dir = os.path.join(os.path.dirname(__file__), 'server')
game_dir = os.path.join(os.path.dirname(__file__), 'game')

server_secret_file = None
server_public_file = None
client_secret_file = None
client_public_file = None


def main():
    print("\n[#] Welcome to the cert-creating script")
    print("[#] Please choose one of the following options:")
    print("\n\t[1] Initialize all repository's certs\n\t[2] Create client certs\n\t[3] Create server certs\n\t[0] Exit")
    try:
        choice = int(input("[?] Your choice: "))
        if choice == 1:
            initialize_repos_certs()
        elif choice == 2:
            client_certs()
        elif choice == 3:
            server_certs()
        elif choice == 0:
            exit()
        else:
            print("\n[!!] Is it so hard to choose right?\n")
    except Exception as e:
        print("\n[!!!] Use your brain: {}".format(e))


def initialize_repos_certs():
    print("[#] Initializing all repository's certificates...")
    server_certs()
    try:
        # move server's secret key to server/certs/private
        path = os.path.join(server_dir, 'certs', 'private')
        print("[#] Moving server's private cert to: {}".format(path))
        shutil.move(server_secret_file, path)
        # save copy of public key in server/certs/
        path = os.path.join(server_dir, 'certs')
        print("[#] Copying server's public cert to: {}".format(path))
        shutil.copy(server_public_file, path)
        # move server's public key to game/certs/public
        path = os.path.join(game_dir, 'certs', 'public')
        print("[#] Moving server's public cert to: {}".format(path))
        shutil.move(server_public_file, path)
        print("[#] Server certs moved successfully")
    except Exception as e:
        print("\n[!!] Error moving files: {}".format(e))
    client_certs()
    try:
        # move client's secret key to game/certs/private
        path = os.path.join(game_dir, 'certs', 'private')
        print("[#] Moving client's private cert to: {}".format(path))
        shutil.move(client_secret_file, path)
        # save copy of public key in game/certs/
        path = os.path.join(game_dir, 'certs')
        print("[#] Copying client's public cert to: {}".format(path))
        shutil.copy(client_public_file, path)
        # move client's public key to server/certs/public
        path = os.path.join(server_dir, 'certs', 'public')
        print("[#] Moving client's public cert to: {}".format(path))
        shutil.move(client_public_file, path)
        print("[#] Client certs moved successfully")
    except Exception as e:
        print("\n[!!] Error moving files: {}".format(e))


def client_certs():
    global client_public_file, client_secret_file
    keys_dir = os.path.join(base_dir, 'client')
    print("[#] Creating new client's certificates in: {}".format(keys_dir))
    # create new keys in keys_dir named client
    client_public_file, client_secret_file = zmq.auth.create_certificates(keys_dir, "client")
    print("[#] Client certs correctly created:")
    print("\t> {}".format(client_public_file))
    print("\t> {}".format(client_secret_file))


def server_certs():
    global server_public_file, server_secret_file
    keys_dir = os.path.join(base_dir, 'server')
    print("[#] Creating new server's certificates in: {}".format(keys_dir))
    # create new keys in keys_dir named server
    server_public_file, server_secret_file = zmq.auth.create_certificates(keys_dir, "server")
    print("[#] Server certs correctly created:")
    print("\t> {}".format(server_public_file))
    print("\t> {}".format(server_secret_file))


if __name__ == '__main__':
    if zmq.zmq_version_info() < (4, 0):
        raise RuntimeError("Security is not supported in libzmq version < 4.0. libzmq version {0}".format(zmq.zmq_version()))
    main()
