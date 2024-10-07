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


from typing import Optional, Union, List

import pyrogram
from pyrogram import raw, types, enums, utils


class SendStarGift:
    async def send_star_gift(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        star_gift_id: int,
        text: Optional[str] = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: Optional[List["types.MessageEntity"]] = None,
        hide_my_name: Optional[bool] = None,
    ) -> bool:
        """Send star gift.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            star_gift_id (``int``):
                Unique identifier of star gift.

            text (``str``, *optional*):
                Text of the message to be sent.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in message text, which can be specified instead of *parse_mode*.

            hide_my_name (``bool``, *optional*):
                If True, your name will be hidden from visitors to the gift recipient's profile.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Send gift
                app.send_star_gift(chat_id=chat_id, star_gift_id=123)
        """
        peer = await self.resolve_peer(chat_id)

        if not isinstance(peer, (raw.types.InputPeerUser, raw.types.InputPeerSelf)):
            raise ValueError("chat_id must belong to a user.")

        text, entities = (await utils.parse_text_entities(self, text, parse_mode, entities)).values()

        invoice = raw.types.InputInvoiceStarGift(
            user_id=peer,
            gift_id=star_gift_id,
            hide_name=hide_my_name,
            message=raw.types.TextWithEntities(text=text, entities=entities) if text else None
        )

        form = await self.invoke(
            raw.functions.payments.GetPaymentForm(
                invoice=invoice
            )
        )

        await self.invoke(
            raw.functions.payments.SendStarsForm(
                form_id=form.form_id,
                invoice=invoice
            )
        )

        return True
