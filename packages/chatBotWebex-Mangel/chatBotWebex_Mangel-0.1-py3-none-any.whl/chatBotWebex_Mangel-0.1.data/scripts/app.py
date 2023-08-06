from decouple import config
from webex_bot.webex_bot import WebexBot
from commands.firstCommand import firstCommand
from commands.filterCommand import filterCommand
from commands.siteFilterCommand import siteFilterCommand
from commands.finishCommad import finishCommad


token = config('WEBEX_TOKEN')

bot = WebexBot(token)

bot.add_command(firstCommand())
bot.add_command(siteFilterCommand())
bot.add_command(filterCommand())
bot.add_command(finishCommad())

bot.run()