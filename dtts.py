import io
import requests

from .. import loader, utils

def register(cb):
	cb(DttsMod())

class DttsMod(loader.Module):
	"""Text to speech module"""

	strings = {'name': 'DTTS',
			  	 'no_text': "I can't say nothing"}

	async def say(self, message, speaker, text):
		if not text:
			return await utils.answer(message, self.strings['no_text'])

		reply = await message.get_reply_message()
		await message.delete()

		data = {"text": text}
		if speaker:
			data["speaker"] = speaker

		f = io.BytesIO(requests.get("https://station.aimylogic.com/generate", data=data).content)
		f.name = "file.ogg"
		
		await message.client.send_file(message.to_id, f, voice_note=True, reply_to=reply)

	async def levitancmd(self, message):
		"""Levitan voice"""
		await self.say(message, "levitan", utils.get_args_raw(message))

	async def oksanacmd(self, message):
		"""Oksana voice"""
		await self.say(message, "oksana", utils.get_args_raw(message))

	async def yandexcmd(self, message):
		"""Yandex voice"""
		await self.say(message, None, utils.get_args_raw(message))

# By @vreply @pernel_kanic @nim1love @db0mb3r and add @tshipenchko some geyporn
