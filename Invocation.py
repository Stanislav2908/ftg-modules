from telethon import events
from telethon import functions
import asyncio
from telethon import errors
from .. import loader, utils

class addmembersMod(loader.Module):

    strings = {"name":"Invocation"}

    async def addcmd(self, event):
        """#Invocation"""
        if len(event.text.split()) == 2:
            idschannelgroup = event.text.split(" ", maxsplit=1)[1]
            user = [i async for i in event.client.iter_participants(event.to_id.channel_id)]
            await event.edit(f"<b>{len(user)} users will be invited from the chat {event.to_id.channel_id} to chat/channel {idschannelgroup}</b>")
            for u in user:
                try:
                    try:
                        if u.bot == False:
                            await event.client(functions.channels.InviteToChannelRequest(idschannelgroup, [u.id]))
                            await asyncio.sleep(1)
                        else:
                            pass
                    except:
                        pass
                except errors.FloodWaitError as e:
                    print('Flood for', e.seconds)
        else:
            await event.edit(f"<b>Where to invite?</b>")
    
    async def kickcmd(self, event):
        """#Invocation"""
        user = [i async for i in event.client.iter_participants(event.to_id.channel_id)]
        await event.edit(f"<b>{len(user)} users will be kicked out of the chat {event.to_id.channel_id}</b>")
        for u in user:
            try:
                try:
                    if u.is_self != True:
                        await event.client.kick_participant(event.chat_id, u.id)
                        await asyncio.sleep(1)
                    else:
                        pass
                except:
                    pass
            except errors.FloodWaitError as e:
                print('Flood for', e.seconds)