import os
import sys
import cmd
import subprocess
from pathlib import PurePath

from tinydb import where
from columnar import columnar
from sshpubkeys import SSHKey, InvalidKeyError

from .database import SSHManDB
from .config import Config


class SSHManCMD(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.db = SSHManDB()

    @staticmethod
    def err(msg):
        print(msg)
        exit(1)

    def add(
        self, name: str, destination: str, provider: str, keyname: str = None
    ) -> None:
        key = self.db.get_key_uuid(keyname)["uuid"]
        self.db.add_serv(name, provider, destination, key)
        self.ls()

    def ls(self) -> str:
        data = []
        for k, item in enumerate(self.db.servers):
            data.append(
                [
                    k,
                    item["serv_name"],
                    f"{item['serv_dest']}:{item['serv_port']}",
                    item["serv_prov"],
                ]
            )

        if len(data):
            headers = ["#", "Name", "Destination", "Provider"]
            table = columnar(data, headers, no_borders=True)
            print(table)
        else:
            print("No entires.")

    def rm(self, name: str) -> None:
        rows = self.db.servers.all()
        for item in rows:
            self.db.servers.remove(where("name") == name)

    def cpkey(self, key=None, serv=None):
        kdata = self.db.get_key(key)
        sdata = self.db.get_serv(serv)

        print(f"Copying {kdata['key_name']} to {sdata['serv_dest']}")

        os.execl(
            Config.sshcp,
            "ssh-copy-id",
            "-i",
            kdata["key_path"],
            "-p",
            sdata["serv_port"],
            sdata["serv_dest"],
        )

    def rmkey(self, option):
        self.db.rm_key(option)
        self.lsk()

    def addkey(self, keyname):
        path = str(PurePath(Config.key_dir, keyname))
        try:
            with open(f"{path}.pub", "r") as file:
                sshk = SSHKey(str(file.read()))
                sshk.parse()
        except InvalidKeyError as err:
            self.err("Invalid key:", err)
        except NotImplementedError as err:
            self.err("Invalid key type:", err)
        except FileNotFoundError as err:
            self.err(f"File not found: {path}.pub")
        else:
            self.db.add_key(keyname, str(sshk.key_type.decode()), str(sshk.bits), path)
            self.lsk()

    def nkey(self, keyname: str, keytype: str = None, keybits: str = None):
        path = str(PurePath(Config.key_dir, keyname))

        def ktype():
            if not keytype:
                return ["-t", "ecdsa", "-b", "521"]
            if not keybits:
                return ["-t", keytype]
            return ["-t", keytype, "-b", keybits]

        kt = ktype()
        command = [Config.keygen, "-f", path]
        command.extend(kt)

        p1 = subprocess.Popen(["printf", "\n"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(command, stdin=p1.stdout, stdout=subprocess.PIPE)

        for s in (str(p2.communicate())[2:-10]).split("\\n"):
            print(s)

        self.addkey(keyname)

    def lsk(self):
        data = []
        for k, item in enumerate(self.db.keys):
            data.append([k, item["key_name"], f"{item['key_type']}", item["key_bits"]])

        if len(data):
            headers = ["#", "Name", "Keytype", "Keybits"]
            table = columnar(data, headers, no_borders=True)
            print(table)
        else:
            print("No keys.")

    def go(self, serv_option, key_option):

        try:
            serv = self.db.get_serv(serv_option)
        except:
            self.err("Invalid server")

        if not key_option:
            try:
                key = self.db.get_key_uuid(serv["serv_key"])["key_path"]
            except IndexError:
                try:
                    key = self.db.get_key()["key_path"]
                except IndexError:
                    self.err("There are no default keys configured. Try sshman newkey.")
        else:
            try:
                key = self.db.get_key(key_option)["key_path"]
            except IndexError:
                self.err("Invalid key")

        if not serv:
            self.err("Invalid server")
        else:
            os.execl(
                str(Config.sshbin),
                "ssh",
                str(serv["serv_dest"]),
                "-o",
                "IdentitiesOnly=yes",
                "-i",
                str(key),
            )
