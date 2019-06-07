from telegram.ext import Updater
from secrets import bot_token, api_hash, api_id
from pyrogram import Client
from servant_handlers import new_post_handler
upd = Updater(bot_token,
              use_context=True)

dp = upd.dispatcher

servant = Client("xakep_servant",
                 api_hash=api_hash,
                 api_id=api_id)


def main():

    servant.add_handler(new_post_handler)
    servant.run()



if __name__ == '__main__':
    main()
