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

"""Utils for handling cli parameters validation
"""

import os
import click

from rich import print
from rich.prompt import Prompt

from .passwords import PasswordItem
from .folders import FolderItem
from .ui import ui
from .gpg import gpg


class params:
    """Static class for handling cli parameters validation
    """

    @staticmethod
    def validate(is_json: bool,
                 value: str,
                 message: str,
                 default_value: str = "",
                 print_old: bool = False,
                 old_value: str = "") -> str:
        """Generic string parameter validation

        Args:
            is_json (bool): is cli in JSON mode
            value (str): parameter value
            message (str): cli message for input
            default_value (str, optional): default value if cli input. Defaults to "".
            print_old (bool, optional): if True prints the existing value. Defaults to False.
            old_value (str, optional): existing value. Defaults to "".

        Returns:
            str: validated value
        """
        new_value = value.strip()
        # If JSON mode, new_value must not be empty
        assert (new_value != "" or not is_json), f"Incorrect <{message}> value"
        if new_value == "":
            if print_old:
                print(f"Current value: {old_value}")
            if default_value == "":
                new_value = Prompt.ask(message)
            else:
                new_value = Prompt.ask(message, default=default_value)
            assert (new_value.strip() != ""), f"Incorrect <{message}> value"
        return new_value

    @staticmethod
    def validate_path(is_json: bool, value: str, message: str) -> str:
        """Path parameter validation

        Args:
            is_json (bool): is cli in JSON mode
            value (str): parameter value
            message (str): cli message for input

        Returns:
            str: validated value
        """
        new_value = params.validate(is_json, value, message)
        # assert (os.path.exists(new_value)), "Invalid path"
        if not os.path.exists(new_value):
            os.makedirs(new_value)
        return new_value

    @staticmethod
    def validate_identity(is_json: bool, value: str) -> str:
        """Identity parameter validation

        Args:
            is_json (bool): is cli in JSON mode
            value (str): parameter value

        Returns:
            str: validated value
        """
        new_value = value.strip()
        identities = gpg.get_identities()
        availables_keyids = list(map(lambda i: i["keyid"], identities))
        assert (not(is_json and new_value not in availables_keyids)), f"Invalid identity key <{value}>"
        if (new_value != "" and new_value not in availables_keyids):
            new_value = ""
        if new_value == "":
            identity = ui.select_identity(identities)
            new_value = identity["keyid"]
        assert (new_value != ""), "Invalid identity key"
        return new_value

    @staticmethod
    def validate_multiline(is_json: bool, value: str, old_value: str, message: str) -> str:
        """Multiline parameter validation

        Args:
            is_json (bool): is cli in JSON mode
            value (str): parameter value
            old_value (str, optional): existing value
            message (str): cli message for input

        Returns:
            str: validated value
        """
        new_value = value.strip()
        if not is_json and new_value == "":
            new_value = click.edit(old_value)
        return new_value

    @staticmethod
    def validate_passwordvalue(is_json: bool, value: str) -> str:
        """Password parameter validation

        Args:
            is_json (bool): is cli in JSON mode
            value (str): parameter value

        Returns:
            str: validated value
        """
        new_value = value.strip()
        assert (new_value != "" or not is_json), "Incorrect password value"
        if new_value == "":
            new_value1 = Prompt.ask("Password", password=True)
            new_value2 = Prompt.ask("Confirm password", password=True)
            assert (new_value1 == new_value2), "Incorrect password confirmation"
            new_value = new_value1.strip()
            assert (new_value != ""), "Incorrect password value"
        return new_value

    @staticmethod
    def validate_folder(is_json: bool, name: str, folder_items: list[FolderItem]) -> str:
        """Folder parameter validation

        Args:
            is_json (bool): is cli in JSON mode
            value (str): parameter value
            folder_items (list[FolderItem]): list of folders

        Returns:
            str: validated value
        """
        assert (len(folder_items) != 0), "No folder available"
        found_name = list(filter(lambda i: i.name.lower().startswith(name.lower()), folder_items))
        if len(found_name) == 1:
            return found_name[0]["name"]
        elif is_json and len(found_name) > 1:
            raise Exception("Multiple folders")
        elif is_json and name != "":
            raise Exception(f"Folder <{name}> does not exist")
        elif is_json:
            raise Exception("Invalid folder name")
        elif len(found_name) == 0 and name != "":
            raise Exception(f"Folder <{name}> does not exist")
        else:
            folder = ui.select_folder(found_name)
            return folder["name"]

    @staticmethod
    def validate_password(is_json: bool, items: list[PasswordItem]) -> PasswordItem:
        """Password file paramater validation

        Args:
            is_json (bool): is cli in JSON mode
            items (list[PasswordItem]): list of password files

        Returns:
            PasswordItem: validated password file
        """
        assert (len(items) != 0), "No password"
        if is_json:
            assert (len(items) == 1), "Multiple password items"
            return items[0]
        elif len(items) != 1:
            return ui.select_password(items)
        else:
            return items[0]
