from operator import add
import os
import logging
# import dotenv
# dotenv.load_dotenv()
from logging.handlers import RotatingFileHandler

#Api Id/Api Hash/Owner Id/Owner Username or tag
APP_ID = int(os.environ.get("APP_ID", "24828197"))
API_HASH = os.environ.get("API_HASH", "d36e278e89ebeb900aeda4128d413a77")
OWNER_ID = int(os.environ.get("OWNER_ID", "8108281129"))
OWNER_TAG = os.environ.get("OWNER_TAG", "Yae_X_Miko")

#Channel/Force sub
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002381050327"))
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "0"))
FORCE_SUB_CHANNEL2 = int(os.environ.get("FORCE_SUB_CHANNEL2", "0"))

if FORCE_SUB_CHANNEL > FORCE_SUB_CHANNEL2:
    temp = FORCE_SUB_CHANNEL2 
    FORCE_SUB_CHANNEL2 = FORCE_SUB_CHANNEL
    FORCE_SUB_CHANNEL = temp

#Bot Token/Tg Bot Worker/Port
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "7716433955:AAFzXYzLXq8gdftXoohSRkkfQNSZOSpL11s")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))
PORT = os.environ.get("PORT", "6666")

#Database
DB_URL = os.environ.get("DB_URL", "mongodb+srv://munkog:6mOVQ1GqWD5P30XE@cluster245.e2vmr.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DB_NAME", "filestorabot")

#Bot Stats/start Massage/user Reply Text
BOT_STATS_TEXT = os.environ.get("BOTS_STATS_TEXT","<b>BOT UPTIME </b>\n{uptime}")
USER_REPLY_TEXT = os.environ.get("USER_REPLY_TEXT", "Don't send me messages directly I'm only File Share bot! ")
START_MSG = os.environ.get("START_MESSAGE", "Hello {first}\n\nI can store private files in Specified Channel and other users can access it from special link. ")

#Time in seconds for message delete, put 0 to never delete
TIME = int(os.environ.get("TIME", "57600"))
#Shortner (token system) 
"""
some token verification sites
https://dashboard.shareus.io/
"""
# Turn this feature on or off using True or False put value inside  ""
# TRUE for yes FALSE if no 
USE_SHORTLINK = True if os.environ.get('USE_SHORTLINK', "TRUE") == "TRUE" else False 
# only shareus service known rightnow rest you can test on your own
SHORTLINK_API_URL = os.environ.get("SHORTLINK_API_URL", "modijiurl.com")
# SHORTLINK_API_KEY = os.environ.get("SHORTLINK_API_KEY", "971a7eef7f38784d7cb5accdc2a4ad044c87e25d")
SHORTLINK_API_KEY = os.environ.get("SHORTLINK_API_KEY", "971a7eef7f38784d7cb5accdc2a4ad044c87e25d")
#add your custom time in secs for shortlink expiration.
# 24hr = 86400
# 12hr = 43200
VERIFY_EXPIRE = int(os.environ.get('VERIFY_EXPIRE', "86400")) # Add time in seconds
#put TRUE if you want shortner in every link generated by the bot.
U_S_E_P = True if (True if os.environ.get('U_S_E_P', "True") == "TRUE" else False) and (USE_SHORTLINK) else False
#Tutorial video for the user of your shortner on how to download.
TUT_VID = os.environ.get("TUT_VID","https://t.me/middlenightdiaries/10")

#Payment to remove the token system
#put TRUE if you want this feature
USE_PAYMENT = True if (True if os.environ.get("USE_PAYMENT", "TRUE") == "TRUE" else False) and (USE_SHORTLINK) else False
#UPI ID
UPI_ID = os.environ.get("UPI_ID", "xyz@upi")
#UPI QR CODE IMAGE
UPI_IMAGE_URL = os.environ.get("UPI_IMAGE_URL", "https://t.me/powermoviespage/2")
#SCREENSHOT URL of ADMIN for verification of payments
SCREENSHOT_URL = os.environ.get("SCREENSHOT_URL", f"t.me/{OWNER_TAG}")
#Time and its price
#7 Days
PRICE1 = os.environ.get("PRICE1", "20 rs")
#1 Month
PRICE2 = os.environ.get("PRICE2", "49 rs")
#3 Month
PRICE3 = os.environ.get("PRICE3", "135 rs")
#6 Month
PRICE4 = os.environ.get("PRICE4", "250 rs")
#1 Year
PRICE5 = os.environ.get("PRICE5", "500 rs")

#Force Message For Joining The Channel/Custom Caption/Protect Content
FORCE_MSG = os.environ.get("FORCE_MSG", "Hello {first}\n\n<b>You need to join in my Channel/Group to use me\n\nKindly Please join Channel</b> 🥺")
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "<b>• ʙʏ @POWERMODOWNER</b>")
PROTECT_CONTENT = True if os.environ.get("PROTECT_CONTENT", "TRUE") == "TRUE" else False

# True for yes False if no
DISABLE_CHANNEL_BUTTON = True if os.environ.get("DISABLE_CHANNEL_BUTTON", "TRUE") == "TRUE" else False
try:
    ADMINS=[]
    for x in (os.environ.get("ADMINS", "5904478052 ").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

#No Need To Do Anything
ADMINS.append(OWNER_ID)

LOG_FILE_NAME = "logs.txt"
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
