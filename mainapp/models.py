from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class stock(models.Model):
    ticker = models.CharField(max_length= 20 , null=False ,blank=False , unique=True)

    def __str__(self) -> str:
        return self.ticker
    
class selected_stock(models.Model):
    user = models.ForeignKey(User,on_delete= models.CASCADE)
    ticker = models.ForeignKey(stock ,on_delete= models.CASCADE)
    
