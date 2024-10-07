#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.
from typing import List

import pyrogram
from pyrogram import raw, types


class GetStarGifts:
    async def get_star_gifts(
        self: "pyrogram.Client",
    ) -> List["types.StarGift"]:
        """Get all available star gifts to send.

        .. include:: /_includes/usable-by/users.rst

        Returns:
            List of :obj:`~pyrogram.types.StarGift`: On success, a list of star gifts is returned.

        Example:
            .. code-block:: python

                app.get_star_gifts()
        """
        r = await self.invoke(
            raw.functions.payments.GetStarGifts(hash=0)
        )

        return types.List([await types.StarGift._parse(self, gift) for gift in r.gifts])
