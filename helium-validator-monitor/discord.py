import logger
from os import getenv
from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv

log = logger.get_logger(__name__)

load_dotenv() #Check Environment Variables in .env file
webhook_url = getenv('DISCORD_CHANNEL_WEBHOOK_URL')
webhook = DiscordWebhook(url=webhook_url) #Discord WebHook URL

SUCCESS_COLOR = '0x22bb33'
FAILURE_COLOR = '0xbb2124'

def send_status_message(validator_name, validator_explorer, validator_status):
    embed = None
    if validator_status == 'online':
        embed = DiscordEmbed(title=f'{validator_name}', url=validator_explorer, color=SUCCESS_COLOR)
        embed.add_embed_field(name="Status Check", value="ONLINE", inline=False)
    else:
        webhook.set_content('@everyone')
        embed = DiscordEmbed(title=f'{validator_name}', url=validator_explorer, color=FAILURE_COLOR)
        embed.add_embed_field(name="Status Check", value="OFFLINE", inline=False) 
       
    webhook.add_embed(embed)
    response = webhook.execute(remove_embeds=True)
    log.debug("Discord message sent: {}".format(response))