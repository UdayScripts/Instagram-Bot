# MIT License (Same as original)

from pyrogram import Client
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid, UserIsBlocked
import asyncio
import os
from instaloader import Instaloader, TwoFactorAuthRequiredException

# Predefined Values (Replace with your details)
API_ID = 26383754  # Replace with your Telegram API_ID
API_HASH = "f743596f09f383e7bbcc62ce62367f06"  # Replace with your Telegram API_HASH
BOT_TOKEN = "8183335872:AAEndw3eTG-F_UakwMzX6WVOD1kDFFwSIHc"  # Replace with your Telegram Bot Token
TELEGRAM_ID = 1489381549  # Replace with your Telegram ID (Integer)
INSTA_USERNAME = "udayscripts"  # Replace with your Instagram username
INSTA_PASSWORD = "###@UDAY1"  # Replace with your Instagram password

L = Instaloader()


async def generate():
    bot = Client("INSTASESSION", API_ID, API_HASH, bot_token=BOT_TOKEN)
    await bot.start()

    try:
        L.login(INSTA_USERNAME, INSTA_PASSWORD)
        L.save_session_to_file(filename=f"./{INSTA_USERNAME}")
    except TwoFactorAuthRequiredException:
        print("Your account has Two-Factor Authentication enabled.")
        code = input("Enter the 2FA code received on your mobile: ")
        L.two_factor_login(code)
        L.save_session_to_file(filename=f"./{INSTA_USERNAME}")
    except Exception as e:
        print(f"Login Error: {e}")
        return

    print("Successfully Logged into Instagram")

    try:
        f = await bot.send_document(
            chat_id=TELEGRAM_ID,
            document=f"./{INSTA_USERNAME}",
            file_name=f"{INSTA_USERNAME}_session",
            caption="⚠️ KEEP THIS SESSION FILE SAFE AND DO NOT SHARE WITH ANYBODY",
        )
        file_id = f.document.file_id
        await bot.send_message(
            chat_id=TELEGRAM_ID,
            text=f"Here is Your <code>INSTA_SESSIONFILE_ID</code>\n\n<code>{file_id}</code>\n\n⚠️ KEEP THIS SESSION FILE SAFE AND DO NOT SHARE WITH ANYBODY",
        )
        print("Session file sent successfully.")
    except PeerIdInvalid:
        print("ERROR: Invalid Telegram ID or bot not started. Send /start to the bot and try again.")
    except UserIsBlocked:
        print("ERROR: Bot is blocked. Unblock it and try again.")
    except Exception as e:
        print(f"Telegram Error: {e}")

    await bot.stop()
    os.remove(f"./{INSTA_USERNAME}")
    os.remove("INSTASESSION.session")


loop = asyncio.get_event_loop()
loop.run_until_complete(generate())
