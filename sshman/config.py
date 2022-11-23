"""Configuration class"""
from pathlib import Path, PurePath
import shutil


class Config:
    home_dir = str(Path.home())
    db_dir = PurePath(home_dir, '.config/', 'sshman/')
    db_file = PurePath(db_dir, 'data.json')
    key_dir = PurePath(home_dir, ".ssh/")

    keygen = shutil.which("ssh-keygen")
    sshbin = shutil.which("ssh")
    sshcp = shutil.which("ssh-copy-id")

    Path(db_dir).mkdir(parents=True, exist_ok=True)

