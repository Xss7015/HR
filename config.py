import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
GROUP_LINK_RU = os.getenv("GROUP_LINK_RU", "https://t.me/+XXXXXXXXX")
GROUP_LINK_EN = os.getenv("GROUP_LINK_EN", "https://t.me/+YYYYYYYYY")
GROUP_LINK_HE = os.getenv("GROUP_LINK_HE", "https://t.me/+ZZZZZZZZZ")