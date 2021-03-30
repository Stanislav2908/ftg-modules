#смс бомбер работающий на боте t.me/framebomb_bot
# автор by @laciamemeframe

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from .. import loader, utils


def refister(cb):
    cb(SmsbomberMod())
class SmsbomberMod(loader.Module):
    """Вдохновлялся русской смекалкой"""
    strings = {'name': 'Смс_бомбер'}
    
    def __init__(self):
        self.name = self.strings['name']
        self._me = None
        self._ratelomit = {}
    
    async def client_ready(self, client, db):
        self._db =db
        self._client = client
        self.me =await client.get.me() 

    async def smsbombercmd(self, event):
        """.smsbomber {Номер}"""
        user_msg = """{}""".format(utils.get_args_raw(event))
        global text
        text = False
        if event.fwd_from:
            return
            self_mess = True
            if not user_msg:
                await event.edit('<code>Напишите номер в формате 380xxxxxxxxx, 79xxxxxxxxx, 77xxxxxxxxx. 998хххххххх</code>')
                return 
        chat = '@FrameBomb_bot'
        await event.edit('<code>Спам запущен на 10 минут</code>')
        async with event.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(events.NewMessage(incoming=True,
                                                             from_users=1130754200))
                await event.client.send_message(chat, user_msg)
                response = await response
            except YouBlockedUserError:
                await event.reply('<code>Разблокируй @FrameBomb_bot</code>')

    async def stopsmsbombercmd(self, event):
        """.stopsmsbomber останавливает смс спам"""
        user_msg = """{}""".format(utils.get_args_raw(event))
        global text
        text = False
        if event.fwd_from:
            return
            self_mess = True
            if not user_msg:
                await event.edit('<code>Напишите номер в формате 380xxxxxxxxx, 79xxxxxxxxx, 77xxxxxxxxx. 998хххххххх</code>')
                return 
        chat = '@FrameBomb_bot'
        await event.edit('<code>Смс спам остановлен</code>')
        async with event.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(events.NewMessage(incoming=True,
                                                             from_users=1130754200))
                await event.client.send_message(chat, 'Остановить спам🛑')
                response = await response
            except YouBlockedUserError:
                await event.reply('<code>Разблокируй @FrameBomb_bot</code>')            