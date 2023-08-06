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

"""Retrieve available password files
"""

import os


class PasswordItem(dict):
    """Helper class for password file
    """
    def __init__(self, root: str, root_name: str, f: str, f_name: str, path: str):
        dict.__init__(self, root=root, root_name=root_name, f=f, f_name=f_name, path=path)
        self.root = root
        self.root_name = root_name
        self.f = f
        self.f_name = f_name
        self.path = path


class passwords:
    """Static class for password files
    """

    @staticmethod
    def get_list(path: str, filter: str) -> list[PasswordItem]:
        """Return the list of password files

        Args:
            path (str): working directory
            filter (str): name filter

        Returns:
            list[PasswordItem]: list of password files
        """
        assert (os.path.exists(path)), f"Path <{path}> does not exist"
        assert (os.path.isdir(path)), f"Path <{path}> is not a valid directory"

        items: list[PasswordItem] = []
        for (root, dirs, files) in os.walk(path):
            # Loop all directories (only one level)
            dirs.sort()
            files.sort()
            is_root_ok = False

            root_name = root.replace(os.path.join(path, ""), "")

            if ".git" in root_name:
                # Skip git directory
                continue
            if filter == "" or filter.lower() in root_name.lower():
                # Check directory name vs filter
                # is_root_ok = True
                # TODO set this flag to True with enhanced filters
                pass

            for f in files:
                # Loop all files
                f_name = f.replace(".gpg", "")

                is_file_ok = is_root_ok
                if not f.endswith(".gpg"):
                    # Skip non gpg files
                    continue
                if filter == "" or filter.lower() in f_name.lower():
                    # Check file name vs filter
                    is_file_ok = True
                if is_file_ok:
                    # Add to returned list
                    items.append(PasswordItem(root, root_name, f, f_name, os.path.join(root, f)))

        return items
