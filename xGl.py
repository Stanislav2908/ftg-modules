from .. import loader, utils
@loader.tds
class NeofetchMod(loader.Module):
    """Neofetch for Heroku"""
    strings = {"name": "neofetch"}
    @loader.unrestricted
    async def nftcmd(self, message):
        """Neofetch for Heroku"""
        await message.edit(__import__("os").popen("curl -Ls https://github.com/dylanaraps/neofetch/raw/master/neofetch | bash -s -- --stdout").read())
        
