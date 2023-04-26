# SSHMan

!!!! BROKEN !!!!
Needs a major overhaul, does not work correctly righ tnow. I'll hopefully have time to get around to it soon.


A simple utility to manage ssh servers and keys.
Uses docopt and tinydb.

```
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
```
