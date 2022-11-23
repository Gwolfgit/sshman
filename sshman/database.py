from uuid import uuid4

from tinydb import TinyDB, Query, where

from .config import Config


class SSHManDB:
    def __init__(self):
        self.db = TinyDB(Config.db_file)
        self.servers_db = self.db.table("_servers")
        self.keys_db = self.db.table("_keys")

    @staticmethod
    def uuid():
        return str(str(uuid4()).split("-")[4])

    @property
    def servers(self):
        return self.servers_db

    @property
    def keys(self):
        return self.keys_db

    @staticmethod
    def is_unique(db, field, value):
        return not bool(db.search(where(field) == value))

    def add_key(self, key_name, key_type, key_bits, key_path):
        if key_name.isnumeric():
            print("Key name cannot be numeric.")
            exit(1)
        if not self.is_unique(self.keys_db, "key_name", key_name):
            print("Key name must be unique.")
            exit(1)

        return self.keys_db.insert(
            {
                "uuid": self.uuid(),
                "key_name": key_name,
                "key_type": key_type,
                "key_bits": key_bits,
                "key_path": key_path,
            }
        )

    def add_serv(self, serv_name, serv_prov, serv_dest, serv_key):
        if serv_name.isnumeric():
            print("Server name cannot be numeric.")
            exit(1)
        if not self.is_unique(self.servers_db, "serv_name", serv_name):
            print("Server name must be unique")
            exit(1)
        if ":" in serv_dest:
            parts = serv_dest.split(":")
            serv_port = parts[1]
            serv_dest = parts[0]
        else:
            serv_dest = serv_dest
            serv_port = "22"

        return self.servers_db.insert(
            {
                "uuid": self.uuid(),
                "serv_name": serv_name,
                "serv_prov": serv_prov,
                "serv_dest": serv_dest,
                "serv_port": serv_port,
                "serv_key": serv_key,
            }
        )

    def get_key(self, option: str = None):
        if not option:
            return self.keys_db.all()[0]
        if option.isnumeric():
            return self.keys_db.all()[int(option)]
        return self.servers_db.search(where("name") == option)[0]

    def get_key_uuid(self, option: str = None):
        if not option:
            return self.keys_db.all()[0]
        return self.keys_db.search(where("uuid") == option)[0]

    def get_serv(self, option: str = None):
        if not option:
            return self.servers_db.all()[0]
        if option.isnumeric():
            return self.servers_db.all()[int(option)]
        else:
            q = Query()
            return self.servers_db.search(q.serv_name == option)

    def rm_key(self, option: str = None):
        if option.isnumeric():
            i = self.keys_db.all()[int(option)]
            self.keys_db.remove(where("uuid") == i["uuid"])
        else:
            self.keys_db.remove(where("name") == option)
