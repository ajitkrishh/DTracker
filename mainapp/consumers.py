import asyncio
import json
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async,async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from django_celery_beat.models import PeriodicTask,IntervalSchedule

from mainapp.models import stock,selected_stock

class StockConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def getStocklist(self):
        return list(selected_stock.objects.all().distinct().values_list('ticker__ticker' , flat= True))
    
    @sync_to_async
    def getpersonal_Stocklist(self):
        return list(selected_stock.objects.filter(user = self.scope['user']).distinct().values_list('ticker__ticker' , flat= True))
    
    @sync_to_async
    def addToCeleryBeat(self):
        task = PeriodicTask.objects.filter(name = "every-20-seconds").first()
        if task:
            args = json.loads(task.args)
            args = args[0]
            for i in self.stocklist:
                if i not in args:
                    args.append(i)
            task.args = json.dumps([args])
            # print(task.args)
            task.save()
        else:
            schedule,created = IntervalSchedule.objects.get_or_create(every = 20 , period = IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(interval = schedule , name = 'every-20-seconds' , task = 'mainapp.tasks.update_stock_list' , args = json.dumps([self.stocklist]))

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "stock_%s" % self.room_name
        self.stocklist = await self.getStocklist()
        self.personal_stocklist = await self.getpersonal_Stocklist()
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        try:         
            query_params = parse_qs(self.scope['query_string'].decode())
            print("query_params" ,query_params)
        except Exception as e:
            print("exceptoipn " , e)
        finally:
            await self.addToCeleryBeat()
            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        self.close()
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "stock_update", "message": message}
        )

    # Receive message from room group
    async def stock_update(self, event):
        message = event["message"]

        # Send message to WebSocket
        
        stockname =list( message.keys())[0]
        if stockname in self.personal_stocklist:
            await self.send(text_data=json.dumps( message))