from telethon import TelegramClient, events, sync
from telethon.tl.types import InputChannel
import sys
import logging
from app import config
import app.utils.db as db_utils
import asyncio
from time import sleep


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('telethon').setLevel(level=logging.WARNING)
logger = logging.getLogger(__name__)

def select_news(last_id):
    db_utils.select_news(last_id)
            
def start():
    sleep(60)
    
    client = TelegramClient(config.telegram["session_name"], 
                            config.telegram["api_id"], 
                            config.telegram["api_hash"])
    client.start()

    channel_found=False
    for d in client.iter_dialogs():
        if d.name == config.channel["name"] or d.entity.id == config.channel["id"]:
            #output_channel=InputChannel(d.entity.id, d.entity.access_hash)
            logging.info('Channel found')
            channel_found=True
            break
    
    if not channel_found:
        logging.error('Channel not found')
        return
        
    async def send_news():
        last_id = None
        while True:
            logging.info('Reading data from DB')
            news = db_utils.select_news(last_id)
            
            if news.shape[0]>0:
                last_id = news.id.max()
                logging.info('Writing data to channel')
                
                for ix,row in news.iterrows():
                    msg = f"{row.title}\n{row.href}"
                    await client.send_message(config.channel["id"], msg)
            
            await asyncio.sleep(config.read_delay)
        
    client.loop.run_until_complete(send_news())
            

if __name__ == "__main__":
    start()
