from .. import loader, utils 
@loader.tds 
class SaveFFMod(loader.Module): 
    """SaveFF module""" 
    strings = {"name": "Saveff"} 
    @loader.unrestricted 
    async def fcmd(self, message): 
        """.f - save Text/media""" 
        reply = await message.get_reply_message() 
        if not reply: 
            return 
        await message.client.send_message("me", reply) 
        await message.delete()