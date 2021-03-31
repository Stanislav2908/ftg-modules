# Coded by D4n1l3k300
# t.me/D4n13l3k00
from .. import loader, utils
def register(cb):
	cb(RipperMod())
class RipperMod(loader.Module):
	"""Ripper"""
	strings = {'name': 'Ripper'}
	def __init__(self):
		self.name = self.strings['name']
		self._me = None
		self._ratelimit = []
	async def client_ready(self, client, db):
		self._db = db
		self._client = client
		self.me = await client.get_me()
	async def ripcmd(self, message):
		"""Похоронить"""
		await message.edit("""<code>⁠    _
⁪ __| |__ 
|_R.I.P_|
   | |   
   | |   
   | |   
   |_|</code>
""")
	async def ripingcmd(self, message):
		"""Похоронить с табличкой
		Можно реплай или свой текст"""
		reply = await message.get_reply_message()
		if utils.get_args_raw(message):
			ript = utils.get_args_raw(message)
		else:
			try:
				reply.sender
				ript = reply.sender.first_name
			except:
				await message.edit("Oh fuck")
				return
		await message.edit(f"""<code>⁠       _
   ⁪ __| |__ 
   |_R.I.P_|
      | |   
      | |   
      | |   
      |_|

Посвящается {ript}
     от души
   в душу

        ауф</code>
""")
		


		