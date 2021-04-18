# -*- coding: future_fstrings -*-

#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from .. import loader, utils
import logging
import asyncio
import telethon
import os
import re

logger = logging.getLogger(__name__)


def register(cb):
    cb(TerminalMod())


class TerminalMod(loader.Module):
    """Runs commands"""
    def __init__(self):
        self.commands = {"terminal": self.terminalcmd, "terminate": self.terminatecmd, "kill": self.killcmd,
                         "apt": self.aptcmd, "neofetch": self.neocmd, "uptime": self.upcmd}
        self.config = loader.ModuleConfig("FLOOD_WAIT_PROTECT", 2, "How long to wait in seconds during commands")
        self.name = _("Terminal")
        self.activecmds = {}

    async def terminalcmd(self, message):
        """.terminal <command>"""
        await self.runcmd(message, utils.get_args_raw(message))

    async def aptcmd(self, message):
        """Shorthand for '.terminal apt'"""
        await self.runcmd(message, ("apt " if os.geteuid() == 0 else "sudo -S apt ")
                          + utils.get_args_raw(message) + " -y",
                          RawMessageEditor(message, "apt " + utils.get_args_raw(message), self.config, True))

    async def runcmd(self, message, cmd, editor=None):
        if len(cmd.split(" ")) > 1 and cmd.split(" ")[0] == "sudo":
            needsswitch = True
            for word in cmd.split(" ", 1)[1].split(" "):
                if word[0] != "-":
                    break
                if word == "-S":
                    needsswitch = False
            if needsswitch:
                cmd = " ".join([cmd.split(" ", 1)[0], "-S", cmd.split(" ", 1)[1]])
        sproc = await asyncio.create_subprocess_shell(cmd, stdin=asyncio.subprocess.PIPE,
                                                      stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                                                      cwd=utils.get_base_dir())
        if editor is None:
            editor = SudoMessageEditor(message, cmd, self.config)
        editor.update_process(sproc)
        self.activecmds[hash_msg(message)] = sproc
        await editor.redraw(True)
        await asyncio.gather(read_stream(editor.update_stdout, sproc.stdout, self.config["FLOOD_WAIT_PROTECT"]),
                             read_stream(editor.update_stderr, sproc.stderr, self.config["FLOOD_WAIT_PROTECT"]))
        await editor.cmd_ended(await sproc.wait())
        del self.activecmds[hash_msg(message)]

    async def terminatecmd(self, message):
        """Use in reply to send SIGTERM to a process"""
        if not message.is_reply:
            await message.edit(_("Reply to a terminal command to terminate it."))
            return
        if hash_msg(await message.get_reply_message()) in self.activecmds:
            try:
                self.activecmds[hash_msg(await message.get_reply_message())].terminate()
            except Exception:
                await message.edit(_("Could not kill!"))
            else:
                await message.edit(_("Killed!"))
        else:
            await message.edit(_("No command is running in that message."))

    async def killcmd(self, message):
        """Use in reply to send SIGKILL to a process"""
        if not message.is_reply:
            await message.edit(_("Reply to a terminal command to kill it."))
            return
        if hash_msg(await message.get_reply_message()) in self.activecmds:
            try:
                self.activecmds[hash_msg(await message.get_reply_message())].kill()
            except Exception:
                await message.edit(_("Could not kill!"))
            else:
                await message.edit(_("Killed!"))
        else:
            await message.edit(_("No command is running in that message."))

    async def neocmd(self, message):
        """Show system stats via neofetch"""
        await self.runcmd(message, "neofetch --stdout", RawMessageEditor(message, "neofetch --stdout", self.config))

    async def upcmd(self, message):
        """Show system uptime"""
        await self.runcmd(message, "uptime", RawMessageEditor(message, "uptime", self.config))


def hash_msg(message):
    return str(utils.get_chat_id(message)) + "/" + str(message.id)


async def read_stream(func, stream, delay):
    last_task = None
    data = b""
    while True:
        dat = (await stream.read(1))
        if not dat:
            # EOF
            if last_task:
                # Send all pending data
                last_task.cancel()
                await func(data.decode("utf-8"))
                # If there is no last task there is inherently no data, so theres no point sending a blank string
            break
        data += dat
        if last_task:
            last_task.cancel()
        last_task = asyncio.ensure_future(sleep_for_task(func, data, delay))


async def sleep_for_task(func, data, delay):
    await asyncio.sleep(delay)
    await func(data.decode("utf-8"))


class MessageEditor():
    def __init__(self, message, command, config):
        self.message = message
        self.command = command
        self.stdout = ""
        self.stderr = ""
        self.rc = None
        self.redraws = 0
        self.config = config

    async def update_stdout(self, stdout):
        self.stdout = stdout
        await self.redraw()

    async def update_stderr(self, stderr):
        self.stderr = stderr
        await self.redraw()

    async def redraw(self, skip_wait=False):
        text = _("<code>Running command: {}").format(utils.escape_html(self.command)) + "\n"
        if self.rc is not None:
            text += _("Process exited with code {}").format(utils.escape_html(str(self.rc)))
        text += "\n" + _("Stdout:") + "\n"
        text += utils.escape_html(self.stdout[max(len(self.stdout) - 2048, 0):]) + "\n\n" + _("Stderr:") + "\n"
        text += utils.escape_html(self.stderr[max(len(self.stdout) - 1024, 0):]) + "</code>"
        try:
            await self.message.edit(text)
        except telethon.errors.rpcerrorlist.MessageNotModifiedError:
            pass
        except telethon.errors.rpcerrorlist.MessageTooLongError as e:
            logger.error(e)
            logger.error(text)
        # The message is never empty due to the template header

    async def cmd_ended(self, rc):
        self.rc = rc
        self.state = 4
        await self.redraw(True)

    def update_process(self, process):
        pass


class SudoMessageEditor(MessageEditor):
    PASS_REQ = "[sudo] password for"
    WRONG_PASS = r"\[sudo\] password for (.*): Sorry, try again\."
    TOO_MANY_TRIES = r"\[sudo\] password for (.*): sudo: [0-9]+ incorrect password attempts"

    def __init__(self, message, command, config):
        super().__init__(message, command, config)
        self.process = None
        self.state = 0
        self.authmsg = None

    def update_process(self, process):
        logger.debug("got sproc obj %s", process)
        self.process = process

    async def update_stderr(self, stderr):
        logger.debug("stderr update " + stderr)
        self.stderr = stderr
        lines = stderr.strip().split("\n")
        lastline = lines[-1]
        lastlines = lastline.rsplit(" ", 1)
        handled = False
        if len(lines) > 1 and re.fullmatch(self.WRONG_PASS,
                                           lines[-2]) and lastlines[0] == self.PASS_REQ and self.state == 1:
            logger.debug("switching state to 0")
            await self.authmsg.edit(_("Authentication failed, please try again."))
            self.state = 0
            handled = True
            await asyncio.sleep(2)
            await self.authmsg.delete()
        logger.debug("got here")
        if lastlines[0] == self.PASS_REQ and self.state == 0:
            logger.debug("Success to find sudo log!")
            text = r"<a href='tg://user?id="
            text += str((await self.message.client.get_me()).id)
            text += r"'>"
            text += _("Interactive authentication required.")
            text += r"</a>"
            try:
                await self.message.edit(text)
            except telethon.errors.rpcerrorlist.MessageNotModifiedError as e:
                logger.debug(e)
            logger.debug("edited message with link to self")
            self.authmsg = await self.message.client.send_message("me", _("Please edit this message to the password "
                                                                          + "for user {user} to run command {command}")
                                                                  .format(command="<code>"
                                                                          + utils.escape_html(self.command) + "</code>",
                                                                          user=utils.escape_html(lastlines[1][:-1])))
            logger.debug("sent message to self")
            self.message.client.remove_event_handler(self.on_message_edited)
            self.message.client.add_event_handler(self.on_message_edited,
                                                  telethon.events.messageedited.MessageEdited(chats=["me"]))
            logger.debug("registered handler")
            handled = True
        if len(lines) > 1 and (re.fullmatch(self.TOO_MANY_TRIES, lastline)
                               and (self.state == 1 or self.state == 3 or self.state == 4)):
            logger.debug("password wrong lots of times")
            await self.message.edit(_("Authentication failed, please try again later."))
            await self.authmsg.delete()
            self.state = 2
            handled = True
        if not handled:
            logger.debug("Didn't find sudo log.")
            if self.authmsg is not None:
                await self.authmsg.delete()
                self.authmsg = None
            self.state = 2
            await self.redraw()
        logger.debug(self.state)

    async def update_stdout(self, stdout):
        self.stdout = stdout
        if self.state != 2:
            self.state = 3  # Means that we got stdout only
        if self.authmsg is not None:
            await self.authmsg.delete()
            self.authmsg = None
        await self.redraw()

    async def on_message_edited(self, message):
        # Message contains sensitive information.
        if self.authmsg is None:
            return
        logger.debug("got message edit update in self " + str(message.id))
        if hash_msg(message) == hash_msg(self.authmsg):
            # The user has provided interactive authentication. Send password to stdin for sudo.
            try:
                self.authmsg = await message.edit(_("Authenticating..."))
            except telethon.errors.rpcerrorlist.MessageNotModifiedError:
                # Try to clear personal info if the edit fails
                await message.delete()
            self.state = 1
            self.process.stdin.write(message.message.message.split("\n", 1)[0].encode("utf-8") + b"\n")


class RawMessageEditor(SudoMessageEditor):
    def __init__(self, message, command, config, show_done=False):
        super().__init__(message, command, config)
        self.show_done = show_done

    async def redraw(self, skip_wait=False):
        logger.debug(self.rc)
        if self.rc is None:
            text = "<code>" + utils.escape_html(self.stdout[max(len(self.stdout) - 4095, 0):]) + "</code>"
        elif self.rc == 0:
            text = "<code>" + utils.escape_html(self.stdout[max(len(self.stdout) - 4090, 0):]) + "</code>"
        else:
            text = "<code>" + utils.escape_html(self.stderr[max(len(self.stderr) - 4095, 0):]) + "</code>"
        if self.rc is not None and self.show_done:
            text += "\n" + _("Done")
        logger.debug(text)
        try:
            await self.message.edit(text)
        except telethon.errors.rpcerrorlist.MessageNotModifiedError:
            pass
        except telethon.errors.rpcerrorlist.MessageEmptyError:
            pass
        except telethon.errors.rpcerrorlist.MessageTooLongError as e:
            logger.error(e)
            logger.error(text)
