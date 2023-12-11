import discord
import os
import random
import secrets
import asyncio
from keep_alive import keep_alive

intents = discord.Intents.all()
intents.typing = True
client = discord.Client(intents=intents)

#all the used data for the bot. Was too lazy to add a database.
pozdravy = [
    "ahoj", "čus", "zdar", "zduř", "čau", "zdravím", "hola", "nazdar", "těpic",
    "nazdárek", "ello"
]
jakje = ["jak je", "jak se vede", "jak to jde"]
nudes = [
    "nudes", "send nudes", "sex", "fekf", "sekz", "dáme sex", "dáme fekf",
    "dáme sekz"
]
cali = ["caly", "caloň", "calys", "cali", "calis", "caldo", "calinádo"]
request_queue = asyncio.Queue()
response_dict = {
    tuple(pozdravy):
    "Krásný dobrý den vám přeji!",
    "здравствуйте":
    "Хорошего дня товарищи! <:KKomrade:705045404059959367>",
    "kekw":
    "<:KEKW:705021797623660604> vám přeji!",
    "sieg heil":
    "<:agrWeird:705049870385545367>",
    tuple(jakje):
    "Stojí to za hovno, děkuji za optání",
    tuple(nudes):
    "https://static.wikia.nocookie.net/hedgecomic/images/c/ce/Vernevg.png/revision/latest/scale-to-width-down/250?cb=20130712010321",
}
russian_roulette_safe = [
    " se málem dosral",
    " už byl smířený, ale nakonec je safe",
    " měl teď namále",
    " ani sebou necuknul",
    " se málem zhroutil",
    " už to chtěl mít za sebou, ale má smůlu",
    " opět potvrzuje, že má koule z oceli",
    " to actually přežil <:Pog:705046932518600754>",
    " se už loučil",
    " na chvilku zapomněl, že tam je kulka, ale žije",
]
occupied = False


@client.event
async def on_ready():
  print("Nemám ponětí, co dělám {}".format(client))


@client.event
async def on_message(message):
  #used so the bot doesn't respond to itself
  if message.author == client.user:
    return
  #to prevent handling multiple requests at once (spam). Could make a queue later
  global occupied
  if occupied:
    return
  occupied = True

  #for case insensitive comparisons
  msg = message.content.lower()

  #goes through a list of possible ways the bot can be called
  #then responds to the message by utilizing a dictionary
  if any(calys in msg for calys in cali):
    for response in response_dict:
      if msg.startswith(response):
        await message.channel.send(response_dict[response])
        
  #russian roulette - cyllinder spun after kill variation
  if msg.startswith("rr"):
    #an attempt to make it as random as possible
    mentioned_people = message.mentions
    random.shuffle(mentioned_people)
    count = 0
    hit = secrets.randbelow(6)
    
    await asyncio.sleep(1)
    #goes till there isn't only 1 contestant in list left
    while len(mentioned_people) != 1:
      #variable for the current player to mention him
      on_turn = str(message.mentions[(count % len(mentioned_people))].mention)
      #if it equals, it hits, otherwise a goofy response gets called
      if count % 6 == hit:
        await message.channel.send(on_turn + ":boom::saluting_face:")
        #deletes, changes value for next round and shuffles them all again
        hit = secrets.randbelow(6)
        del mentioned_people[count % len(mentioned_people)]
        random.shuffle(mentioned_people)
      else:
        await message.channel.send(
            on_turn + russian_roulette_safe[secrets.randbelow(10)])
      count += 1
      await asyncio.sleep(1)
    #when the loop finishes, the last person gets a confirmation he won
    await message.channel.send("Victory royale: :crown:" +
                               mentioned_people[0].mention + ":crown:")
    
  occupied = False

#to run the bot
bot_token = os.getenv('BOT_TOKEN')
keep_alive()
if bot_token is None:
  print("Error: BOT_TOKEN not existent")
else:
  client.run(bot_token)
