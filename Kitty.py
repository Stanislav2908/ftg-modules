#by @laciamemeframe

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from .. import loader, utils


def register(cb):
	cb(AnimalsMod())


class AnimalsMod(loader.Module):
	"""Фото животных из @pixelsetup_bot"""

	strings = {'name': 'Животные'}

	def __init__(self):
		self.name = self.strings['name']
		self._me = None
		self._ratelimit = []

	async def client_ready(self, client, db):
		self._db = db
		self._client = client
		self.me = await client.get_me()

	async def catcmd(self, event):
         """.cat"""
         user_msg = """{}""".format(utils.get_args_raw(event))
         global text
         text = False
         if event.fwd_from:
             return
             self_mess = True
             if not user_msg:
                 return 
         chat = '@pixelsetup_bot'
         await event.edit('<code>Обработка</code>')
         async with event.client.conversation(chat) as conv:
             try:
                 response = conv.wait_event(events.NewMessage(incoming=True,
                                                              from_users=787358569))
                 await event.client.send_message(chat, '/kitty')
                 response = await response
             except YouBlockedUserError:
                 await event.reply('<code>Разблокируй @pixelsetup_bot</code>')
                 return
             await event.delete()
             await event.client.send_file(event.to_id, response.media)
    
	async def dogcmd(self, event):
         """.dog"""
         user_msg = """{}""".format(utils.get_args_raw(event))
         global text
         text = False
         if event.fwd_from:
             return
             self_mess = True
             if not user_msg:
                 return 
         chat = '@pixelsetup_bot'
         await event.edit('<code>Обработка</code>')
         async with event.client.conversation(chat) as conv:
             try:
                 response = conv.wait_event(events.NewMessage(incoming=True,
                                                              from_users=787358569))
                 await event.client.send_message(chat, '/dogs')
                 response = await response
             except YouBlockedUserError:
                 await event.reply('<code>Разблокируй @pixelsetup_bot</code>')
                 return
             await event.delete()
             await event.client.send_file(event.to_id, response.media)  