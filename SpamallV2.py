from .. import loader, utils
def register(cb):
    cb(spamallV2Mod())
class spamallV2Mod(loader.Module):
    """Спамим по всем чатам"""
    strings = {'name': 'SpamAllV2'}
    async def spamallcmd(self, message):
        '''запуск спамчика'''
        await utils.answer(message, "спамим в чаты...")
        args = utils.get_args_raw(message) 
        ф = 0
        н = 0
        получилось = ""
        неполучилось = ""
        if not args: 
            return await utils.answer(message, "<b>Эту команду юзни в чате, Даун.</b>") 
        async for i in message.client.iter_dialogs():
            title = i.name
            if not title:
                title = "Зомби 🧟"
            try:
                await message.client.send_message(i.id, args)
                ф = ф+1
                получилось += "\n"+title
            except Exception as e:
                н = н+1
                неполучилось += "\n"+title
        return await utils.answer(message, "<b>Закончил спамить в чаты!</b>\n<b>Получилось:</b> <code>"+получилось+"\n\n"+str(ф)+" чатов</code>\n<b>Не получилось:</b> <code>"+неполучилось+"\n\n"+str(н)+" чатов</code>")