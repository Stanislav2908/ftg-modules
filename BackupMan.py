# Coded by D4n1l3k300
# t.me/D4n13l3k00
from .. import loader
import io, zlib
def register(cb):
    cb(BackupManMod())
class BackupManMod(loader.Module):
    """BackupMan"""
    strings = {'name': 'BackupMan'}
    def __init__(self):
        self.name = self.strings['name']
        self._me = None
        self._ratelimit = []
    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self.me = await client.get_me()
    async def restmcmd(self, m):
        "Установить все модули из *.bkm файла"
        reply = await m.get_reply_message()
        if not reply or not reply.file or reply.file.name.split('.')[-1] != "bkm": return await m.edit("<b>[BackupMan]</b> Reply to <code>*.bkm</code> file")
        modules = self._db.get("friendly-telegram.modules.loader", "loaded_modules", [])
        txt = io.BytesIO(await reply.download_media(bytes))
        valid, already_loaded = 0, 0
        for i in zlib.decompress(txt.read()).decode('utf-8').split("\n"):
            if i not in modules:
                valid += 1
                modules.append(i)
            else: already_loaded += 1
        self._db.set("friendly-telegram.modules.loader", "loaded_modules", modules)
        await m.edit(f"<b>[BackupMan]</b>\n\n<i>Загружено:</i> <code>{valid}</code>\n<i>Загружены ранее:</i> <code>{already_loaded}</code>\n\n" + ("<b>> Юзербот автоматически перезагрузится</b>" if valid != 0 else "<b>> Ничего не загружено</b>"))
        if valid != 0: await self.allmodules.commands["restart"](await m.respond("_"))
    async def backmcmd(self, m):
        "Сделать бэкап модулей в *.bkm файл"
        modules = self._db.get("friendly-telegram.modules.loader", "loaded_modules", [])
        txt = io.BytesIO(zlib.compress("\n".join(modules).encode('utf-8'), 9))
        txt.name = "BackupMan-{}.bkm".format(str((await m.client.get_me()).id))
        await m.client.send_file(m.to_id, txt, caption=f"<b>[BackupMan]</b> <i>Бэкап модулей</i>\n<i>Модулей:</i> <code>{len(modules)}</code>")
        await m.delete()

        