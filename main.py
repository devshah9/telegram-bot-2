import re
from binance.client import Client as bicl
from telethon import TelegramClient, events
import os
import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                   level=logging.INFO)


api_key = 'LbH9EPv3jCfo4vj1qXGmIs0OCLvzAh5dUnkArPiWnr0Il3YxSH5OCAb6PzrrOyvN'
api_secret = 'cKd0P6B1tREL9v9mG9WGaaoLKuG6chPO6zfyortQsGXF02mrfcqNeZhSi7bjimAR'
binance_client_api = bicl(api_key, api_secret)


api_id = 5911805
api_hash = 'baf59bae0d7caba308cdada2079670c2'

INPUT = [1433774445]
OUTPUT = -1001183431565


client = TelegramClient("forward", api_id, api_hash)





def change_text(text):
    # text = '#BEL_USDT Scalp Long!!!\n\nEntry Zone:2270 & 2050\n\nSell Target:2295-2320-2400-2600-3000\n\nStopLoss : 1H Close Under 1950\n\nLev: Cross With (25-50)x Lev\n\nExchange : Binance Futures'

    final_output = ''

    # To find the stock 
    symbol_search = re.search(r"(#)(\w+)[_](\w+)", text)
    symbol_to_check = symbol_search.group(2) + symbol_search.group(3) 


    # To find the price of stock 
    info = binance_client_api.get_symbol_ticker(symbol=symbol_to_check)
    price_len = len(str(int(float(info['price']) //1)))  #To find the number before decimal point


    # To search find price of Entry Point    # To search find price of Entry Point
    EZ = re.search(r"([Ee]ntry [Zz]one:)([0-9]+\.[0-9]+|[0-9]+) & ([0-9]+\.[0-9]+|[0-9]+)", text)
    ez_first_int =EZ.group(2)
    ez_last_int = EZ.group(3)


    # To find Selling Target
    ST = re.search(r'([0-9]+\.[0-9]+|[0-9]+)-([0-9]+\.[0-9]+|[0-9]+)-([0-9]+\.[0-9]+|[0-9]+)-([0-9]+\.[0-9]+|[0-9]+)-([0-9]+\.[0-9]+|[0-9]+)', text)
    st_first = ST.group(1)
    st_second = ST.group(2)
    st_third = ST.group(3)
    st_fourth = ST.group(4)



    # To find Stop Loss
    for i in text.split('\n\n'):
        if 'stoploss' in i.lower():
            sl = i.split()[-1]
        elif 'scalp' in i.lower():
            scalp = re.search(r'(long|short)', i.lower())
            if scalp.group(0) == 'long':
                b = 'Long'
            if scalp.group(0) == 'short':
                b = 'Short'

    if '.' not in ez_first_int:
    # To place the decimal point in price
        if price_len == 1 and info['price'].startswith('0'):
            ez_first_int = '0.'+ ez_first_int[:]
            ez_last_int = '0.'+ ez_last_int[:]

            st_first = '0.' + st_first[:]
            st_second = '0.' + st_second[:]
            st_third = '0.' + st_third[:]
            st_fourth = '0.' + st_fourth[:]

            sl = '0.' + sl[:]


        else:
            ez_first_int = ez_first_int[:price_len] +'.'+ ez_first_int[price_len:]
            ez_last_int = ez_last_int[:price_len] +'.'+ ez_last_int[price_len:]

            st_first = st_first[:price_len] + '.' + st_first[price_len:]
            st_second = st_second[:price_len] + '.' + st_second[price_len:]
            st_third = st_third[:price_len] + '.' + st_third[price_len:]
            st_fourth = st_fourth[:price_len] + '.' + st_fourth[price_len:]

            sl = sl[:price_len] + '.' + sl[price_len:]


    final_output += f'#{symbol_search.group(2)}/{symbol_search.group(3)}\n'
    final_output += text.split('\n\n')[-1] + '\n'
    final_output += f'Signal Type: Regular ({b})\n'
    final_output += 'Leverage: Cross (20.0X)\n'
    final_output += 'Amount: 2.0%\n\n'
    final_output += 'Entry Targets:\n'
    final_output += f'1) {ez_first_int}\n'
    final_output += f'2) {ez_last_int}\n\n'
    final_output += 'Take-Profit Targets:\n'
    final_output += f'1) {st_first}\n'
    final_output += f'2) {st_second}\n'
    final_output += f'3) {st_third}\n'
    final_output += f'4) {st_fourth}\n\n'
    final_output += 'Stop Targets:\n'
    final_output += f'1) {sl}'

    return final_output



def main():
    client.start()
    print("Userbot on!")
    client.run_until_disconnected()





@client.on(events.NewMessage(chats = INPUT))
async def forward(event):
    chat_id = event.original_update.message.peer_id
    chat_info = await client.get_entity(chat_id)
    chat_link = f'Forward : [{chat_info.title}](t.me/{chat_info.username})\n'
    text = event.text
    text = change_text(text)    
    
    text = chat_link + text
    if event.message.media is not None:
        # To download the media
        media = event.message.media
        path = await client.download_media(media)
        if text is None:
            await client.send_message(OUTPUT,  file = path)# link_preview=False,
        else:
            await client.send_message(OUTPUT, message = text, file = path)# link_preview=False
        os.remove(path)
    elif text:
        await client.send_message(OUTPUT, message = text)# link_preview=False,

if __name__ == "__main__":
    main()



