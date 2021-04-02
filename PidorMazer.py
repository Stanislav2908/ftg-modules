from .. import loader, utils 
import re, random 
@loader.tds 
class PidorMazerMod(loader.Module): 
    strings = {"name": "Пидормайзер"} 
    prefix = "<b>[Пидормайзер]</b>\n" 
    @loader.owner 

    async def pidrchcmd(self, m): 
        ".pidrch покажу пидора в чате!:)" 
        if not m.chat: await m.edit(self.prefix+"<b>Это не чат, Пидор</b>"); return 
        users = await m.client.get_participants(m.chat) 
        user = random.choice(users) 
        await m.edit(self.prefix+f"<b>Режим:</b> ПидорМейзер, покажу пидора чата\n<b>Пидор чата:</b> <a href=\"tg://user?id={user.id}\">{user.first_name}</a> | <code>{user.id}</code>")