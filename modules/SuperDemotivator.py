from .. import loader, utils
import logging
from PIL import Image, ImageDraw, ImageOps, ImageFont
from textwrap import wrap
import io
import requests
from random import choice
# https://t.me/KeyZenD
# https://t.me/SomeScripts
logger = logging.getLogger(__name__)

@loader.tds
class DeMoTiVaToRsMod(loader.Module):
	"""Демотиватори на картинки від @SomeScripts by @DneZyeK"""
	strings = {
		"name": "SuperDemotivator"
	}

	async def client_ready(self, client, db):
		self.client = client
	
	
	@loader.owner
	async def demoticmd(self, message):
		"""текст + фото або відповідь на фото
           не мне фотки"""
		await cmds(message, 0)
		
	async def demotcmd(self, message):
		"""текст + фото або відповідь на фото
           мне фотки"""
		await cmds(message, 1)
		
	
async def cmds(message, type):
	event, is_reply = await check_media(message)
	if not event:
		await message.edit("<b>Відповідь командою на зображення!</b>")
		return
	text = utils.get_args_raw(message)
	
	if not text:
		text = choice(tttxxx)
		
	await message.edit("<b>Демотивую...</b>")
	bytes_image = await event.download_media(bytes)
	demotivator = await demotion(font_bytes, bytes_image, text, type)
	if is_reply:
		await message.delete()
		return await event.reply(file=demotivator)
		
	else:
		return await event.edit(file=demotivator, text="")
	
		
async def check_media(message):
	reply = await message.get_reply_message()
	is_reply = True
	if not reply:
		reply = message
		is_reply = False
	if not reply.file:
		return False, ...
	mime = reply.file.mime_type.split("/")[0].lower()
	if mime != "image":
		return False, ...
	return reply, is_reply
	
async def textwrap(text, length=50, splitter = "\n\n"):
	out = []
	
	lines = text.rsplit(splitter, 1)
	for text in lines:
		txt = []
		parts = text.split("\n")
		for part in parts:
			part = "\n".join(wrap(part, length))
			txt.append(part)
		text = "\n".join(txt)
		out.append(text)
	return out

async def draw_main(
			bytes_image,
			type,
			frame_width_1 = 5,
			frame_fill_1 = (0, 0, 0),
			frame_width_2 = 3,
			frame_fill_2 = (255, 255, 255),
			expand_proc = 10,
			main_fill = (0, 0, 0)
			):
				
	main_ = Image.open(io.BytesIO(bytes_image))
	main = Image.new("RGB", main_.size, "black")
	main.paste(main_, (0, 0))
	if type == 1:
		main = main.resize((700, 550))
	main = ImageOps.expand(main, frame_width_1, frame_fill_1)
	main = ImageOps.expand(main, frame_width_2, frame_fill_2)
	w, h = main.size
	h_up = expand_proc*(h//100)
	im = Image.new("RGB", (w+(h_up*2), h+h_up), main_fill)
	im.paste(main, (h_up, h_up))
	return im

async def _draw_text(
			text,
			font_bytes,
			font_size,
			font_add = 20,
			main_fill = (0, 0, 0),
			text_fill = (255, 255, 255),
			text_align = "center"
			):
				
	font = ImageFont.truetype(io.BytesIO(font_bytes), font_size)
	w_txt, h_txt = ImageDraw.Draw(Image.new("RGB", (1, 1))).multiline_textsize(text=text, font=font)
	txt = Image.new("RGB", (w_txt, h_txt+font_add), main_fill)
	ImageDraw.Draw(txt).text((0, 0), text=text, font=font, fill=text_fill, align=text_align)
	return txt
	
async def text_joiner(text_img_1, text_img_2, main_fill = (0, 0, 0)):
	w_txt_1, h_txt_1 = text_img_1.size
	w_txt_2, h_txt_2 = text_img_2.size
	w = max(w_txt_1, w_txt_2)
	h = h_txt_1 + h_txt_2
	text = Image.new("RGB", (w, h), main_fill)
	text.paste(text_img_1, ((w-w_txt_1)//2, 0))
	text.paste(text_img_2, ((w-w_txt_2)//2, h_txt_1))
	return text
	
async def draw_text(text, font_bytes, font_size):
	text = await textwrap(text)
	if len(text) == 1:
		text = await _draw_text(text[0], font_bytes, font_size[0] )
	else:
		text_img_1 = await _draw_text(text[ 0], font_bytes, font_size[0])
		text_img_2 = await _draw_text(text[-1], font_bytes, font_size[1])
		text = await text_joiner(text_img_1, text_img_2)
	return text
	
async def text_finaller(text, main, expand_width_proc = 25, main_fill = (0, 0, 0)):
	x = min(main.size)
	w_txt, h_txt = text.size
	w_proc = expand_width_proc*(w_txt//100)
	h_proc = expand_width_proc*(h_txt//100)
	back = Image.new("RGB", (w_txt+(w_proc*2), h_txt+(h_proc*2)), main_fill)
	back.paste(text, (w_proc, h_proc))
	back.thumbnail((x, x))
	return back
	
	
async def joiner(text_img, main_img, format_save="JPEG"):
	w_im, h_im = main_img.size
	w_txt, h_txt = text_img.size
	text_img.thumbnail((min(w_im, h_im), min(w_im, h_im)))
	w_txt, h_txt = text_img.size
	main_img = main_img.crop((0, 0, w_im, h_im+h_txt))
	main_img.paste(text_img, ((w_im-w_txt)//2, h_im))
	output = io.BytesIO()
	main_img.save(output, format_save)
	output.seek(0)
	return output.getvalue()
	
async def demotion(font_bytes, bytes_image, text, type):
	main = await draw_main(bytes_image, type)
	font_size = [20*(min(main.size)//100), 15*(min(main.size)//100)]
	text = await draw_text(text, font_bytes, font_size)
	text = await text_finaller(text, main)
	output = await joiner(text, main)
	return output
tttxxx = ['А чо', 'змушує замислитися', 'Шкода пацана', 'ти че сука??', 'ААХАХАХАХАХАХАХААХАХА\n\n\ААХАХАХАХАХАХАХАХА', 'ГІГАНТ МИСЛІ\n\потець російської демократії', 'Він', 'ЩО БЛЯТТТЯ?', 'охуєнна тема', 'Он вони\n\птипові комедиклабовские жарти', 'АЛЕ НЕ БЛЯДИНА? ', 'Впізнали?', 'Згодні?', 'Ось це мужик', 'ЇЇ ІДЕЇ\n\n\пбудуть актуальні завжди', '\n\пПРИ СТАЛІНІ ВІН би сидів', 'про вадима', '2 місяці на дваче\n\ппі це, блядь, ніхуя не смішно', 'Що далі? \n\n\пЧайник з функцією жопа?', '\n\n\пІ нахуя мені ця інформація?', 'Верхній текст', 'нижній текст', 'Здалося', 'Суди за анкапи', 'Хуйло з району\n\n\n\птака наволоч з одного стусана ляже', 'Брух', 'Розкажи їм\n\пкак ти втомився в офісі', 'Недопалок бляха\n\п\песть 2 рублі? ', 'Аніме стало легендою', 'СМІРИСЬ\n\n\n\n\n\n\пти ніколи не станеш настільки ж крутим', 'але ж це ідея', '\n\пЯкщо не лайкнеш у тебе немає серця', 'Замість тисячі слів', 'ШАХ І МАТ!!! ', 'Найбільший член у світі\n\n\nУ цієї дівчини', 'Трохи\n\n\пперфекціонізму', 'хто', '\n\n\nця сука забирає чужих чоловіків', 'Хто він???', '\n\nВи теж хотіли насрати туди в дитинстві? ', '\n\n\nВся суть сучасного суспільства\n\n\пв одному фото', 'Він обов'язково виживе!', '\n\nВи теж хочете подрочити йому?', '\n\nІ ось цій хуйні поклоняються росіяни?', 'Ось вона суть\n\n\n\n\nлюдського суспільства в одній картинці', 'Ви думали це рофл? \n\n\пНі це жопа', '\n\nПри Сталіні такої хуйні не було\n\пА у вас було?', 'Він гриз дроти', 'На зло старим\n\n\пна радість онаністам', 'Десь у Челябінську', 'Агітація за Порошенка', 'ІДЕАЛЬНО', 'Гриз? ', 'Ну давай розкажи їм\n\пкакакака в тебе важка робота', '\n\пЖелаю в кожному домі такого гостя', 'Шкура на виріст', 'НІКОЛИ\n\пне здавайся', 'Оппа гангнам стайл\n\пууууусексі лейді оп оп оп', 'Вони зробили це\n\псучі діти, вони впорались', 'Ця сука\n\пхоче грошей', 'Це гівно, а ти? ', '\n\n\nОсь вона нинішня молодь', 'Погладь кота\n\n\nпогладь кота сука', 'Я обов'язково виживу', '\n\nОсь вона, справжня чоловіча дружба\n\n\пбез політики і ліцимерії', '\n\n\nПРИКРАСНО ЩО Я ЖИВУ В КРАЇНІ\n\n\пде гантелі коштують у 20 разів дорожче ніж пляшка горілки', 'Цар, просто цар', '\n\nНахуй ви це в підручники вставили? \n\n\пІ ще їбану контрольну влаштували', '\n\пЦЕ СПРАВЖНЯ КРАСА\n\па не ваші голі бляді', '\n\пТему розкрито ПОВНІСТЮ', '\n\пРОСІЯ, ЯКУ МИ ВТРАТИЛИ', 'ЦЕ - Я\n\пПОПОДУМАЙ МОЖЕ ЦЕ ТИ', 'чому\n\n\пщо чому', 'КУПИТИ БИ ДЖИП\n\пБЛЯТЬ ТА НАХУЙ ТРЕБА', '\n\n\n\n\пми не продаємо бомбастер особам, старшим за 12 років', 'МРАЗЯ', 'Правильна аерографія', 'Ось вона російська\n\n\пСМЕКАЛОЧКА', 'Він взяв рехстаг! \n\пА чого домігся ти? ', 'На аватарку', 'Фотошоп по-селянськи', 'Інструкція в літаку', 'Цирк дю Солей', 'Смак дитинства\n\пшколоті не зрозуміти', 'Ось воно - ЩАСЛИВО', 'Він за тебе воював\n\п\па ти навіть не знаєш його імені', 'Зате не за комп'ютером', '\n\n\пНе чіпай це на новий рік', 'Мій перший малюнок\n\n\пмочею на снігу', '\n\пТравневі свята на дачі', 'Ваш піздюк? ', 'Тест драйв підгузків', 'Не розумію\n\пкак це взагалі виросло?', 'Супермен в СРСР', 'Єдиний\n\н\пхто тобі радий', 'Макдональдс відпочиває', 'Ну че\n\n\n як справи на роботі пацани? ', 'Вся суть стосунків', 'Білоруси, спасибі!', '\n\пПід дверима узбецького військкомату', 'Замість 1000 слів', 'Одне запитання\n\пнахуя?', 'Відповідь на санкції\n\пЄВРОПИ', 'ЦИганські фокуси', 'Блядь! \n\пда він геній! ', '\n\n\пУкраїна шукає нові джерела газу', 'ОСЬ ЦЕ\n\n\пСПРАВЖНІ КОЗАКИ а не ряджені', 'Нового року не буде\n\пСанта прийняв Іслам', '\n\пВін був проти наркотиків\n\пта ти й далі вбивай себе', 'Всім похуй! \n\n\пВсім похуй!', 'БРАТЯ СЛАВ'ЯНИ\n\п пам'ятайте один про одного', '\n\пОН ВИГАДАВ ГІБНЯ\n\п ти навіть не знаєш його імені', '\n\пкороткий курс історії нацболів', 'Епоха ренесансу']
font_bytes = requests.get("https://raw.githubusercontent.com/KeyZenD/l/master/times.ttf").content
#######################
