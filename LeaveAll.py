from .. import loader, utils
from telethon.tl.types import PeerChat as e
from telethon.tl.types import PeerUser as r
from telethon.tl.functions.channels import LeaveChannelRequest

def register(cb):
    cb(LeaveChatsMod())
class LeaveChatsMod(loader.Module):
    strings = {'name': 'LeaveChats'}
    async def client_ready(self, client, db):
        self.db = db
    async def leaveallcmd(self, message):
        whchat = self.db.get("LeaveChats", "WHchats", [])
        allchats = await message.client.get_dialogs()
        suc = err = 0
        for _ in allchats:
            try:
                chat = _.entity.megagroup
            except:
                None
            if _.name.startswith("friendly-"):
                None
            elif type(_.message.to_id) == r:
                None
            elif chat or type(_.message.to_id) == e:
                if _.id not in whchat:
                    try:
                        await message.client(LeaveChannelRequest(_.id))
                        suc += 1
                    except:
                        err += 1
        await message.client.send_message(message.chat_id, f"Вы вышли из {suc} чатов\nНе получилось выйти из {err} чатов")
    async def bcleavecmd(self, message):
        whchat = self.db.get("LeaveChats", "WHchats", [])
        chatid = message.chat_id
        if chatid not in whchat:
            whchat.append(chatid)
            self.db.set("LeaveChats", "WHchats", whchat)
            return await message.edit("Чат был занесен в вайтлист")
        else:
            whchat.remove(chatid)
            self.db.set("LeaveChats", "WHchats", whchat)
            return await message.edit("Чат был убран из вайтлиста")
    async def whleavecmd(self, message):
        whchat = self.db.get("LeaveChats", "WHchats", [])
        chats = ""
        n = 0
        for _ in whchat:
            n += 1
            chatdata = await message.client.get_entity(_)
            chats += f"<b>{n})</b> {chatdata.title} <code>({chatdata.id})</code>\n"
        await message.client.send_message(message.chat_id, f"Список чатов в вайт листе:\n{chats}")