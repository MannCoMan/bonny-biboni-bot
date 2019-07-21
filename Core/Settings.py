import os, time


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Bot token
BOT_TOKEN = ""

# Bot profile pic
BOT_PROFILE_PICTURE = "https://cdn.discordapp.com/app-icons/433383936425721861/22ada08bd209e314caf1938156a7b808.png?size=512"

# Bot documentaion
DOCS_LINK = "https://docs.google.com/document/d/1MsD0cZyTKnLoJppLjcbASF8WsQQT-8Q2Eumaazw4CUQ/edit?usp=sharing"

# Roles stuff
# Admin roles
ADMIN_ROLES = (
	"Министерство Информации",
	"Министерство Культуры",
	"Министерство Обороны",
)

# Other bots
BOTS_ROLES = (
	"Радио",
	"Groovy",
	"Rhytm",
	"Rhytm 2",
)

# Bot locale
BOT_LOCALE = "ru_ru"

LOCALE_FILES = (
	("ru_ru", "Locales/ru_ru.json"),
)

# Bot command prefix
# <prefifx> [command]
BOT_COMMAND_PREFIX = "биба "

# Bot case sensetive
BOT_CASE_SENSETIVE = False

# Remove standard commands
BOT_REMOVED_COMMANDS = (
	"help",
)

BOT_LOG_CHANNELS = {
	"on_message": 601750600195112971,
	"on_command": 601750335052316683,
	"on_command_error": 601750242786017300,
}

# Force bot to send errors and logs to `BOT_LOG_CHANNEL`
BOT_ENABLE_LOGS = False

# Status stuff
# All statuses
BOT_GAME_STATUSES = [
	"Включайте свою камеру для вирт. секса",
	"Привет! Ты откуда?)))",
	"Ч У Ш Ь",
	"mom found my poop sock",
	":doge:",
	"ты лох",
]

# In mil. seconds
BOT_STATUS_TIMER = 1800


# System stuff
# Bot enable greet
BOT_AUTOSTART_GREET = False

# Bot greetings
BOT_GREET_MESSAGES = [
	# f"Здарова бандиты: *{time.strftime('%d.%m.%y-%H:%M:%S', time.gmtime())}*",
	"Здарова бандиты :doge:",
]

# Clear console/terminal after `restart` command
BOT_RESTART_CLEAR_CONSOLE = True

# Specify which clear method bot need to use
OS_CLR = {
	"win32":  "cls",
	"linux":  "clear",
	"darwin": "clear",
}

# Modules
MODS = [
	"Mods.Tools.Tools",
	"Mods.Fun.Fun",
	# "Mods.Games",
	# "Mods.ASCII",
]


# Dev Mode stuff
BOT_DEV_MODE_STATUS = (
	"DEV MODE",
)

BOT_ENABLE_DEV_MODE = False

DEVMODE_MODS = [
	"Mods.Tools",
]


# Fonts
FONTS_ROOT = os.path.join(BASE_DIR, "Fonts")
FONTS = {
	"impact": os.path.join(FONTS_ROOT, "impact", "impact.ttf"),
	"arial": os.path.join(FONTS_ROOT, "arial", "arial.ttf"),
}


# Images
IMAGES_PATH = os.path.join(BASE_DIR, "Images")
IMAGES_TMP_PATH = os.path.join(IMAGES_PATH, "Temp")
IMAGES_TEMPLATE_PATH = os.path.join(IMAGES_PATH, "PNG")


# Colors
COLORS = {
	"orange": 0xffae00,
	"purple": 0xe200ff,
	"red": 0xff0000,
	"magenta": 0xb620fc,
	"blue": 0x2027fc,
	"cyan": 0x00f6ff,
	"drk_orange": 0xc66300,
	"drk_red": 0x750000,
	"drk_magenta": 0x821f91,
	"drk_blue": 0x99ccff,
	"drk_cyan": 0x216a77,
}


# Imgur
IMGUR_CLIEND_ID = ""
IMGUR_CLIENT_SECRET = ""