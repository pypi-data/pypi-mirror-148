import os
import getpass
import warnings
from . import path
from .local_io import LocalIO
from .minio_io import MinioIO
import urllib


class IoTools:
    def __init__(self, cache_root=None, localio=LocalIO(), minio=MinioIO(),
                 max_cache_usage_fraction=0.8, path=path):
        """
        :param cache_path: common cache path
        :param localio: path to local file storage backend
        :param minio: path to minio backend
        :param max_cache_usage_fraction: stop caching when exeeding this usage fraction
        """
        self.minio = minio
        self.localio = localio
        self.cache_root = cache_root
        self.max_cache_usage_fraction = max_cache_usage_fraction
        self.path = path

    @staticmethod
    def factory(**kwargs):
        """
        Build IoTools with new backends
        :param args:
        :param kwargs:
        :return:
        """
        kwargs["minio"] = kwargs.get("minio", MinioIO())
        kwargs["localio"] = kwargs.get("localio", LocalIO())
        return IoTools(**kwargs)

    def set_cache_root(self, root):
        root = os.path.normpath(root)
        assert os.path.isdir(root), "Cache root must be a path to a directory"
        self.cache_root = root

    def get_backend(self, path):
        if path.startswith("s3://"):
            return self.minio
        else:
            return self.localio

    def resolve_access_rights(self, path, *args, **kwargs):
        backend = self.get_backend(path)
        backend.resolve_access_rights(path, *args, **kwargs)

    def read_file(self, path, cache=None, errors="raise"):
        try:
            path = path if isinstance(path, str) else str(path, "utf-8")
            backend = self.get_backend(path)

            cache_root = cache or self.cache_root
            if cache_root and backend.cache_files:
                return self.localio.file_cache(path, cache_root, backend.read, self.max_cache_usage_fraction)
            else:
                return backend.read(path)
        except Exception as ex:
            if errors == "raise":
                raise ex
            return None

    def write_file(self, path, content):
        return self.get_backend(path).write(path, content)

    def remove(self, path):
        return self.get_backend(path).remove(path)

    def copy(self, src, dst, *args, **kwargs):
        src_backend = self.get_backend(src)
        dst_backend = self.get_backend(dst)
        if src_backend == dst_backend:
            return src_backend.copy(src, dst, *args, **kwargs)
        else:
            return dst_backend.write(dst, src_backend.read(src))

    def move(self, src, dst, *args, **kwargs):
        if src == dst:
            return
        src_backend = self.get_backend(src)
        dst_backend = self.get_backend(dst)
        if src_backend == dst_backend:
            return src_backend.move(src, dst, *args, **kwargs)
        else:
            raise NotImplementedError("Cross origin move")

    def make_dirs(self, path):
        backend = self.get_backend(path)
        return backend.make_dirs(path)

    def walk(self, path, exclude_hidden=False, **kwargs):
        backend = self.get_backend(path)
        return backend.walk(path, exclude_hidden=exclude_hidden, **kwargs)

    def isfile(self, path):
        backend = self.get_backend(path)
        return backend.isfile(path)

    @staticmethod
    def get_uri(path):
        if path.startswith("gs://"):
            path = path[5:]
        elif path.startswith("s3://"):
            path = path[len(path[:5].split("/", 1)[0]) + 5:]
        return urllib.parse.quote(path, safe='')

    def get_md5(self, path):
        backend = self.get_backend(path)
        return backend.get_md5(path)


io_tools = IoTools()


def load_file_safe(x, cache_dir=None, io=io_tools):
    """
    Load a file safely with and without tensorflow
    :param x: path to file
    :param cache_dir:
    :param io:
    :return:
    """
    try:
        assert x
        try:
            x = x.numpy()
        except AttributeError:
            pass
        buf = io.read_file(x, cache_dir)
        return buf or b''
    except Exception as ex:
        #log.error(str(np.array(x), "utf8"), exc_info=ex)
        return b''


def prompt_for_password(prompt="Password:"):
    password = getpass.getpass(prompt)
    if len(password) <= 1:
        warnings.warn(f"Did you mean to enter a password with length {len(password)}")
        if os.name == "nt":
            warnings.warn(f""" Beware of windows terminal bug, when pasting secrets into a Windows terminal using Ctrl+V
                In addition to Ctrl+V, Shift+Insert also doesn't work. This behavior is the same Command Prompt and PowerShell on Windows 10.

                Workarounds include:

                - Type the password
                - Clicking `Edit > Paste` from the window menu
                - Enabling `Properties > Options > Use Ctrl+Shift+C/V as Copy/Paste` from the menu
                - Use right-click to paste
                - Using the new Windows Terminal: https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701
                - provide the password as an environment variable - which is currently supported by web_api / PlatformAPI
            """)
    return password