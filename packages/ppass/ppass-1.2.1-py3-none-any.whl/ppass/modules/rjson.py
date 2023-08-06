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

"""Utils for JSON response
"""

import json
import rich


class rjson:
    """Static class for JSON response
    """

    @staticmethod
    def success(data: json = {}, message: str = ""):
        """Success response

        Args:
            data (json, optional): JSON data content. Defaults to {}.
            message (str, optional): Success message. Defaults to "".
        """
        json_item = {}
        json_item["success"] = True
        json_item["message"] = message
        json_item["data"] = data
        try:
            rich.print(json.dumps(json_item, indent=4))
        except Exception:
            json_item["data"] = data.to_json()
            rich.print(json.dumps(json_item, indent=4))

    @staticmethod
    def error(message: str = ""):
        """Error response

        Args:
            message (str, optional): Error message. Defaults to "".
        """
        json_item = {}
        json_item["success"] = False
        json_item["message"] = message
        json_item["data"] = None
        rich.print(json.dumps(json_item, indent=4))
