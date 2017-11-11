import Bot
import pymsgbox

bot = Bot.Bot()

bot.Login_With_Google("---", "---")

bot.playMatch('your game name', 'your game id', 10, 0.1)
