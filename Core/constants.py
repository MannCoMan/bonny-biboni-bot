"""
Base constants class
"""
import os


class Const:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BOT_TOKEN = "NDMzMzgzOTM2NDI1NzIxODYx.XYeupg.qqfbFKXCHTONOw1UKCFHvo3TGBo"

    ADMINS_ROLES = (
        "Министерство Информации",
        "Министерство Культуры",
        "Министерство Обороны",
    )

    BOTS_ROLES = (
        "Радио",
        "Groovy",
        "Rhytm",
        "Rhytm 2",
    )

    EMOJI_RESPONSE = (
        ":flushed:", ":relieved:", ":smirk:", 
        ":sunglasses:", ":alien:", ":thinking:"
    )

    BOT_DEFAULT_LOCALE = "en-US"
    BOT_DEFAULT_PREFIX = "-"
    BOT_CASE_SENSITIVE = False

    BOT_REMOVED_COMMANDS = (
        "help",
    )

    BOT_ENABLE_LOGS = False
    BOT_LOG_CHANNELS = {
        "on-command": 601750335052316683,
        "on-command-error": 601750242786017300,
    }

    BOT_STATUS_TIMER = 1800

    BOT_GAME_STATUSES = (
        "Включайте свою камеру для вирт. секса",
        "Привет! Ты откуда?)))",
        "Ч У Ш Ь",
        "mom found my poop sock",
        ":doge:",
        "ты лох",
    )

    BOT_DEV_STATUSES = (
        "/dev/",
    )

    BOT_GREET_MESSAGES = (
        "Henlo",
    )
    BOT_RESTART_CLEAR_CONSOLE = True
    OS_CLR = {
        "win32":  "cls",
        "linux":  "clear",
        "darwin": "clear",
    }

    MODS = [
        "Mods.Tools.tools",
        "Mods.Fun.fun",
    ]

    BOT_ENABLE_DEV_MODE = False

    DEVMODE_MODS = (
        "Mods.Tools",
    )

    FOLDERS = [
        "Data",
        "Logs",
        "Images/Temp",
    ]

    COLORS = {
        "orange": 0xffae00,
        "purple": 0xe200ff,
        "red": 0xff0000,
        "magenta": 0xb620fc,
        "blue": 0x2027fc,
        "cyan": 0x00f6ff,
        "dark-orange": 0xc66300,
        "dark-red": 0x750000,
        "dark-magenta": 0x821f91,
        "dark-blue": 0x99ccff,
        "dark-cyan": 0x216a77,
    }

