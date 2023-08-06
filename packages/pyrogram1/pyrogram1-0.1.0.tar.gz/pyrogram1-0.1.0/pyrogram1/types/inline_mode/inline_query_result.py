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

from uuid import uuid4

import pyrogram1
from pyrogram1 import types
from ..object import Object

"""- :obj:`~pyrogram1.types.InlineQueryResultCachedAudio`
    - :obj:`~pyrogram1.types.InlineQueryResultCachedDocument`
    - :obj:`~pyrogram1.types.InlineQueryResultCachedGif`
    - :obj:`~pyrogram1.types.InlineQueryResultCachedMpeg4Gif`
    - :obj:`~pyrogram1.types.InlineQueryResultCachedPhoto`
    - :obj:`~pyrogram1.types.InlineQueryResultCachedSticker`
    - :obj:`~pyrogram1.types.InlineQueryResultCachedVideo`
    - :obj:`~pyrogram1.types.InlineQueryResultCachedVoice`
    - :obj:`~pyrogram1.types.InlineQueryResultAudio`
    - :obj:`~pyrogram1.types.InlineQueryResultContact`
    - :obj:`~pyrogram1.types.InlineQueryResultGame`
    - :obj:`~pyrogram1.types.InlineQueryResultDocument`
    - :obj:`~pyrogram1.types.InlineQueryResultGif`
    - :obj:`~pyrogram1.types.InlineQueryResultLocation`
    - :obj:`~pyrogram1.types.InlineQueryResultMpeg4Gif`
    - :obj:`~pyrogram1.types.InlineQueryResultPhoto`
    - :obj:`~pyrogram1.types.InlineQueryResultVenue`
    - :obj:`~pyrogram1.types.InlineQueryResultVideo`
    - :obj:`~pyrogram1.types.InlineQueryResultVoice`"""


class InlineQueryResult(Object):
    """One result of an inline query.

    Pyrogram currently supports results of the following types:

    - :obj:`~pyrogram1.types.InlineQueryResultArticle`
    - :obj:`~pyrogram1.types.InlineQueryResultPhoto`
    - :obj:`~pyrogram1.types.InlineQueryResultAnimation`
    """

    def __init__(
        self,
        type: str,
        id: str,
        input_message_content: "types.InputMessageContent",
        reply_markup: "types.InlineKeyboardMarkup"
    ):
        super().__init__()

        self.type = type
        self.id = str(uuid4()) if id is None else str(id)
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup

    async def write(self, client: "pyrogram1.Client"):
        pass
