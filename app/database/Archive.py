import hashlib
import io
import re  # regex
import tarfile
from pathlib import Path

import ujson


class Archive():

    pattern = re.compile(r"^.*\.tar\.xz$")

    class flags():
        no_check = 0
        soft = 1     # print whether file matches checksum
        strict = 2   # print and stop read

    class Hash():
        defaultMethod = "sha256"

        def __init__(self, method: str = defaultMethod):
            self.h = hashlib.new(method)

        def __call__(self, s: bytes) -> str:
            c = self.h.copy()
            c.update(s)
            return c.hexdigest()

    def getFileNames(self):
        if self.isArchive:
            return self.archive.getnames()
        else:
            return [p.name for p in self.path.glob("*.json")]

    def read(self, filepath: str, hash_flag=flags.strict) -> dict:
        if self.isArchive:
            s = self.archive.extractfile(filepath).read()
        else:
            f = self.path/filepath
            s = f.read_bytes()

        if hash_flag != Archive.flags.no_check:
            m1 = self.hash(s)
            m2 = self.hash_dict["files"][filepath]
            if m1 == m2:
                print("Hash '{hash_method}' matches '{filepath}'".format(
                    hash_method=self.hash_dict["hash_method"], filepath=self.path/filepath))
            else:
                print(
                    "Hash '{hash_method}' does not match '{filepath}'\n"
                    "Original: {m2}\n"
                    "Current : {m1}".format(
                        hash_method=self.hash_dict["hash_method"], filepath=self.path/filepath, m1=m1, m2=m2
                    )
                )
            if hash_flag == Archive.flags.strict:
                print("Abort reading")
                return dict()
        return ujson.loads(s.decode("utf-8"))

    def write(self, filepath: str, data: dict, hash_gen=True):
        """
        filepath represent relative path to archive root
        e.g. 'f/123.txt' will create a folder 'f' and write to 'f/123.txt'
        """
        if self.mode != "w":
            return False
        s = ujson.dumps(data, ensure_ascii=False, escape_forward_slashes=False)
        encoded = s.encode("utf-8")
        if self.isArchive:
            stream = io.BytesIO(encoded)
            tarinfo = tarfile.TarInfo(name=filepath)
            tarinfo.size = len(encoded)
            self.archive.addfile(tarinfo, stream)
        else:
            f = self.path/filepath
            f.write_bytes(encoded)
        if hash_gen:
            m = self.hash(encoded)
            self.hash_dict["files"][filepath] = m
        return True

    def __init__(self, path: Path, mode: str = None):
        """
        mode is "r" or "w", None for auto detection
        """
        if mode in {"r", "w", None}:
            if mode is None:
                self.mode = "r" if path.exists() else "w"
            else:
                self.mode = mode
        else:
            print("Invalid mode '{mode}' for '{path}'".format(
                mode=mode, path=path))
            return None

        self.path = path
        if type(self).pattern.match(path.name):
            path.parent.mkdir(parents=True, exist_ok=True)
            self.isArchive = True
            self.archive = tarfile.open(path, mode+":xz")
        else:
            path.mkdir(parents=True, exist_ok=True)
            self.isArchive = False
        # hash
        if self.mode == "r":
            if "hash.json" in self.getFileNames():
                self.hash_dict = self.read("hash.json", hash_check=False)
                self.hash = type(self).Hash(self.hash_dict["hash_method"])
            else:
                print("No hash file found in {path}".format(path=self.path))
        else:
            self.hash = type(self).Hash()
            self.hash_dict = {
                "hash_method": type(self).Hash.defaultMethod,
                "files": dict()
            }

    def __del__(self):
        self.write("hash.json", self.hash_dict, False)
        if self.isArchive:
            self.archive.close()
