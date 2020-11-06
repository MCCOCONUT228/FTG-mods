from telethon import events
from .. import loader, utils
import os
import requests
from PIL import Image,ImageFont,ImageDraw
import re
import io
from textwrap import wrap

def register(cb):
	cb(AverageMod())

class AverageMod(loader.Module):
	"""Любителизатор"""
	strings = {
		'name': 'Любителизатор',
		'usage': 'Напиши <code>.help Любителизатор</code>',
	}
	def __init__(self):
		self.name = self.strings['name']
		self._me = None
		self._ratelimit = []
	async def client_ready(self, client, db):
		self._client = client

	async def acmd(self, message):
		""".a <реплай на сообщение/свой текст>"""

		ufr = requests.get("https://github.com/LaciaMemeFrame/FTG-Modules/blob/master/open-sans.ttf?raw=true")
		f = ufr.content

		reply = await message.get_reply_message()
		args = utils.get_args_raw(message)
		if not args:
			if not reply:
				await utils.answer(message, self.strings('usage', message))
				return
			else:
				txt = reply.raw_text
		else:
			txt = utils.get_args_raw(message)
		await message.edit("<b>Извинись, быдло...</b>")
		pic = requests.get("https://raw.githubusercontent.com/MCCOCONUT228/FTG-mods/master/enjoyer.png")
		pic.raw.decode_content = True
		img = Image.open(io.BytesIO(pic.content)).convert("RGB")

		W, H = img.size
		text = message.text
		tf = text[4:text.find("&")]
		ts = text[text.find("&")+1:len(text)]
		draw = ImageDraw.Draw(img)
		font = ImageFont.truetype(io.BytesIO(f), 14, encoding='UTF-8')
		imtext = Image.new("RGBA", (W+10, H+10), (0, 0,0,0))
		draw = ImageDraw.Draw(imtext)
		draw.text((10, 10),tf,(0,0,0),font=font, align='left')
		draw.text((340, 10),ts,(0,0,0),font=font, align='left')
		imtext.thumbnail((680, 501))
		img.paste(imtext, (10,10), imtext)
		out = io.BytesIO()
		out.name = "enjoyer.jpg"
		img.save(out)
		out.seek(0)
		await message.client.send_file(message.to_id, out, reply_to=reply)
		await message.delete()
