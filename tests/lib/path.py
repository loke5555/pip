# flake8: noqa
# -*- coding: utf-8 -*-
# Author: Aziz Köksal
from __future__ import absolute_import

import glob
import os
import shutil
import sys

from pip._vendor import six

try:
    from os import supports_fd
except ImportError:
    supports_fd = set()



_base = six.text_type if os.path.supports_unicode_filenames else str


class Path(_base):
    """
    Models a path in an object oriented way.
    """

    # File system path separator: '/' or '\'.
    sep = os.sep

    # Separator in the PATH environment variable.
    pathsep = os.pathsep

    def __new__(cls, *paths):
        if len(paths):
            return _base.__new__(cls, os.path.join(*paths))
        return _base.__new__(cls)

    def __div__(self, path):
        """
        Joins this path with another path.

        >>> path_obj / 'bc.d'
        >>> path_obj / path_obj2
        """
        return Path(self, path)

    __truediv__ = __div__

    def __rdiv__(self, path):
        """
        Joins this path with another path.

        >>> "/home/a" / path_obj
        """
        return Path(path, self)

    __rtruediv__ = __rdiv__

    def __idiv__(self, path):
        """
        Like __div__ but also assigns to the variable.

        >>> path_obj /= 'bc.d'
        """
        return Path(self, path)

    __itruediv__ = __idiv__

    def __sub__(self, path):
        """
        Makes this path relative to another path.

        >>> path_obj - '/home/a'
        >>> path_obj - path_obj2
        """
        return Path(os.path.relpath(self, path))

    def __rsub__(self, path):
        """
        Returns path relative to this path.

        >>> "/home/a" - path_obj
        """
        return Path(os.path.relpath(path, self))

    def __add__(self, path):
        """
        >>> Path('/home/a') + 'bc.d'
        '/home/abc.d'
        """
        return Path(_base(self) + path)

    def __radd__(self, path):
        """
        >>> '/home/a' + Path('bc.d')
        '/home/abc.d'
        """
        return Path(path + _base(self))

    def __repr__(self):
        return u"Path(%s)" % _base.__repr__(self)

    def __hash__(self):
        return _base.__hash__(self)

    @property
    def name(self):
        """
        '/home/a/bc.d' -> 'bc.d'
        """
        return os.path.basename(self)

    @property
    def namebase(self):
        """
        '/home/a/bc.d' -> 'bc'
        """
        return Path(os.path.splitext(self)[0]).name

    @property
    def ext(self):
        """
        '/home/a/bc.d' -> '.d'
        """
        return Path(os.path.splitext(self)[1])

    @property
    def abspath(self):
        """
        './a/bc.d' -> '/home/a/bc.d'
        """
        return Path(os.path.abspath(self))

    @property
    def realpath(self):
        """
        Resolves symbolic links.
        """
        return Path(os.path.realpath(self))

    @property
    def normpath(self):
        """
        '/home/x/.././a//bc.d' -> '/home/a/bc.d'
        """
        return Path(os.path.normpath(self))

    @property
    def folder(self):
        """
        Returns the folder of this path.

        '/home/a/bc.d' -> '/home/a'
        '/home/a/' -> '/home/a'
        '/home/a' -> '/home'
        """
        return Path(os.path.dirname(self))

    @property
    def exists(self):
        """
        Returns True if the path exists.
        """
        return os.path.exists(self)

    def mkdir(self, mode=0x1FF):  # 0o777
        """
        Creates a directory, if it doesn't exist already.
        """
        if not self.exists:
            os.mkdir(self, mode)
        return self

    def makedirs(self, mode=0x1FF):  # 0o777
        """
        Like mkdir(), but also creates parent directories.
        """
        if not self.exists:
            os.makedirs(self, mode)
        return self

    def remove(self):
        """
        Removes a file.
        """
        return os.remove(self)

    rm = remove  # Alias.

    def rmdir(self):
        """
        Removes a directory.
        """
        return os.rmdir(self)

    def rmtree(self, noerrors=True):
        """
        Removes a directory tree. Ignores errors by default.
        """
        return shutil.rmtree(self, ignore_errors=noerrors)

    def copy(self, to):
        return shutil.copy(self, to)

    def copytree(self, to):
        """
        Copies a directory tree to another path.
        """
        return shutil.copytree(self, to, symlinks=True)

    def move(self, to):
        """
        Moves a file or directory to another path.
        """
        return shutil.move(self, to)

    def rename(self, to):
        """
        Renames a file or directory. May throw an OSError.
        """
        return os.rename(self, to)

    def glob(self, pattern):
        return (Path(i) for i in glob.iglob(self.join(pattern)))

    def join(self, *parts):
        return Path(self, *parts)

    def read_text(self):
        with open(self, "r") as fp:
            return fp.read()

    def write(self, content):
        with open(self, "w") as fp:
            fp.write(content)

    def touch(self, times=None):
        with open(self, "a") as fp:
            os.utime(fp.fileno() if os.utime in supports_fd else self, times)

curdir = Path(os.path.curdir)
