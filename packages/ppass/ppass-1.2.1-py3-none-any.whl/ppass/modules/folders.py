# Copyright (C) 2022 Sebastien Guerri
#
# This file is part of ppass.
#
# ppass is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# ppass is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Utils to handle folders
"""

import os
import shutil


# TODO rename class
class FolderItem(dict):
    """Helper class for folder item
    """
    def __init__(self, path: str, name: str):
        dict.__init__(self, path=path, name=name)
        self.path = path
        self.name = name


# TODO rename class
class folders:
    """Static class for folder handling
    """

    @staticmethod
    def get_list(path: str) -> list[FolderItem]:
        """Get the list of folders

        Args:
            path (str): working directory

        Returns:
            list[FolderItem]: list of folders
        """
        assert (os.path.exists(path)), f"Path <{path}> does not exist"
        assert (os.path.isdir(path)), f"Path <{path}> is not a valid directory"
        paths = os.listdir(path)
        paths.sort()
        # Remove hidden folders
        paths = list(filter(lambda p: not p.startswith("."), paths))
        # Remove files
        paths = list(filter(lambda p: os.path.isdir(os.path.join(path, p)), paths))
        # Transform to folder items
        paths = list(map(lambda p: FolderItem(os.path.join(path, p), p), paths))
        return paths

    @staticmethod
    def create(name: str, path: str):
        """Create a directory

        Args:
            name (str): Directory name
            path (str): Directory path
        """
        assert (name.strip() != ""), "Incorrect folder name"
        assert (not os.path.exists(path)), f"Folder <{name}> already exists"
        try:
            os.mkdir(path)
        except OSError as error:
            raise Exception(error.strerror)

    @staticmethod
    def delete(name: str, path: str):
        """Delete a directory

        Args:
            name (str): Directory name
            path (str): Directory path
        """
        assert (name.strip() != ""), "Incorrect folder name"
        assert (os.path.exists(path)), f"Folder <{name}> does not exist"
        assert (os.path.isdir(path)), f"Path <{path}> is not a valid directory"
        try:
            shutil.rmtree(path)
        except OSError as error:
            raise Exception(error.strerror)
