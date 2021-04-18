# -*- coding: future_fstrings -*-

#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging

from .. import loader, utils

logger = logging.getLogger(__name__)


def register(cb):
    cb(YourMod())


class YourMod(loader.Module):
    """Description for module"""
    def __init__(self):
        self.config = loader.ModuleConfig("CONFIG_STRING", _("hello"),
                                          "This is what is said, you can edit me with the configurator")
        self.name = _("A Name")

    async def examplecmd(self, message):
        """Does something when you type .example"""
        logger.debug("We logged something!")
        await utils.answer(message, self.config["CONFIG_STRING"])
