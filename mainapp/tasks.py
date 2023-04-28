import asyncio
import aiohttp
from django.db import transaction
import random
from celery import shared_task
from yahoo_fin.stock_info import *
from django.conf import settings
from datetime import datetime as dt
from channels.layers import get_channel_layer
from mainapp.models import stock
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


query_url = settings.QUERY_URL

@shared_task(bind =True)
def clean_stock_track(self):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_discard)('stock_track', 'clean-up')

async def get_stock(session, ticker):
    try:
        url = query_url + ticker.lower()
        async with session.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}) as response:
            data = await response.json()
            # return (ticker, data["chart"]["result"][0])
            return (ticker, data[0])
    except Exception as e:
        print(e, "at get stock, ticker is " , ticker)
        return None
    

async def send_stock_update_to_channel_layer(neededdata):
    channel_layer = get_channel_layer()
    await channel_layer.group_send('stock_track', {
        'type': 'stock_update',
        'message': neededdata
    })

async def update(stocklist):
    print("stocklist from main update ",stocklist)
    if len(stocklist) > 0:
        async with aiohttp.ClientSession() as session:
            tasks = [get_stock(session, ticker) for ticker in stocklist]
            results = await asyncio.gather(*tasks)

        stocks = []
        for data in results:
            data1 = data[1]
            neededdata = [data1[i] for i in range(1,5)]
        # for data in results:
        #     data1 = data[1]
        #     neededdata = [
        #         data1["meta"]["regularMarketPrice"],
        #         data1["meta"]["previousClose"]
        #         ]
        #     keys = ["open","close","high","low"]
        #     data1 = data1["indicators"]["quote"][0]
        #     quote = []
        #     idx  = -2
        #     flag = False
        #     while not flag:
        #         for key in keys:
        #             if key == 'close':
        #                 x = data1[key][idx -1]
        #             else:
        #                 x = data1[key][idx]
        #             if not x:
        #                 quote.clear()
        #                 idx -=1
        #                 break
        #             else:
        #                 quote.append(x)
        #                 if key == 'low':
        #                     flag = True
        #     neededdata.extend(quote)
            neededdata =  [round(item,3) for item in neededdata]
            # stocks.append(stock(ticker=data[0], current_price=neededdata[0], previous_close=neededdata[1], open=neededdata[2], close=neededdata[3], high=neededdata[4], low=neededdata[5]))
            await send_stock_update_to_channel_layer({data[0]:neededdata})

        try:
            with transaction.atomic():
                stock.objects.bulk_update(stocks)
            
        except Exception as e:
            return f"Error: {e}"
        return 'Done'
    else:
        return "No Stocks"


@shared_task(bind =True)
def update_stock_list(self,stocklist):
    asyncio.run(update(stocklist))

'''
 C:/Users/ajitk/.virtualenvs/django-N-DyJwgQ/Scripts/activate.bat  
 celery -A stockTracker.celery worker --pool=solo -l info
 celery -A stockTracker beat -l INFO
'''

