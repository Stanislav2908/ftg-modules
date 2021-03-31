# Coded by D4n1l3k300
# t.me/D4n13l3k00
from .. import loader, utils
@loader.tds
class McoderMod(loader.Module):
  "Мой простейший кодировщик текста"
  strings = {"name": "Mcoder"}
  @loader.owner
  async def enccmd(self, m):
	  ".enc <text or reply_to_text>"
	  reply = await m.get_reply_message()
	  if utils.get_args_raw(m):
	    text = utils.get_args_raw(m)
	  elif reply:
	    text = reply.raw_text
	  else:
	    await m.delete()
	    return
	  await m.edit("⁠".join([str(ord(i)) for i in text]))
  async def deccmd(self, m):
	  ".dec <text or reply_to_text>"
	  reply = await m.get_reply_message()
	  if utils.get_args_raw(m):
	    text = utils.get_args_raw(m)
	  elif reply:
	    text = reply.raw_text
	  else:
	    await m.delete()
	    return
	  await m.edit("".join([chr(int(i)) for i in text.split("⁠")]))