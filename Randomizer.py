# Coded by D4n1l3k300
# t.me/D4n13l3k00
from .. import loader, utils
import re, random
@loader.tds
class RandomizerMod(loader.Module):
    strings = {"name": "Рандомайзер"}
    prefix = "<b>[Рандомайзер]</b>\n"
    @loader.owner
    async def rndintcmd(self, m):
        ".rndint <int> <int> - рандомное число из заданногоо диапозона"
        args = utils.get_args_raw(m)
        check = re.compile(r"^(\d+)\s+(\d+)$")
        if check.match(args):
            fr, to = check.match(args).groups()
            if int(fr) < int(to):
                rndint = random.randint(int(fr), int(to))
                await m.edit(self.prefix+f"<b>Режим:</b> Рандомное число из диапозона\n<b>Диапозон:</b> <code>{fr}-{to}</code>\n<b>Выпало число:</b> <code>{rndint}</code>")
            else: await m.edit(self.prefix+"Вася, укажи диапозон чисел!")
        else: await m.edit(self.prefix+"Вася, укажи диапозон чисел!")
    async def rndelmcmd(self, m):
        ".rndelm <элементы через запятую> - рандомный элемент из списка"
        args = utils.get_args_raw(m)
        if not args: await m.edit(self.prefix+"Вася, напиши список элементов через запятую!"); return
        lst = [i.strip() for i in args.split(",") if i]
        await m.edit(self.prefix+f"<b>Режим:</b> Рандомный элемент из списка\n<b>Список:</b> <code>{', '.join(lst)}</code>\n<b>Выпало:</b> <code>{random.choice(lst)}</code>")
    async def rndusercmd(self, m):
        ".rnduser - выбор рандомного юзера из чата"
        if not m.chat: await m.edit(self.prefix+"<b>Это не чат</b>"); return
        users = await m.client.get_participants(m.chat)
        user = random.choice(users)
        await m.edit(self.prefix+f"<b>Режим:</b> Рандомный юзер из чата\n<b>Юзер:</b> <a href=\"tg://user?id={user.id}\">{user.first_name}</a> | <code>{user.id}</code>")
    
        
        
        