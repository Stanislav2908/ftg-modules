from .. import loader, utils
from SimpleQIWI import QApi
def register(cb):
    cb(qiwiMod())
class qiwiMod(loader.Module):
    """получаем инфу о киви"""
    strings = {'name': 'Mini Qiwi Helper'}
    async def client_ready(self, client, db):
        self.db = db
        self.client = client
    async def setqiwinumbercmd(self, message):
        '''поставить номер киви'''
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, "<b>а что ставить то?</b>")
        self.db.set("qiwi", "number", args)
        return await utils.answer(message, "<b>да, поставил</b>")
    async def setqiwitokencmd(self, message):
        '''поставить токен киви'''
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, "<b>а что ставить то?</b>")
        self.db.set("qiwi", "token", args)
        return await utils.answer(message, "<b>да, поставил</b>")
    async def qiwicmd(self, message):
        '''отправляем инфу про киви'''
        number = self.db.get("qiwi", "number")
        token = self.db.get("qiwi", "token")
        if not number or not token:
            return await utils.answer(message, "ты забыл что-то заполнить")
        data = {
            "643": "RUB",
            "840": "USD",
            "978": "EUR",
            "398": "KZT"
        }
        balances = []
        api = QApi(token=token, phone=number)
        try:
            a = api.full_balance
        except:
            return await utils.answer(message, "ты что-то криво заполнил")
        for i in a:
            x = i['balance']
            balance = str(x['amount'])+" "+data[str(x['currency'])]
            balances.append(balance)
        bl = "\n".join(balances)
        try:
            pp = api.payments['data'][0]
        except:
            return await utils.answer(message, "ты что-то криво заполнил")
        ppnum = pp['account']
        replaced = ppnum[5]+ppnum[6]+ppnum[7]+ppnum[8]+ppnum[9]
        ppnum = ppnum.replace(replaced, '*'*len(replaced))
        pp = "💸 <b>Последнee получение денег:</b>\n<code>"+ppnum+" - "+str(pp['sum']['amount'])+" "+data[str(pp['sum']['currency'])]+"</code>"
        itog = "💰 <b>Мой баланс QIWI:</b>\n<code>"+bl+"</code>\n\n"+pp
        await utils.answer(message, itog)
    async def sendqiwicmd(self, message):
        '''отправляем денюжку'''
        number = self.db.get("qiwi", "number")
        token = self.db.get("qiwi", "token")
        args = utils.get_args_raw(message)
        if not number or not token or not args:
            return await utils.answer(message, "ты забыл что-то заполнить или у тебя пустые аргументы")
        sendto = utils.get_args(message)[0]
        sendamount = utils.get_args(message)[1]
        comment = args.split(sendamount)[1] or ''
        api = QApi(token=token, phone=number)
        if not sendto or not sendamount or not sendamount.isdigit():
            return await utils.answer(message, "ты забыл что-то заполнить или у тебя пустые/кривые аргументы")
        try:
            api.pay(account=sendto, amount=int(sendamount), comment=comment)
        except:
            return await utils.answer(message, "❌ <b>Не удалось перевести деньги!</b>")
        return await utils.answer(message, "💸 <b>Перевёл успешно!</b>")