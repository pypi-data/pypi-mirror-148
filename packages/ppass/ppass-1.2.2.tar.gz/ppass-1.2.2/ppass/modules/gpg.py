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

"""Handle gpg actions
"""

import os
import json
import gnupg


class Password:
    """Password object
    """
    app: str = ''
    password: str = ''
    username: str = ''
    url: str = ''
    comment: str = ''

    def to_json(self) -> json:
        """Convert object to JSON

        Returns:
            json: password object in json format
        """
        json_item = {}
        json_item["app"] = self.app
        json_item["password"] = self.password
        json_item["username"] = self.username
        json_item["url"] = self.url
        json_item["comment"] = self.comment
        return json_item


class gpg:
    """Static class for gpg actions
    """

    @staticmethod
    def get_identities():
        """Get available GPG identities

        Returns:
            any: list of gpg keys
        """
        gpg_item = gnupg.GPG()
        gpg_item.encoding = "utf-8"
        return gpg_item.list_keys(True)

    @staticmethod
    def decrypt_file(filepath: str) -> str:
        """Decrypt gpg file to string

        Args:
            filepath (str): path of file to decrypt

        Returns:
            str: decrypted content
        """
        assert (os.path.exists(filepath)), f"{filepath} does not exist"
        assert (os.path.isfile(filepath)), f"{filepath} is not a file"
        assert (filepath.endswith(".gpg")), f"{filepath} is not a gpg file"

        gpg_item = gnupg.GPG()
        gpg_item.encoding = "utf-8"
        stream = open(filepath, "rb")
        decrypted_data = gpg_item.decrypt_file(stream)
        stream.close()

        return str(decrypted_data)

    @staticmethod
    def gpg_to_password(filepath: str, content: str, username_prefix: str, url_prefix: str) -> Password:
        """Transform decrypted content to Password object

        Args:
            filepath (str): path of file to decrypt
            content (str): decryted content
            username_prefix (str): prefix for username line
            url_prefix (str): prefix for url line

        Returns:
            Password: password object
        """
        password = Password()
        password.app = os.path.basename(filepath).replace(".gpg", "")
        lines = content.splitlines()
        first_line = True
        for line in lines:
            if first_line:
                first_line = False
                password.password = line.strip()
                continue
            if line.startswith(username_prefix):
                password.username = line.replace(username_prefix, "").strip()
                continue
            if line.startswith(url_prefix):
                password.url = line.replace(url_prefix, "").strip()
                continue
            password.comment += "" if password.comment == "" else "\n"
            password.comment += line
        return password

    @staticmethod
    def decrypt_to_password(filepath: str, username_prefix: str, url_prefix: str) -> Password:
        """Decrypt gpg file to Password object

        Args:
            filepath (str): path of file to decrypt
            username_prefix (str): prefix for username line
            url_prefix (str): prefix for url line

        Returns:
            Password: password object
        """
        content = gpg.decrypt_file(filepath)
        assert (content != ""), "Decrypted file is empty"
        return gpg.gpg_to_password(filepath, content, username_prefix, url_prefix)

    @staticmethod
    def encrypt_data(content: str, identity: str) -> str:
        """Encrypt string to gpg

        Args:
            content (str): data to encrypt
            identity (str): gpg identity

        Returns:
            str: encrypted content
        """
        gpg_item = gnupg.GPG()
        gpg_item.encoding = "utf-8"
        encrypted = gpg_item.encrypt(content, identity)
        encrypted = str(encrypted).strip()
        assert (encrypted != ""), "Invalid identity"
        return encrypted

    @staticmethod
    def encrypt_to_file(content: str, identity: str, filepath: str):
        """Encrypt string and save to file

        Args:
            content (str): data to encrypt
            identity (str): gpg identity
            filepath (str): file where to save encryted content
        """
        assert (not os.path.exists(filepath)), "File already exists"
        f = open(filepath, "w")
        f.writelines(gpg.encrypt_data(content, identity))
        f.close()
