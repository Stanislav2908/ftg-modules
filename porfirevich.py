# By @vreply @pernel_kanic @nim1love @db0mb3r 

import requests

from .. import loader, utils

def register(cb):
    cb(PorfirevichMod())

class PorfirevichMod(loader.Module):
    "Porfirevich wrapper"
    
    strings = {'name': 'Porfirevich',
                        'no_text': '<strong>Empty message</strong>'}
            
    async def pfcmd(self, message):
        text = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        
        if text:
        	text = '<strong>' + text + '</strong>'
        	if reply:
        		text = '<em>' + reply.raw_text + '</em> ' + text
        else:
        	if reply:
        		text = '<strong>' + reply.raw_text + '</strong>'
        	else:
        		return await utils.answer(message, self.strings['no_text'])

        response = requests.post("https://pelevin.gpt.dobro.ai/generate/",
                                                         json={"prompt": text,"length": 30}).json()
        
        return await utils.answer(message, text + response["replies"][-1])
                
        
        
        
            