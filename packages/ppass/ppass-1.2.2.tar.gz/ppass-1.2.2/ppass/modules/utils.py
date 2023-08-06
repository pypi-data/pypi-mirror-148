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

"""Other utils
"""

import string
import random


class utils:
    """Static class for utils
    """

    @staticmethod
    def generate_password() -> str:
        """Generate a new random password

        Returns:
            str: random password
        """
        g4_1 = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(4))
        g4_2 = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(4))
        g4_3 = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(4))
        return g4_1 + "-" + g4_2 + "-" + g4_3
