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

"""Handle xdotool actions
"""

import subprocess


class xdotool:
    """Static class for handling xdotool actions
    """

    @staticmethod
    def clip(username: str, password: str):
        """Minimize current window and paste username and password

        Args:
            username (str): password username
            password (str): password value
        """
        xdotool.minimize_window()
        xdotool.send_message(username)
        xdotool.send_tab()
        xdotool.send_message(password)
        xdotool.send_return()

    @staticmethod
    def ssh_open(user: str, domain: str, password: str):
        """Minimize current window and connect to SSH

        Args:
            user (str): SSH user
            domain (str): SSH site
            password (str): SSH password
        """
        xdotool.minimize_window()
        subprocess.call(["gnome-terminal", "--maximize", "--window", "--", "bash", "-c", f"ssh {user}@{domain}"])
        xdotool.wait("1")
        xdotool.send_message(f"{password}\n")

    @staticmethod
    def wait(duration: str = "0.2"):
        """Wait between two xdotool actions
        """
        subprocess.call(["sleep", duration])

    @staticmethod
    def minimize_window():
        """Minimize current window
        """
        subprocess.call(["xdotool", "getactivewindow", "windowminimize"])
        xdotool.wait()

    @staticmethod
    def send_message(message: str):
        """Send message to active window

        Args:
            message (str): message
        """
        subprocess.call(["xdotool", "getactivewindow", "type", message])
        xdotool.wait()

    @staticmethod
    def send_tab():
        """Send <kbd>Tab</kbd> to active window
        """
        subprocess.call(["xdotool", "getactivewindow", "key", "Tab"])

    @staticmethod
    def send_return():
        """Send <kbd>Enter</kbd> to active window
        """
        subprocess.call(["xdotool", "getactivewindow", "key", "Return"])
