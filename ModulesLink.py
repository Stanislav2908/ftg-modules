import io, inspect, logging
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class ModulesLinkMod(loader.Module):
    """Get link on module"""
    strings = {'name': 'ModulesLink'}

    @loader.unrestricted
    async def mlcmd(self, message):
        """Get link on module by one's name"""
        args = utils.get_args_raw(message)
        if not args: return await utils.answer(message, '<b>Type module name in arguments</b>')
        message = await utils.answer(message, '<b>Searching...</b>')
        try:
            f = ' '.join(
                [x.strings["name"] for x in self.allmodules.modules if args.lower() == x.strings["name"].lower()])
            r = inspect.getmodule(
                next(filter(lambda x: args.lower() == x.strings["name"].lower(), self.allmodules.modules)))
            link = str(r).split('(')[1].split(')')[0]
            if "http" not in link:
                text = f"File {f}:"
            else:
                text = f"<a href=\"{link}\">Link</a> for {f}: \n<code>{link}</code>"
            out = io.BytesIO(r.__loader__.data)
            out.name = f + ".py"
            out.seek(0)
            
            
            await utils.answer(message, text, file=out)
            await utils.answer(message, out, caption=text)
        except Exception as e:
            logger.info("Module was not found due to:", exc_info=True)
            await utils.answer(message, "<b>Module was not found</b>")
            
    async def mlccmd(self, message):
        """Get link on module by one's command"""
        args = utils.get_args_raw(message)
        if not args: return await utils.answer(message, '<b>Type module name in arguments</b>')
        if args in self.allmodules.commands.keys():
            args = self.allmodules.commands[args].__self__.strings["name"]
        else:
            return await utils.answer(message, '<b>Command was not found!</b>')
        message = await utils.answer(message, '<b>Searching...</b>')
        try:
            f = ' '.join(
                [x.strings["name"] for x in self.allmodules.modules if args.lower() == x.strings["name"].lower()])
            r = inspect.getmodule(
                next(filter(lambda x: args.lower() == x.strings["name"].lower(), self.allmodules.modules)))
            link = str(r).split('(')[1].split(')')[0]
            if "http" not in link:
                text = f"File {f}:"
            else:
                text = f"<a href=\"{link}\">Link</a> for {f}: \n<code>{link}</code>"
            out = io.BytesIO(r.__loader__.data)
            out.name = f + ".py"
            out.seek(0)
            
            
            await utils.answer(message, out, caption=text)
        except Exception as e:
            logger.info("Module was not found due to:", exc_info=True)
            await utils.answer(message, "<b>Module was not found</b>")