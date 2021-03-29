#=========================INIT SECTION=======================
import telebot,requests
token = "1096796260:AAFKx0T2epThNTo_Exr1muSCS5vjo1r0BiM"
bot = telebot.TeleBot(token=token,threaded=False)


#=========================REQUESTS SECTION=======================
def quote():
	response = requests.get("http://public-restapi.herokuapp.com/api/quote-generator")
	results = response.json()
	return results["quote"]

def wiki(q):
	response = requests.get(f"http://public-restapi.herokuapp.com/api/wiki-pedia?q={q}")
	results = response.json()
	key = list(results["query"]["pages"].keys())[0]
	return results["query"]["pages"][key]["extract"]

def translate2id(text):
	response = requests.get(f"http://public-restapi.herokuapp.com/api/translate?text={text}&to=id")
	results = response.json()
	return results["success"]

def translate2en(text):
	response = requests.get(f"http://public-restapi.herokuapp.com/api/translate?text={text}&to=en")
	results = response.json()
	return results["success"]

def simsimi(text):
	response = requests.get(f"https://api.simsimi.net/v1/?text={text}&lang=id")
	results = response.json()
	return results["success"]

def anime():
	response = requests.get("http://public-restapi.herokuapp.com/api/anime-random-image")
	results = response.json()
	return results["image"]


#=========================MESSAGE SECTION=======================
@bot.message_handler(commands=["start"])
def welcome(message):
	# print(message)
	nama = message.from_user.first_name
	pesan = f"Halo {nama} selamat bergabung."
	markup = telebot.types.InlineKeyboardMarkup()

	btnQuote = telebot.types.InlineKeyboardButton("Quote💭", callback_data='/quote')
	btnWiki = telebot.types.InlineKeyboardButton("Wikipedia🌎", callback_data='/wikipedia')
	btnAnime = telebot.types.InlineKeyboardButton("Random Anime🖼", callback_data='/anime')
	btnToid = telebot.types.InlineKeyboardButton("Translate to 🇮🇩", callback_data='/toid')
	btnToen = telebot.types.InlineKeyboardButton("Translate to 🏴󠁧󠁢󠁥󠁮󠁧󠁿", callback_data='/toen')

	markup.row(btnQuote,btnWiki,btnAnime)
	markup.row(btnToid,btnToen)
	bot.send_message(message.from_user.id,pesan,reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text is not None)
def other(message):
	pesan = simsimi(message.text)
	bot.reply_to(message,pesan)


#=========================CALLBACK SECTION=======================
@bot.callback_query_handler(func=lambda msg: msg.data == '/quote')
def cbquote(message):
	pesan = f'<i>"{quote()}"</i>'
	nx = bot.send_message(message.from_user.id,pesan,parse_mode="HTML")
	bot.register_next_step_handler(nx,nx_quote)

@bot.callback_query_handler(func=lambda msg: msg.data == '/wikipedia')
def cbwiki(message):
	pesan = "Mau cari apa di Wikipedia ?"
	nx = bot.send_message(message.from_user.id,pesan)
	bot.register_next_step_handler(nx,nx_wiki)

@bot.callback_query_handler(func=lambda msg: msg.data == '/anime')
def cbanime(message):
	photo = anime()
	nx = bot.send_photo(message.from_user.id, photo)
	bot.register_next_step_handler(nx,nx_anime)

@bot.callback_query_handler(func=lambda msg: msg.data == '/toid')
def cbid(message):
	pesan = "Translate to Indonesia :"
	nx = bot.send_message(message.from_user.id,pesan)
	bot.register_next_step_handler(nx,nx_id)

@bot.callback_query_handler(func=lambda msg: msg.data == '/toen')
def cben(message):
	pesan = "Translate to English :"
	nx = bot.send_message(message.from_user.id,pesan)
	bot.register_next_step_handler(nx,nx_en)


#=========================NEXT SECTION=======================
def nx_quote(message):
	if "lagi" in message.text.lower() or "more" in message.text.lower():
		pesan = f'<i>"{quote()}"</i>'
		nx = bot.send_message(message.from_user.id,pesan,parse_mode="HTML")
		bot.register_next_step_handler(nx,nx_quote)
	else:
		bot.reply_to(message,"Quote nya keren kan😄")

def nx_wiki(message):
	pesan = wiki(message.text)
	bot.send_message(message.from_user.id,pesan,parse_mode="HTML")

def nx_anime(message):
	if "lagi" in message.text.lower() or "more" in message.text.lower():
		photo = anime()
		nx = bot.send_photo(message.from_user.id, photo)
		bot.register_next_step_handler(nx,nx_anime)
	else:
		bot.reply_to(message,"Photo nya keren kan😄")

def nx_id(message):
	pesan = translate2id(message.text)
	bot.send_message(message.from_user.id,pesan)

def nx_en(message):
	pesan = translate2en(message.text)
	bot.send_message(message.from_user.id,pesan)


#=========================MAIN SECTION=======================
if __name__ == '__main__':
	print("Running..")
	# bot.polling()
	while True:
		try:
			bot.polling()
		except Exception as e:
			bot.stop_polling()