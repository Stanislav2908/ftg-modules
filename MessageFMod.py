# by @Sm1ke
from .. import loader, utils 
import io 
  
@loader.tds 
class MessageFMod(loader.Module): 
 """send Message file""" 
 strings = {'name': 'MessageFile'} 
 
 async def filecmd(self, message): 
  """.file <reply to text>""" 
  reply = await message.get_reply_message() 
  if not reply or not reply.message: 
   await message.edit("<b>Reply to text!</b>") 
   return  
  text = bytes(reply.raw_text, "utf8") 
  fname = utils.get_args_raw(message) or str(message.id+reply.id)+".txt" 
  file = io.BytesIO(text) 
  file.name = fname 
  file.seek(0) 
  await reply.reply(file=file) 
  await message.delete() 
   
 async def kodcmd(self, message): 
  """.kod <reply to file>""" 
  reply = await message.get_reply_message() 
  if not reply or not reply.file: 
   await message.edit("<b>Reply to file!</b>") 
   return  
  text = await reply.download_media(bytes) 
  text = str(text, "utf8") 
  if utils.get_args(message): 
   text = f"<code>{text}</code>" 
  await utils.answer(message, utils.escape_html(text))