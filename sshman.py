#!/usr/bin/env python3
"""
SSHman v0.8

Usage:
    sshman ls
    sshman go <id>/<name>
    sshman add <name> <user@host:port> <provider> [<key>]
    sshman rm <id>
    sshman lsk
    sshman newkey <keyname> [<keytype>] [<keybits>]
    sshman addkey <keyname>
    sshman cpkey <keyid>/<keyname> <servid>/<servname>
    sshman rmkey <id>/<name>
    sshman (-h | --help | --version)
Options:
    -h, --help  Show this screen and exit.
    -p, --port  Port [default: 22]
    -k, --key   Keyname [default: id_rsa]
    -i, --init  Copies key [default: false]
"""

import sys

from docopt import docopt
from sshman.command import SSHManCMD


if __name__ == "__main__":
    shm = SSHManCMD()
    opt = docopt(__doc__, version="SSHman version 0.8")
    cmd = sys.argv[1]

    match cmd:
        case "add":
            shm.add(
                opt["<name>"],
                opt["<user@host:port>"],
                opt["<provider>"],
                opt["<key>"],
            )
        case "ls":
            shm.ls()
        case "go":
            shm.go(
                opt["<id>/<name>"]
            )
        case "rm":
            shm.rm(
                opt["<id>/<name>"]
            )
        case "rmkey":
            shm.rmkey(
                opt["<id>/<name>"]
            )
        case "addkey":
            shm.addkey(
                opt["<keyname>"]
            )
        case "cpkey":
            shm.cpkey(
                opt["<keyid>/<keyname>"],
                opt["<servid>/<servname>"],
            )
        case "lsk":
            shm.lsk()
        case "newkey":
            shm.nkey(
                opt["<keyname>"],
                opt["<keytype>"],
                opt["<keybits>"],
            )
